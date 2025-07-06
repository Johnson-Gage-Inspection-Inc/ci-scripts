# CI Scripts Repository

This repository serves as a central location for shared CI/CD scripts that can be used across multiple repositories in the organization. The primary script, `upload_sop.sh`, automates the process of uploading Excel SOP files to Qualer.

## 📌 Features
- **Centralized Management**: Update once, apply changes across all repositories.
- **Seamless Integration**: Easily referenced in GitHub Actions workflows.
- **Secure Authentication**: Uses GitHub Secrets for storing credentials.
- **Automated SOP File Upload**: Detects changes in Excel files and uploads them to Qualer.
- **Excel Reference Validation**: Checks for broken references (#REF! errors) before allowing merge.

---

## 📂 Repository Structure
```
ci-scripts/
│── upload_sop.sh          # Main script for uploading SOP files to Qualer
│── check_excel_refs.py    # Script to check for #REF! errors in Excel files
│── auth_and_prepare.sh    # Shared authentication & file preparation
│── validate_upload.sh     # Pre-merge validation script
│── main-protection.json   # Branch protection configuration
│── requirements.txt       # Python dependencies
│── README.md              # Documentation
```

---

## 🚀 How to Use in Your Repository

To use the `upload_sop.sh` script in another repository’s GitHub Actions workflow, follow these steps:

### 1️⃣ **Add the GitHub Actions Workflow**
Create a file in your repository at `.github/workflows/upload_sop.yml`:

```yaml
name: Upload Excel File to Qualer

on:
  pull_request:
    branches:
      - main

jobs:
  upload:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Checkout shared CI scripts
        uses: actions/checkout@v3
        with:
          repository: your-org/ci-scripts
          path: ci-scripts  # Store in a subfolder

      - name: Locate Changed Excel File
        id: changed-file
        uses: tj-actions/changed-files@v35
        with:
          files: '**/*.xlsm'

      - name: Ensure Only One File is Changed
        if: steps.changed-file.outputs.any_changed == 'true'
        run: |
          FILE_COUNT=$(echo "${{ steps.changed-file.outputs.all_changed_files }}" | wc -w)
          if [ "$FILE_COUNT" -ne 1 ]; then
            echo "❌ Error: More than one Excel file was changed. Only one file is allowed per PR."
            exit 1
          fi
          echo "MERGED_FILE=${{ steps.changed-file.outputs.all_changed_files }}" >> $GITHUB_ENV

      - name: Upload Excel File to Qualer
        if: steps.changed-file.outputs.any_changed == 'true'
        run: ./ci-scripts/upload_sop.sh
        env:
          QUALER_EMAIL: ${{ secrets.QUALER_EMAIL }}
          QUALER_PASSWORD: ${{ secrets.QUALER_PASSWORD }}
          SOP_ID: 2351  # Replace per repository
          MERGED_FILE: ${{ env.MERGED_FILE }}
```

### 2️⃣ **Store GitHub Secrets**
Go to **GitHub Repo → Settings → Secrets and variables → Actions** and add the following secrets:

| Secret Name       | Description                      |
|------------------|--------------------------------|
| `QUALER_EMAIL`   | Your Qualer login email       |
| `QUALER_PASSWORD`| Your Qualer password         |

### 3️⃣ **Push Changes & Open a Pull Request**
Once this workflow is added, it will automatically:
- Detect changed `.xlsm` files.  (TODO: Add other file types)
- Fetch the `upload_sop.sh` script from `ci-scripts`.
- Upload the changed file to Qualer.
- Block merging if the upload fails.

---

## 🔧 Updating the Script
Since all repositories pull `upload_sop.sh` dynamically from this repo, any updates made here will apply to all linked repositories **without requiring manual changes** in each repo.

To update the script:
1. Modify `upload_sop.sh` in `ci-scripts`.
2. Commit and push changes.
3. The new version will automatically be used by all repositories referencing it.

---

## ❓ Troubleshooting
- **Workflow Fails Due to Authentication?** Ensure `QUALER_EMAIL` and `QUALER_PASSWORD` are set as GitHub Secrets.
- **CSRF Token Extraction Issues?** If the authentication process changes, update the script accordingly.
- **No `.xlsm` File Changes Detected?** Confirm that the modified file types match the workflow’s `changed-files` filter.

---

## 🔍 Excel Reference Validation

The `check_excel_refs.py` script automatically validates Excel files for broken references before allowing PRs to be merged.

### What it checks:
- **#REF! errors**: Detects broken cell references in formulas
- **All worksheets**: Scans every sheet in the workbook
- **Formula preservation**: Optionally exports sheets with formulas intact

### How it works:
1. **Automatic Integration**: Runs as part of the pre-check workflow
2. **Blocking**: Prevents merge if any #REF! errors are found
3. **Detailed Reporting**: Shows exact location of each broken reference

### Manual Usage:
```bash
# Check a specific Excel file
python check_excel_refs.py /path/to/file.xlsx

# Or use environment variable
export EXCEL_FILE="/path/to/file.xlsx"
python check_excel_refs.py

# Export sheets with formulas for analysis
export EXPORT_SHEETS="true"
python check_excel_refs.py
```

### Output Example:
```
🔍 Checking MyFile.xlsx for #REF! errors...
❌ Found 2 #REF! errors:
  - Sheet 'Summary', Cell B5: =SUM(#REF!)
  - Sheet 'Data', Cell C10: =#REF!*2

❌ Please fix broken references before merging.
```

---

## 🏆 Benefits of This Approach
✅ **DRY (Don’t Repeat Yourself)** – One script for all repositories.
✅ **Instant Updates** – Change the script once, all repos benefit.
✅ **Secure** – Uses GitHub Secrets, no credentials in source code.
✅ **Prevents Bad Merges** – Ensures uploads succeed before merging.

---

## 👏 Contributing
If you need modifications or new scripts added, open a pull request with your proposed changes.

---

## 📝 License
This repository is for internal use within `Johnson-Gage-Inspection-Inc`. Ensure compliance with security policies before modifying shared scripts.

---

For any issues or questions, reach out to Jeff or open an issue in this repository. 🚀

