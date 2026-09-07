#!/usr/bin/env python3
"""
Bulk Email Sender (Outlook SMTP)

Sends personalized emails from a CSV of recipients. Uses a config file for
subject, body template, CC, BCC, and attachments. Body template supports
{{email}}, {{name}}, {{surname}}, {{custom_line}}.

Credentials are prompted when you run the script (password is hidden). They
exist only in memory and are not written to disk. Optional: set OUTLOOK_EMAIL
and OUTLOOK_PASSWORD in the environment to skip prompts.

Example:
  python scripts/bulk_email/send.py --config scripts/bulk_email/config.yaml
  python scripts/bulk_email/send.py --config config.yaml --dry-run --limit 2
"""
import argparse
import csv
import getpass
import os
import smtplib
import sys
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import yaml


# Default SMTP (override in config: smtp_host, smtp_port, smtp_timeout)
DEFAULT_SMTP_HOST = "smtp.office365.com"
DEFAULT_SMTP_PORT = 587
DEFAULT_SMTP_TIMEOUT = 30
DEFAULT_SMTP_DELAY = 2


def load_config(config_path: Path) -> dict:
    """Load YAML config. Raises if file missing or invalid."""
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_recipients(csv_path: Path) -> list[dict]:
    """Load recipients from CSV. Required: email, name, surname, custom_line. Optional: cc (comma-separated)."""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    rows = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = [h.strip().lower() for h in (reader.fieldnames or [])]
        required = {"email", "name", "surname", "custom_line"}
        if required.issubset(set(fieldnames)):
            for row in reader:
                row = {k.strip().lower(): (v or "").strip() for k, v in row.items()}
                if row.get("email"):
                    rows.append(row)
        else:
            raise ValueError(
                f"CSV must have columns: email, name, surname, custom_line (optional: cc). Got: {reader.fieldnames}"
            )
    return rows


def render_body(template: str, recipient: dict) -> str:
    """Replace {{key}} in template with recipient values."""
    text = template
    for key, value in recipient.items():
        text = text.replace(f"{{{{{key}}}}}", str(value))
    return text


def build_message(
    *,
    sender: str,
    recipient_email: str,
    subject: str,
    body_text: str,
    body_html: str | None,
    cc: list[str],
    bcc: list[str],
    attachment_paths: list[Path],
    base_dir: Path,
) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = recipient_email
    msg["Subject"] = subject
    if cc:
        msg["Cc"] = ", ".join(cc)

    if body_html:
        msg.attach(MIMEText(body_text, "plain", "utf-8"))
        msg.attach(MIMEText(body_html, "html", "utf-8"))
    else:
        msg.attach(MIMEText(body_text, "plain", "utf-8"))

    for rel_path in attachment_paths:
        path = (base_dir / rel_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Attachment not found: {path}")
        with open(path, "rb") as f:
            part = MIMEApplication(f.read(), _subtype=path.suffix.lstrip(".") or "bin")
        part.add_header("Content-Disposition", "attachment", filename=path.name)
        msg.attach(part)

    return msg


def get_credentials() -> tuple[str, str]:
    """Get Outlook credentials: env vars first, then prompt (password hidden). Kept only in memory."""
    email = os.environ.get("OUTLOOK_EMAIL", "").strip()
    password = os.environ.get("OUTLOOK_PASSWORD", "").strip()
    if not email or not password:
        print("Outlook credentials (used only for this run, not stored):")
        email = (email or input("Email: ")).strip()
        password = password or getpass.getpass("Password: ")
    if not email or not password:
        raise SystemExit("Email and password are required.")
    return email, password


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send bulk emails from CSV using Outlook SMTP and a config file."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("scripts/bulk_email/config.yaml"),
        help="Path to YAML config (subject, body/body_file, cc, bcc, attachments, csv path)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not send; print recipient and subject only.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Send only to the first N recipients (for testing).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=None,
        metavar="SECS",
        help="Seconds to wait between sends (overrides config; default from config or " + str(DEFAULT_SMTP_DELAY) + ").",
    )
    parser.add_argument(
        "--smtp-timeout",
        type=int,
        default=None,
        metavar="SECS",
        help="SMTP connection timeout in seconds (overrides config).",
    )
    args = parser.parse_args()

    base_dir = Path.cwd()
    config_path = (base_dir / args.config).resolve()
    if not config_path.is_absolute():
        config_path = base_dir / args.config

    try:
        config = load_config(config_path)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Invalid YAML in {config_path}: {e}", file=sys.stderr)
        sys.exit(1)

    csv_path = config.get("csv_path")
    if not csv_path:
        print("Config must set 'csv_path' (path to recipients CSV).", file=sys.stderr)
        sys.exit(1)
    csv_path = (config_path.parent / csv_path).resolve()
    if not csv_path.exists():
        csv_path = (base_dir / config.get("csv_path")).resolve()

    try:
        recipients = load_recipients(csv_path)
    except (FileNotFoundError, ValueError) as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if args.limit is not None:
        recipients = recipients[: args.limit]

    subject = (config.get("subject") or "").strip()
    if not subject:
        print("Config must set 'subject'.", file=sys.stderr)
        sys.exit(1)

    body_file = config.get("body_file")
    body_inline = (config.get("body") or "").strip()
    body_html_file = config.get("body_html_file")

    body_template = None
    if body_file:
        body_path = (config_path.parent / body_file).resolve()
        if not body_path.exists():
            body_path = (base_dir / body_file).resolve()
        if body_path.exists():
            with open(body_path, "r", encoding="utf-8") as f:
                body_template = f.read()
        else:
            print(f"body_file not found: {body_file}", file=sys.stderr)
            sys.exit(1)
    elif body_inline:
        body_template = body_inline

    body_html_template = None
    if body_html_file:
        html_path = (config_path.parent / body_html_file).resolve()
        if not html_path.exists():
            html_path = (base_dir / body_html_file).resolve()
        if html_path.exists():
            with open(html_path, "r", encoding="utf-8") as f:
                body_html_template = f.read()
        else:
            print(f"body_html_file not found: {body_html_file}", file=sys.stderr)
            sys.exit(1)

    if not body_template and not body_html_template:
        print(
            "Config must set at least one of: 'body', 'body_file', or 'body_html_file'.",
            file=sys.stderr,
        )
        sys.exit(1)
    if not body_template and body_html_template:
        body_template = ""  # HTML-only: plain part empty

    _cc = config.get("cc")
    cc = [a.strip() for a in (_cc if isinstance(_cc, list) else [])]
    _bcc = config.get("bcc")
    bcc = [a.strip() for a in (_bcc if isinstance(_bcc, list) else [])]
    attachment_paths = [Path(p.strip()) for p in config.get("attachments") or []]

    smtp_host = config.get("smtp_host") or DEFAULT_SMTP_HOST
    smtp_port = int(config.get("smtp_port") or DEFAULT_SMTP_PORT)
    smtp_timeout = (
        args.smtp_timeout
        if args.smtp_timeout is not None
        else int(config.get("smtp_timeout") or DEFAULT_SMTP_TIMEOUT)
    )
    smtp_use_tls = config.get("smtp_use_tls", True)
    smtp_auth = config.get("smtp_auth", True)
    delay_secs = (
        args.delay
        if args.delay is not None
        else float(config.get("delay") or DEFAULT_SMTP_DELAY)
    )

    if args.dry_run:
        print(f"DRY RUN: would send to {len(recipients)} recipient(s).")
        for i, r in enumerate(recipients, 1):
            subj = render_body(subject, r)
            row_cc = (r.get("cc") or "").strip()
            extra = f" | cc={row_cc}" if row_cc else ""
            print(f"  {i}. {r.get('email')}{extra} | {subj[:60]}{'...' if len(subj) > 60 else ''}")
        return

    if smtp_auth:
        sender, password = get_credentials()
    else:
        sender = (config.get("sender") or "").strip()
        if not sender:
            sender = input("Sender email (From address): ").strip()
        if not sender:
            raise SystemExit("Sender email is required when smtp_auth is false (set 'sender' in config or enter when prompted).")
        password = None

    for i, recipient in enumerate(recipients):
        to_email = recipient["email"]
        body_text = render_body(body_template, recipient)
        body_html = render_body(body_html_template, recipient) if body_html_template else None
        subj = render_body(subject, recipient)

        # Optional per-row CC (comma/semicolon-separated), merged with config CC
        row_cc = []
        raw_cc = (recipient.get("cc") or "").replace(";", ",")
        for part in raw_cc.split(","):
            addr = part.strip()
            if addr and addr.lower() != to_email.lower() and addr not in row_cc:
                row_cc.append(addr)
        msg_cc = []
        for addr in cc + row_cc:
            if addr and addr.lower() != to_email.lower() and addr not in msg_cc:
                msg_cc.append(addr)

        try:
            msg = build_message(
                sender=sender,
                recipient_email=to_email,
                subject=subj,
                body_text=body_text,
                body_html=body_html,
                cc=msg_cc,
                bcc=bcc,
                attachment_paths=attachment_paths,
                base_dir=config_path.parent,
            )
        except FileNotFoundError as e:
            print(f"Skip {to_email}: {e}", file=sys.stderr)
            continue

        to_list = [to_email] + msg_cc + bcc
        try:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=smtp_timeout) as smtp:
                if smtp_use_tls:
                    smtp.starttls()
                if smtp_auth:
                    smtp.login(sender, password)
                smtp.sendmail(sender, to_list, msg.as_string())
            print(f"Sent ({i + 1}/{len(recipients)}): {to_email}")
        except smtplib.SMTPException as e:
            print(f"Failed {to_email}: {e}", file=sys.stderr)

        if i < len(recipients) - 1 and delay_secs > 0:
            time.sleep(delay_secs)


if __name__ == "__main__":
    main()
