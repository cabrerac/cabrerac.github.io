# Bulk email sender (Outlook)

Sends personalized emails from a CSV using Outlook SMTP. Body and subject can use `{{email}}`, `{{name}}`, `{{surname}}`, `{{custom_line}}`.

## CSV format

Create a CSV with headers: **email**, **name**, **surname**, **custom_line**. One row per recipient.

## Setup

1. Copy `config.example.yaml` to `config.yaml` and set:
   - `subject`, `body_file` (or `body`), `csv_path`
   - Optional: `cc`, `bcc`, `attachments`, `body_html_file`
2. Create your recipients CSV and body template (see `body_template.example.txt`).
3. **Credentials**: When you run the script (without `--dry-run`), it will prompt for your Outlook email and password. The password is hidden; credentials stay only in memory and are not saved. Optional: set `OUTLOOK_EMAIL` and `OUTLOOK_PASSWORD` in the environment to skip the prompts.

## Run

From the repo root:

```bash
# Dry run (no emails sent)
python scripts/bulk_email/send.py --config scripts/bulk_email/config.yaml --dry-run

# Test with 2 recipients
python scripts/bulk_email/send.py --config scripts/bulk_email/config.yaml --limit 2

# Send all
python scripts/bulk_email/send.py --config scripts/bulk_email/config.yaml
```

Use `--delay 3` to wait 3 seconds between sends (default 2). Use `--smtp-timeout 60` to allow more time for the SMTP connection.

## SMTP and timeouts

The script uses `smtp.office365.com:587` by default. You can override in config with `smtp_host`, `smtp_port`, and `smtp_timeout`. **Connection timeouts** often mean your network or firewall is blocking outbound SMTP (port 587 or 25). Try: running from another network (e.g. home or mobile hotspot), or using your institution’s VPN if they require it for SMTP.
