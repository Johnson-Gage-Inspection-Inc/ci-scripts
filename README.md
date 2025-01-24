# CI Scripts Repository

This repository serves as a central location for shared CI/CD scripts that can be used across multiple repositories in the organization. The primary script, `upload_sop.sh`, automates the process of uploading Excel SOP files to Qualer.

## 📌 Features
- **Centralized Management**: Update once, apply changes across all repositories.
- **Seamless Integration**: Easily referenced in GitHub Actions workflows.
- **Secure Authentication**: Uses GitHub Secrets for storing credentials.
- **Automated SOP File Upload**: Detects changes in Excel files and uploads them to Qualer.

---

## 📂 Repository Structure
```
ci-scripts/
│── upload_sop.sh   # Main script for uploading SOP files to Qualer
│── README.md       # Documentation
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
          repository: Johnson-Gage-Inspection-Inc/ci-scripts
          path: ci-scripts  # Store in a subfolder

      - name: Locate Changed Excel Files
        id: changed-files
        uses: tj-actions/changed-files@v35
        with:
          files: '**/*.xlsm'

      - name: Set Environment Variables
        if: steps.changed-files.outputs.any_changed == 'true'
        run: echo "MERGED_FILE=$(realpath ${{ steps.changed-files.outputs.all_changed_files }})" >> $GITHUB_ENV

      - name: Upload Excel File to Qualer
        if: steps.changed-files.outputs.any_changed == 'true'
        run: ./ci-scripts/upload_sop.sh
        env:
          QUALER_EMAIL: ${{ secrets.QUALER_EMAIL }}
          QUALER_PASSWORD: ${{ secrets.QUALER_PASSWORD }}
          SOP_ID: 2351  # Replace per repository
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

