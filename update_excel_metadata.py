import os
import win32com.client

# Get file path from environment variable
file_path = os.getenv("EXCEL_FILE")
if not file_path or not os.path.exists(file_path):
    print(f"❌ ERROR: File not found: {file_path}")
    exit(1)

# Get metadata properties
shell = win32com.client.Dispatch("Shell.Application")
folder = shell.Namespace(os.path.dirname(file_path))
file = folder.ParseName(os.path.basename(file_path))

# Update metadata fields
if not (commit_hash := os.getenv("COMMIT_HASH")):
    print("❌ ERROR: Missing environment variable: COMMIT_HASH")
    exit(1)
if not (release_tag := os.getenv("RELEASE_TAG")):
    print("❌ ERROR: Missing environment variable: RELEASE_TAG")
    exit(1)

file.ExtendedProperty("Title", f"Version {release_tag}")
file.ExtendedProperty("Keywords", commit_hash)
file.ExtendedProperty("Company", "Johnson Gage & Inspection")

print(f"✅ Updated metadata for {file_path}")
