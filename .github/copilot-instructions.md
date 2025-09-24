# Copilot instructions for this repository

Goal: Help an AI coding agent be productive immediately in this repo by knowing how things are structured, how they run, and what conventions to follow.

## What this repo is
- Centralized CI/CD helper scripts used by multiple repos to validate, tag, upload, and release Excel SOP templates.
- Not a Python package. Top-level Python scripts and Bash/PowerShell utilities are invoked directly or via GitHub Actions.

## Architecture at a glance
- Python
  - `check_excel_refs.py`: scans Excel files for `#REF!` across cells, array formulas, data validations, defined names, and raw XLSX XML; can export sheets to CSV (under `exploded/<file>/sheets`).
  - `update_excel_metadata.py`: opens the XLSX zip, edits `docProps/core.xml` to set version (`RELEASE_TAG`) and keywords (`COMMIT_HASH`).
  - `run_integration_tests.py`: driver to run integration tests against the `xl-test` repo (creates PRs, waits for checks).
- Shell (Linux/macOS runners)
  - `auth_and_prepare.sh`: loads `.env`, validates required env vars, authenticates to Qualer, extracts CSRF token and cookies into `tmp/`.
  - `validate_upload.sh`: pre-merge “smoke” step that sources `auth_and_prepare.sh` only (no upload).
  - `upload_sop.sh`: uploads the Excel file to Qualer and then updates SOP metadata via POST; expects CSRF and cookies from `auth_and_prepare.sh`.
- Workflows (reusable): `.github/workflows/`
  - `pre-check.yml`: called on PRs in downstream repos. Detects Excel file changes, validates env/secrets, runs `check_excel_refs.py`.
  - `upload-release.yml`: called on merge. Re-validates, updates Excel metadata (Windows), uploads to SharePoint and Qualer, creates a GitHub release.
  - `ci.yml`: repo’s own CI (lint, type-check, unit + optional integration tests). `protect-main.yml` applies branch protection to `xl-*` repos.

## Key developer workflows
- Install and test locally
  - `python -m venv .venv && source .venv/bin/activate` (Windows Git Bash: `source .venv/Scripts/activate`)
  - `pip install -r requirements.txt`
  - Lint: `flake8 .`  Format check: `black --check .`  Type-check: `mypy check_excel_refs.py update_excel_metadata.py`
  - Run fast tests: `pytest -m "not integration" -v`
  - Run integration (requires `GITHUB_TOKEN` with repo scope): `python run_integration_tests.py`

- Manual Excel validation examples
  - `EXCEL_FILE=tests/test_files/has_no_errors.xltm python check_excel_refs.py`
  - Export formulas to CSV: `EXPORT_SHEETS=true EXCEL_FILE=... python check_excel_refs.py`
  - Extra debug: `DEBUG_EXCEL=true EXCEL_FILE=... python check_excel_refs.py`

## Required configuration and env vars
- Qualer auth (secrets in workflows): `QUALER_EMAIL`, `QUALER_PASSWORD`.
- Excel/SOP metadata (usually from `.env` or workflow inputs):
  - `EXCEL_FILE`, `SOP_ID`, `AUTHOR_NAME`, `COMMIT_HASH`, `DOC_ID`, `DOC_TITLE`, `DOC_DETAILS`.
  - Release tagging: `RELEASE_TAG` (usually date, e.g., `YYYY-MM-DD`).
- Integration tests: `GITHUB_TOKEN` and optionally `SKIP_INTEGRATION=true` to bypass.
- SharePoint (for release sync): `SHAREPOINT_CLIENT_ID`, `SHAREPOINT_CLIENT_SECRET`, `SHAREPOINT_TENANT_ID` (workflows only).

## Conventions and patterns
- Scripts are single-file entry points; prefer environment-driven configuration over flags to match current usage.
- For Excel scanning, prefer `openpyxl` with `data_only=false`, also scan validations/defined names, and fall back to raw XML zip scanning when needed.
- On PRs: only validate and refuse merges on `#REF!`. On merges: tag Excel (`update_excel_metadata.py` on Windows), upload to SharePoint, rename with date, upload to Qualer, create a GitHub Release.
- Output style: informative logs with clear SUCCESS/ERROR lines; exit non-zero on any failure. Temporary files live in `tmp/` and `exploded/`.
- Tests live in `tests/`; unit tests avoid external services; integration tests are marked `@pytest.mark.integration` and are gated by env.

## What to reference when extending
- Examples of robust Excel scanning and export: `check_excel_refs.py`, `tests/test_check_excel_refs.py`.
- Example of XLSX metadata manipulation: `update_excel_metadata.py`.
- Auth + CSRF flow for Qualer: `auth_and_prepare.sh` then `upload_sop.sh` (watch for HTML “Object moved” and JSON `"Success":true`).
- How reusable workflows consume these scripts: `pre-check.yml` and `upload-release.yml`.

If anything above is unclear (e.g., additional env vars a downstream repo expects), ask to confirm and we’ll amend this file.

## Downstream usage examples (xl-test, xlTemplate)

These repos call the reusable workflows in this repo via `workflow_call` to validate Excel changes on PRs and to upload/release on merge.


  ```yaml
  name: Pre-Check Excel
  on:
    pull_request:
      branches: [ main ]

  jobs:
    pre-check:
      uses: Johnson-Gage-Inspection-Inc/ci-scripts/.github/workflows/pre-check.yml@main
      with:
        repo_name: ${{ github.repository }}
        branch: main
      secrets:
        QUALER_EMAIL: ${{ secrets.QUALER_EMAIL }}
        QUALER_PASSWORD: ${{ secrets.QUALER_PASSWORD }}
        SHAREPOINT_CLIENT_ID: ${{ secrets.SHAREPOINT_CLIENT_ID }}
        SHAREPOINT_CLIENT_SECRET: ${{ secrets.SHAREPOINT_CLIENT_SECRET }}
        SHAREPOINT_TENANT_ID: ${{ secrets.SHAREPOINT_TENANT_ID }}
  ```

  Notes:
  - The reusable workflow detects changed `*.xl*` files, ensures only one Excel file is present, and outputs `EXCEL_FILE`.
  - `.env` in the caller repo should provide: `SOP_ID`, `DOC_ID`, `DOC_TITLE`, `DOC_DETAILS` (and optionally anything else you want in Qualer details).
  - If no Excel files are changed, the job exits cleanly and sets `SKIP_UPLOAD=true` for downstream jobs.

#### xl-test variations from the generic examples

`xl-test` intentionally differs from the generic examples above:

- Uses the `dev` ref of this repo for reusable workflows while iterating:
  - `uses: Johnson-Gage-Inspection-Inc/ci-scripts/.github/workflows/<workflow>.yml@dev`

PR-trigger (pre-merge checks):

```yaml
name: Pre-Merge Checks
on:
  pull_request:
    branches: [ main ]

jobs:
  validate:
    uses: Johnson-Gage-Inspection-Inc/ci-scripts/.github/workflows/pre-check.yml@dev
    with:
      repo_name: Johnson-Gage-Inspection-Inc/xl-test  # or use ${{ github.repository }}
    secrets:
      QUALER_EMAIL: ${{ secrets.QUALER_EMAIL }}
      QUALER_PASSWORD: ${{ secrets.QUALER_PASSWORD }}
      SHAREPOINT_CLIENT_ID: ${{ secrets.SHAREPOINT_CLIENT_ID }}
      SHAREPOINT_CLIENT_SECRET: ${{ secrets.SHAREPOINT_CLIENT_SECRET }}
      SHAREPOINT_TENANT_ID: ${{ secrets.SHAREPOINT_TENANT_ID }}
```

MR-trigger (upload + release when PR is merged):

```yaml
name: Upload & Release on Merge
on:
  pull_request:
    branches: [ main ]
    types: [ closed ]

jobs:
  MR-workflow:
    if: github.event.pull_request.merged == true
    uses: Johnson-Gage-Inspection-Inc/ci-scripts/.github/workflows/upload-release.yml@dev
    with:
      repo_name: Johnson-Gage-Inspection-Inc/xl-test  # or use ${{ github.repository }}
    secrets:
      QUALER_EMAIL: ${{ secrets.QUALER_EMAIL }}
      QUALER_PASSWORD: ${{ secrets.QUALER_PASSWORD }}
      SHAREPOINT_CLIENT_ID: ${{ secrets.SHAREPOINT_CLIENT_ID }}
      SHAREPOINT_CLIENT_SECRET: ${{ secrets.SHAREPOINT_CLIENT_SECRET }}
      SHAREPOINT_TENANT_ID: ${{ secrets.SHAREPOINT_TENANT_ID }}
```

Tip: To lock in stable behavior, merge `ci-scripts`' `dev` into `main` (callers don’t need to change refs). Only pin `@main` in callers if you explicitly want them tied to the stable line.

- Upload + Release on merge (in the caller repo after merging to `main`):

  ```yaml
  name: Upload & Release on Merge
  on:
    push:
      branches: [ main ]

  jobs:
    upload-release:
      uses: Johnson-Gage-Inspection-Inc/ci-scripts/.github/workflows/upload-release.yml@main
      with:
        repo_name: ${{ github.repository }}
        branch: main
      secrets:
        QUALER_EMAIL: ${{ secrets.QUALER_EMAIL }}
        QUALER_PASSWORD: ${{ secrets.QUALER_PASSWORD }}
        SHAREPOINT_CLIENT_ID: ${{ secrets.SHAREPOINT_CLIENT_ID }}
        SHAREPOINT_CLIENT_SECRET: ${{ secrets.SHAREPOINT_CLIENT_SECRET }}
        SHAREPOINT_TENANT_ID: ${{ secrets.SHAREPOINT_TENANT_ID }}
  ```

  What happens:
  - Re-validate Excel file change and compute `COMMIT_HASH` and `RELEASE_TAG`.
  - Update Excel metadata on Windows (`update_excel_metadata.py`).
  - Upload to SharePoint and to Qualer (`upload_sop.sh`) using secrets.
  - Rename the file with date and create a GitHub Release with the renamed artifact.
