# Google Forms builder

Build a Google Form from a YAML spec using the [Google Forms API](https://developers.google.com/workspace/forms/api/guides/create-form-quiz).

Run commands from the **repository root**.

## Layout

| Path | Role |
|------|------|
| `build_form.py` | Reads YAML → `forms.create` + `forms.batchUpdate` + optional Drive folder move |
| `forms-sources/*.yaml` | Machine-readable form specs (human spec: `work-space/teaching/big-data/planning/intake-form-spec.md`) |
| `forms-sources/*.out.yaml` | Written after a successful build (form ID, URLs — safe to commit once published) |
| `client_secrets.json` | OAuth client credentials (**local only**, gitignored) |
| `token.json` | OAuth token after first browser consent (**local only**, gitignored) |

## One-time setup

1. [Google Cloud Console](https://console.cloud.google.com/) — create a project (personal Gmail is fine for the Cloud project).
2. Enable **both** APIs (Forms alone is not enough if you use `drive_folder_id`):
   - **Google Forms API** — create and populate the form
   - **Google Drive API** — move the form file into a folder (see below)
3. **APIs & Services → Credentials → Create credentials → OAuth client ID → Desktop app**.
4. Download JSON → save as `scripts/forms_build/client_secrets.json`.
5. **OAuth consent screen → add test users** (required while the app is in *Testing* — see below).
6. Install dependencies (already in repo `requirements.txt`):

   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib pyyaml
   ```

### Enable Google Drive API (required for folder move)

If the form builds but stays in **My Drive root**, or you see:

`Google Drive API has not been used in project … or it is disabled`

then Drive API is not enabled yet (Forms API was, Drive was not):

1. Open your project in [Google Cloud Console](https://console.cloud.google.com/).
2. **APIs & Services → Library**.
3. Search **Google Drive API** → **Enable**.
4. Wait ~1 minute for propagation.
5. Re-run the move (no need to rebuild the form):

   ```bash
   python scripts/forms_build/build_form.py 26-udenar-big-data-intake \
     --move-only --form-id YOUR_FORM_ID
   ```

You do **not** need new OAuth credentials — only enable the API on the same project that owns `client_secrets.json`.

### Folder not found (404)

If move fails with `File not found` for your `drive_folder_id`:

1. **Check the account** — the script prints `Authenticated as: …`. That must be the account that **owns or can open** the folder in a browser.
2. **Re-copy the folder ID** — open the folder in Drive, copy from `…/drive/folders/THIS_PART` (not a file inside the folder).
3. **Account mismatch (most common)** — folder created on personal Gmail but OAuth signed in as `chc79@cam.ac.uk` (or the reverse). Fix:
   - Create the target folder **while signed in as the OAuth account**, update YAML with the new ID, **or**
   - Share the existing folder with `chc79@cam.ac.uk` as **Editor**, wait a minute, retry.
4. **Shared drives** — you need at least **Contributor** on that shared drive.

**Browser `/u/0/` vs `/u/1/`:** In a multi-account browser session, `drive.google.com/drive/u/1/folders/…` means the folder is on your **second** logged-in account (often `chc79@cam.ac.uk`), while `/u/0/` is the first (often personal Gmail). The OAuth token is tied to **one** account only. If `Authenticated as:` shows the wrong email, delete `token.json` and re-run — the script uses `meta.owner_account` as a login hint.

### Error 403: access_denied (app not verified)

If you see *"has not completed the Google verification process"* and *"can only be accessed by developer-approved testers"*, the OAuth app is in **Testing** mode. Add yourself as a test user:

1. **APIs & Services → OAuth consent screen → Test users → Add users**
2. Add **`chc79@cam.ac.uk`** (and personal Gmail if needed)
3. Delete `scripts/forms_build/token.json` if present
4. Re-run `build_form.py`

### Scope change (Drive folder support)

If you previously authenticated with older scopes, delete `token.json` and re-run so the script can request **Drive** access (needed to move the form into a folder).

YAML may use `|` multiline blocks for readability; the script flattens them to a single line (Google Forms rejects newlines in titles/descriptions).

## Build a form

```bash
python scripts/forms_build/build_form.py 26-udenar-big-data-intake
```

**First run:** sign in as **`chc79@cam.ac.uk`** when the browser opens.

### Populate an existing empty form

If a previous run created the title but failed on `batchUpdate`, reuse that form:

```bash
python scripts/forms_build/build_form.py 26-udenar-big-data-intake \
  --form-id 1wchR3PiDLEYDnReNTwgXED4P4nS-BZdVSQj_gDwR5y4
```

### Place the form in a Google Drive folder

1. Create or open the target folder in Drive.
2. Copy the folder ID from the URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
   (or paste the full URL — the script extracts the ID).
3. In `forms-sources/26-udenar-big-data-intake.yaml`, set:

   ```yaml
   meta:
     drive_folder_id: "FOLDER_ID_HERE"
   ```

4. Run the build script. After creation, the script **moves** the form into that folder and **verifies** the new parent.

The folder must belong to the same Google account you use for OAuth (or be shared with **Editor** access to that account). For **Shared drives**, the script uses `supportsAllDrives=True`.

**Move an already-created form** (without rebuilding questions):

```bash
python scripts/forms_build/build_form.py 26-udenar-big-data-intake \
  --move-only --form-id YOUR_FORM_ID
```

Or override the folder from the command line:

```bash
python scripts/forms_build/build_form.py 26-udenar-big-data-intake \
  --move-only --form-id YOUR_FORM_ID \
  --drive-folder-id "1p9B4ZsPwMl2ZINMCtZD2QF7yZ51m6vfw"
```

### Confirmation message

The Forms API **v1** does not support setting the post-submit confirmation text programmatically. After build, paste the `confirmation_message` block from the YAML (or from `*.out.yaml`) into **Google Forms → Settings → Presentation → Confirmation message**.

### After build

Paste `responder_url` from `forms-sources/26-udenar-big-data-intake.out.yaml` into bulk email and Moodle.

## Manual fallback

If OAuth is blocked, build the form manually from `work-space/teaching/big-data/planning/intake-form-spec.md` (~15–20 min).

## Student diagnostic submission

Students upload their completed `.ipynb` via Moodle. Naming convention:

```
diagnostic_{lastname}_{firstname}.ipynb
```

See `forms-sources/26-udenar-big-data-intake.yaml` → `meta.submission_notes`.
