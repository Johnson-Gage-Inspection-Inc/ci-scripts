import os
import requests
import re
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
QUALER_EMAIL = os.getenv("QUALER_EMAIL")
QUALER_PASSWORD = os.getenv("QUALER_PASSWORD")

if not QUALER_EMAIL or not QUALER_PASSWORD:
    print("Missing credentials in .env file. Exiting...")
    exit(1)

print(f"Using Email: {QUALER_EMAIL}")
print("Using Password: [HIDDEN]")

# Create a session to maintain cookies
session = requests.Session()

# Step 1: Get the login page to set cookies
login_url = "https://jgiquality.qualer.com/login"
session.get(login_url)

# Step 2: Extract CSRF token from cookies
csrf_token_name = None
csrf_token_value = None
for cookie in session.cookies:
    if "__RequestVerificationToken_" in cookie.name:
        csrf_token_name = cookie.name
        csrf_token_value = cookie.value
        break

if not csrf_token_name or not csrf_token_value:
    print("Failed to extract CSRF token from cookies.")
    exit(1)

print(f"Extracted CSRF Token Name: {csrf_token_name}")
print(f"Extracted CSRF Token Value: {csrf_token_value}")

# Step 3: Authenticate
login_data = {
    "Email": QUALER_EMAIL,
    "Password": QUALER_PASSWORD,
    csrf_token_name: csrf_token_value,
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
    "Content-Type": "application/x-www-form-urlencoded",
}

response = session.post(login_url + "?returnUrl=%2FSop%2FSops_Read", data=login_data, headers=headers)

if response.status_code != 302:
    print(f"Authentication failed with status code {response.status_code}")
    exit(2)
else:
    print("Authentication succeeded")

# Verify redirect
if "Object moved to <a href=\"/Sop/Sops_Read\"" in response.text:
    print("Login success confirmed.")
else:
    print("Unexpected response after login.")

# Define file path
FILE_PATH = os.path.abspath("../pth/Form_3018_Rockwell_12-19-2024.xlsm")
print(f"File: {FILE_PATH}")
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    exit(3)

# Step 4: Update CSRF token by requesting the SOP page
sop_url = "https://jgiquality.qualer.com/Sop/Sop?sopId=2351"
sop_response = session.get(sop_url, headers=headers)

if sop_response.status_code != 200:
    print(f"Failed to update CSRF token with status code {sop_response.status_code}")
    exit(4)
else:
    print("CSRF token updated successfully")

if "Object moved to <a href=\"/login?returnUrl=" in sop_response.text:
    print("Unexpected response after updating CSRF token.")
else:
    print("CSRF token updated successfully.")

# Extract latest CSRF token before upload
csrf_token_match = re.search(r'<input name="__RequestVerificationToken" type="hidden" value="([^"]+)"', sop_response.text)
csrf_token_value = csrf_token_match.group(1) if csrf_token_match else None

if not csrf_token_value:
    print("Failed to extract new CSRF token.")
    exit(5)

# Step 5: Upload the SOP file
upload_url = "https://jgiquality.qualer.com/Sop/SaveSopFile"
files = {"Documents": open(FILE_PATH, "rb")}
data = {
    "sopId": "2351",
    "__RequestVerificationToken": csrf_token_value,
}

upload_response = session.post(upload_url, files=files, data=data, headers=headers)

if upload_response.status_code != 200:
    print(f"Failed to upload the SOP file with status code {upload_response.status_code}")
    exit(6)

upload_json = upload_response.json()

if upload_json.get("Success"):
    print("Upload succeeded")
else:
    print("Upload failed")
    print(json.dumps(upload_json, indent=4))
