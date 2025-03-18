import pythoncom
import win32com.client


def update_excel_metadata(excel_file, commit_hash, release_tag):
    try:
        # Try to create an instance of the Excel application
        excel_app = win32com.client.Dispatch("Excel.Application")
        print("Successfully created Excel application instance.")

        # Open the Excel file
        w = excel_app.Workbooks.Open(excel_file)
        print(f"Opened Excel file: {excel_file}")

        # Update metadata
        w.CustomDocumentProperties("Revision").Value = commit_hash
        w.CustomDocumentProperties("Version").Value = release_tag
        w.CustomDocumentProperties("Company").Value = "Johnson Gage & Inspection, Inc"
        w.Save()
        w.Close()

        print("Updated Excel metadata successfully.")
    except pythoncom.com_error as e:
        print(f"COM error: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(2)
    finally:
        excel_app.Quit()


if __name__ == "__main__":
    import os
    excel_file = os.getenv("EXCEL_FILE")
    commit_hash = os.getenv("COMMIT_HASH")
    release_tag = os.getenv("RELEASE_TAG")

    if excel_file and commit_hash and release_tag:
        update_excel_metadata(excel_file, commit_hash, release_tag)
    else:
        print("Missing environment variables: EXCEL_FILE, COMMIT_HASH, or RELEASE_TAG")
