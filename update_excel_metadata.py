import os
import pythoncom
import win32com.client


def update_excel_metadata(excel_file, commit_hash, release_tag):
    if not os.path.exists(excel_file):
        print(f"ERROR: Excel file not found: {excel_file}")
        exit(1)

    try:
        # Create an instance of Excel application
        excel_app = win32com.client.Dispatch("Excel.Application")
        excel_app.Visible = False  # Run in background
        print("✅ Successfully created Excel application instance.")

        # Open the Excel file
        workbook = excel_app.Workbooks.Open(excel_file)
        print(f"📂 Opened Excel file: {excel_file}")

        # Update Builtin metadata (safer than CustomDocumentProperties)
        workbook.BuiltinDocumentProperties("Version").Value = release_tag
        workbook.BuiltinDocumentProperties("Keywords").Value = commit_hash
        workbook.BuiltinDocumentProperties("Company").Value = "JGI"

        # Save and close the workbook
        workbook.Save()
        workbook.Close(SaveChanges=True)

        print("✅ Updated Excel metadata successfully.")

    except pythoncom.com_error as e:
        print(f"COM error: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(2)
    finally:
        try:
            excel_app.Quit()
        except Exception:
            pass  # Avoid exception if excel_app was never initialized


if __name__ == "__main__":
    excel_file = os.getenv("EXCEL_FILE")
    commit_hash = os.getenv("COMMIT_HASH")
    release_tag = os.getenv("RELEASE_TAG")

    # Validate environment variables
    variables = ["EXCEL_FILE", "COMMIT_HASH", "RELEASE_TAG"]
    missing_vars = [var for var in variables if not os.getenv(var)]
    if missing_vars:
        for var in missing_vars:
            print(f"ERROR: Environment variable {var} is not set.")
        exit(3)

    update_excel_metadata(excel_file, commit_hash, release_tag)
