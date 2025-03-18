import os
import uuid
import win32com.client

original_file = os.getenv("EXCEL_FILE", "UNKNOWN")
if not os.path.exists(original_file):
    print(f"ERROR: File not found: {original_file}")
    exit(1)

# Ensure Temp directory exists
temp_dir = os.getenv("RUNNER_TEMP", "C:\\Temp")
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Generate unique filename
modified_file = os.path.join(temp_dir, f"{uuid.uuid4().hex}.xltm")

# Read commit hash and tag from environment
commit_hash = os.getenv("COMMIT_HASH", "UNKNOWN")
tag = os.getenv("RELEASE_TAG", "UNKNOWN")
company_name = "Johnson Gage & Inspection"

# Open Excel
excel = win32com.client.Dispatch("Excel.Application")
excel.DisplayAlerts = False

try:
    workbook = excel.Workbooks.Open(original_file)

    # Update metadata
    workbook.BuiltinDocumentProperties("Title").Value = f"Version {tag}"
    workbook.BuiltinDocumentProperties("Keywords").Value = commit_hash
    workbook.BuiltinDocumentProperties("Company").Value = company_name

    workbook.Save()
    workbook.Close(SaveChanges=True)
    excel.Quit()

    excel = win32com.client.Dispatch("Excel.Application")
    workbook = excel.Workbooks.Open(original_file)

    workbook.SaveAs(modified_file, FileFormat=workbook.FileFormat)

    workbook.Close(SaveChanges=True)
    excel.Quit()

    print(
        f"✅ Updated Excel Metadata in {modified_file}:",
        f"Version={tag}, Tags={commit_hash}, Company={company_name}"
    )

    # Output new file path
    with open(os.environ["GITHUB_ENV"], "a") as f:
        f.write(f"EXCEL_FILE={modified_file}\n")

    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"EXCEL_FILE={modified_file}\n")

except Exception as e:
    print(f"❌ Error updating file: {e}")
    workbook.Close(SaveChanges=False)
    excel.Quit()
