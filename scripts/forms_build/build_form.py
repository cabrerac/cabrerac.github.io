#!/usr/bin/env python3
"""Build a Google Form from a YAML spec in forms-sources/."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# drive scope needed to move the form into a folder the user owns
SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/drive",
]

SCRIPT_DIR = Path(__file__).resolve().parent
SOURCES_DIR = SCRIPT_DIR / "forms-sources"
CLIENT_SECRETS = SCRIPT_DIR / "client_secrets.json"
TOKEN_FILE = SCRIPT_DIR / "token.json"


def forms_line(text: str) -> str:
    """Google Forms displayed text must not contain newlines."""
    return " ".join(text.split())


def load_spec(stem: str) -> dict[str, Any]:
    spec_path = SOURCES_DIR / f"{stem}.yaml"
    if not spec_path.exists():
        raise FileNotFoundError(f"Spec not found: {spec_path}")
    with open(spec_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_credentials(login_hint: str | None = None) -> Credentials:
    creds: Credentials | None = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRETS.exists():
                raise FileNotFoundError(
                    f"Missing {CLIENT_SECRETS}. See scripts/forms_build/README.md"
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS), SCOPES)
            run_kwargs: dict[str, Any] = {"port": 0}
            if login_hint:
                run_kwargs["login_hint"] = login_hint
                print(f"OAuth login hint: {login_hint} (pick this account in the browser)")
            creds = flow.run_local_server(**run_kwargs)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    elif creds.scopes is not None and not set(SCOPES).issubset(set(creds.scopes)):
        TOKEN_FILE.unlink(missing_ok=True)
        return get_credentials(login_hint=login_hint)
    return creds


def choice_question(title: str, options: list[str], checkbox: bool, required: bool) -> dict:
    return {
        "questionItem": {
            "question": {
                "required": required,
                "choiceQuestion": {
                    "type": "CHECKBOX" if checkbox else "RADIO",
                    "options": [{"value": forms_line(opt)} for opt in options],
                },
            }
        },
        "title": forms_line(title),
    }


def text_question(title: str, paragraph: bool, required: bool) -> dict:
    return {
        "questionItem": {
            "question": {
                "required": required,
                "textQuestion": {"paragraph": paragraph},
            }
        },
        "title": forms_line(title),
    }


def build_item(item: dict[str, Any]) -> dict:
    item_type = item["type"]
    title = item["title"]
    required = bool(item.get("required", False))

    if item_type == "text":
        return text_question(title, paragraph=False, required=required)
    if item_type == "paragraph":
        return text_question(title, paragraph=True, required=required)
    if item_type == "choice":
        return choice_question(title, item["options"], checkbox=False, required=required)
    if item_type == "checkbox":
        return choice_question(title, item["options"], checkbox=True, required=required)
    if item_type == "info":
        return {"textItem": {}, "title": forms_line(title)}
    raise ValueError(f"Unknown item type: {item_type}")


def page_break_item(title: str, description: str | None = None) -> dict:
    """PageBreakItem has no nested fields — title/description live on Item."""
    item: dict[str, Any] = {"title": forms_line(title), "pageBreakItem": {}}
    if description:
        item["description"] = forms_line(description)
    return item


def build_requests(spec: dict[str, Any]) -> list[dict]:
    requests: list[dict] = []
    index = 0
    form_info = spec["form"]

    if form_info.get("description"):
        requests.append(
            {
                "updateFormInfo": {
                    "info": {"description": forms_line(form_info["description"])},
                    "updateMask": "description",
                }
            }
        )

    email_collection = form_info.get("email_collection_type")
    if email_collection:
        requests.append(
            {
                "updateSettings": {
                    "settings": {"emailCollectionType": email_collection},
                    "updateMask": "emailCollectionType",
                }
            }
        )

    for section in spec.get("sections", []):
        requests.append(
            {
                "createItem": {
                    "item": page_break_item(section["title"], section.get("description")),
                    "location": {"index": index},
                }
            }
        )
        index += 1

        for item in section.get("items", []):
            built = build_item(item)
            if item.get("description"):
                built["title"] = forms_line(
                    f"{built['title']} — {item['description']}"
                )
            requests.append(
                {"createItem": {"item": built, "location": {"index": index}}}
            )
            index += 1

    return requests


def normalize_folder_id(folder_id: str) -> str:
    """Accept raw ID or a full Drive folder URL."""
    folder_id = folder_id.strip().strip('"').strip("'")
    if "/folders/" in folder_id:
        folder_id = folder_id.split("/folders/", 1)[1].split("?", 1)[0].split("/", 1)[0]
    return folder_id


def _drive_api_help(error: HttpError, *, folder_id: str | None = None) -> str:
    """Return a short hint for common Drive API setup errors."""
    try:
        details = error.error_details if hasattr(error, "error_details") else []
        for item in details or []:
            reason = item.get("reason")
            if reason == "accessNotConfigured":
                return (
                    "\n\nEnable the Google Drive API for your Cloud project:\n"
                    "  APIs & Services → Library → search \"Google Drive API\" → Enable\n"
                    "  Or open the link from the error message above, then wait ~1 minute and retry.\n"
                    "  See scripts/forms_build/README.md § Enable Google Drive API."
                )
            if reason == "notFound" and folder_id:
                return (
                    f"\n\nDrive returned 'not found' for folder {folder_id!r}. Common causes:\n"
                    "  1. Wrong folder ID — copy it again from the folder URL while the folder is open.\n"
                    "  2. Account mismatch — the folder must be visible to the SAME Google account\n"
                    "     you used for OAuth (check the line printed above: 'Authenticated as …').\n"
                    "     If the folder lives on another account, either:\n"
                    "       • create the folder on chc79@cam.ac.uk and use that ID, or\n"
                    "       • share the folder with chc79@cam.ac.uk as Editor, then retry.\n"
                    "  3. Folder deleted or you lack access.\n"
                    "See scripts/forms_build/README.md § Folder not found (404)."
                )
    except Exception:
        pass
    return ""


def drive_authenticated_user(drive_service) -> str:
    """Return the email of the account authorized in token.json."""
    about = (
        drive_service.about()
        .get(fields="user(emailAddress,displayName)")
        .execute()
    )
    user = about.get("user", {})
    email = user.get("emailAddress", "unknown")
    name = user.get("displayName")
    return f"{email} ({name})" if name else email


def move_form_to_folder(drive_service, form_id: str, folder_id: str) -> list[str]:
    """Move the form (a Drive file) into folder_id. Returns new parent IDs."""
    folder_id = normalize_folder_id(folder_id)
    drive_kwargs = {"supportsAllDrives": True}

    try:
        folder_meta = (
            drive_service.files()
            .get(fileId=folder_id, fields="id,name,mimeType,driveId", **drive_kwargs)
            .execute()
        )
    except HttpError as exc:
        raise RuntimeError(
            f"Could not read Drive folder {folder_id!r}."
            f"{_drive_api_help(exc, folder_id=folder_id)}"
        ) from exc
    if folder_meta.get("mimeType") != "application/vnd.google-apps.folder":
        raise ValueError(
            f"drive_folder_id {folder_id!r} is not a folder "
            f"(mimeType={folder_meta.get('mimeType')})."
        )
    print(f"  Target folder: {folder_meta.get('name', folder_id)}")

    file_meta = (
        drive_service.files()
        .get(fileId=form_id, fields="id,name,parents,mimeType", **drive_kwargs)
        .execute()
    )
    previous_parents = file_meta.get("parents", [])
    if folder_id in previous_parents:
        print("  Form is already in the target folder.")
        return previous_parents

    previous = ",".join(previous_parents) if previous_parents else None
    update_kwargs: dict[str, Any] = {
        "fileId": form_id,
        "addParents": folder_id,
        "fields": "id, parents",
        **drive_kwargs,
    }
    if previous:
        update_kwargs["removeParents"] = previous

    updated = drive_service.files().update(**update_kwargs).execute()
    new_parents = updated.get("parents", [])
    if folder_id not in new_parents:
        raise RuntimeError(
            f"Drive move did not stick. Expected parent {folder_id}, got {new_parents}."
        )
    print(f"  Moved. Parents now: {new_parents}")
    return new_parents


def write_output_meta(
    stem: str,
    form_id: str,
    responder_url: str,
    edit_url: str,
    spec: dict[str, Any],
    drive_folder_id: str | None,
) -> None:
    out_path = SOURCES_DIR / f"{stem}.out.yaml"
    form_info = spec.get("form", {})
    meta = {
        "form_id": form_id,
        "responder_url": responder_url,
        "edit_url": edit_url,
        "drive_folder_id": drive_folder_id,
        "confirmation_message_manual": (
            "The Forms API v1 does not expose confirmation text. "
            "Paste the block below in Google Forms → Settings → Presentation."
        ),
        "confirmation_message": form_info.get("confirmation_message", "").strip() or None,
        "note": "Paste responder_url into bulk email and Moodle.",
    }
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(meta, f, allow_unicode=True, sort_keys=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Google Form from YAML")
    parser.add_argument("spec_stem", help="YAML file stem in forms-sources/ (without .yaml)")
    parser.add_argument(
        "--form-id",
        help="Populate an existing empty form instead of creating a new one",
    )
    parser.add_argument(
        "--drive-folder-id",
        help="Drive folder ID or URL (overrides meta.drive_folder_id in YAML)",
    )
    parser.add_argument(
        "--move-only",
        action="store_true",
        help="Only move an existing form to drive_folder_id (requires --form-id)",
    )
    args = parser.parse_args()

    spec = load_spec(args.spec_stem)
    form_info = spec["form"]
    meta = spec.get("meta", {})
    drive_folder_id = args.drive_folder_id or meta.get("drive_folder_id")

    creds = get_credentials(login_hint=meta.get("owner_account"))
    forms_service = build("forms", "v1", credentials=creds, cache_discovery=False)
    drive_service = build("drive", "v3", credentials=creds, cache_discovery=False)

    try:
        auth_user = drive_authenticated_user(drive_service)
        print(f"Authenticated as: {auth_user}")
    except HttpError:
        auth_user = "(could not read — check Drive API is enabled)"
        print(f"Authenticated as: {auth_user}")

    if args.move_only:
        if not args.form_id:
            parser.error("--move-only requires --form-id")
        if not drive_folder_id:
            parser.error("--move-only requires drive_folder_id in YAML or --drive-folder-id")
        form_id = args.form_id
        print(f"Moving form {form_id} to Drive folder…")
        move_form_to_folder(drive_service, form_id, drive_folder_id)
        created = forms_service.forms().get(formId=form_id).execute()
        responder_url = created.get("responderUri") or f"https://docs.google.com/forms/d/{form_id}/viewform"
        edit_url = f"https://docs.google.com/forms/d/{form_id}/edit"
        write_output_meta(args.spec_stem, form_id, responder_url, edit_url, spec, drive_folder_id)
        print("\nDone.")
        print(f"  Edit URL: {edit_url}")
        return 0

    if args.form_id:
        form_id = args.form_id
        print(f"Using existing formId: {form_id}")
        created = forms_service.forms().get(formId=form_id).execute()
    else:
        create_body = {"info": {"title": forms_line(form_info["title"])}}
        if form_info.get("document_title"):
            create_body["info"]["documentTitle"] = forms_line(form_info["document_title"])

        print(f"Creating form: {form_info['title']}")
        created = forms_service.forms().create(body=create_body).execute()
        form_id = created["formId"]
        print(f"  formId: {form_id}")

    requests = build_requests(spec)
    if requests:
        print(f"  Adding {len(requests)} batchUpdate requests...")
        forms_service.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()
        created = forms_service.forms().get(formId=form_id).execute()

    if drive_folder_id:
        print(f"  Moving form to Drive folder: {normalize_folder_id(drive_folder_id)}")
        move_form_to_folder(drive_service, form_id, drive_folder_id)
    else:
        print("  No drive_folder_id in YAML — form stays in Drive root.")

    responder_url = created.get("responderUri") or f"https://docs.google.com/forms/d/{form_id}/viewform"
    edit_url = f"https://docs.google.com/forms/d/{form_id}/edit"
    write_output_meta(args.spec_stem, form_id, responder_url, edit_url, spec, drive_folder_id)

    print("\nDone.")
    print(f"  Responder URL: {responder_url}")
    print(f"  Edit URL:      {edit_url}")
    print(f"  Metadata:      {SOURCES_DIR / f'{args.spec_stem}.out.yaml'}")
    if form_info.get("confirmation_message"):
        print("\n  Confirmation message: set manually in Forms UI (see .out.yaml).")
    print("\nManual checks in Google Forms UI (if needed):")
    print("  - Settings → Limit to 1 response")
    print("  - Settings → Link to Google Sheet for responses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
