#!/bin/bash

# Load environment variables from .env file
if [[ -f .env ]]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Missing .env file. Exiting..."
    exit 0
fi

# Debug: Print loaded credentials (REMOVE AFTER DEBUGGING)
echo "Using Email: $QUALER_EMAIL"
echo "Using Password: [HIDDEN]"

# Step 1: Get the login page to set cookies
curl -s -c cookies.txt 'https://jgiquality.qualer.com/login' -o /dev/null

# Step 2: Extract CSRF token name and value dynamically
csrf_token_name=$(awk '$6 ~ /^__RequestVerificationToken_/ {print $6}' cookies.txt | head -1)
csrf_token_value=$(awk -v token="$csrf_token_name" '$6 == token {print $NF}' cookies.txt)

if [[ -z "$csrf_token_name" || -z "$csrf_token_value" ]]; then
  echo "Failed to extract CSRF token from cookies."
  exit 1
fi

echo "Extracted CSRF Token Name: $csrf_token_name"
echo "Extracted CSRF Token Value: $csrf_token_value"

# Second request to authenticate
status_code=$(curl -s -o tmp/login_response.html -w "%{http_code}" 'https://jgiquality.qualer.com/login?returnUrl=%2FSop%2FSops_Read' \
    -b cookies.txt -c cookies.txt \
    -X POST \
    -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0' \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
    -H 'Accept-Language: en-US,en;q=0.5' \
    -H 'Accept-Encoding: gzip, deflate, br, zstd' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -H 'Origin: https://jgiquality.qualer.com' \
    -H 'Connection: keep-alive' \
    -H 'Referer: https://jgiquality.qualer.com/login' \
    -H 'Upgrade-Insecure-Requests: 1' \
    -H 'Sec-Fetch-Dest: document' \
    -H 'Sec-Fetch-Mode: navigate' \
    -H 'Sec-Fetch-Site: same-origin' \
    -H 'Sec-Fetch-User: ?1' \
    -H 'Priority: u=0, i' \
    --data-raw "Email=jhall%40jgiquality.com&Password=PoorGary1%21&$csrf_token_name=$csrf_token_value")

if [[ $status_code -ne 302 ]]; then
  echo "Authentication failed with status code $status_code"
  exit 2
else
  echo "Authentication succeeded (status: $status_code)"
fi

# Verify redirect
if grep -q '<h2>Object moved to <a href="/Sop/Sops_Read">here</a>.</h2>' login_response.html; then
  echo "Login success confirmed."
else
  echo "Unexpected response after login."
fi

# Define file path
FILE_PATH="$(realpath "C:\Users\JGI\Downloads\Form_3018_Rockwell.xlsm")"
echo "File : $FILE_PATH"
# Ensure the file exists before proceeding
if [[ ! -f "$FILE_PATH" ]]; then
  echo "File not found: $FILE_PATH"
  exit 3
fi

# Step 4: Update the CSRF token by making a request to the SOP page
status_code=$(curl -s -w "%{http_code}" 'https://jgiquality.qualer.com/Sop/Sop?sopId=2351' \
    -X GET \
    -b cookies.txt -c cookies.txt \
    -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0' \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
    -H 'Accept-Language: en-US,en;q=0.5' \
    -H 'Accept-Encoding: gzip, deflate, br, zstd' \
    -H 'Connection: keep-alive' \
    -H 'Referer: https://jgiquality.qualer.com/documents' \
    -H 'Upgrade-Insecure-Requests: 1' \
    -H 'Sec-Fetch-Dest: document' \
    -H 'Sec-Fetch-Mode: navigate' \
    -H 'Sec-Fetch-Site: same-origin' \
    -H 'Sec-Fetch-User: ?1' \
    -H 'TE: trailers' \
    -o tmp/sop_page.html)

if [[ $status_code -ne 200 ]]; then
    echo "Failed to update CSRF token with status code $status_code"
    exit 4
else
    echo "CSRF token updated successfully (status: $status_code)"
fi

# Step 5: Verify the response
if grep -q '<h2>Object moved to <a href="/login?returnUrl=' sop_page.html; then
  echo "Unexpected response after updating CSRF token."
else
    echo "CSRF token updated successfully."
fi

# Extract latest CSRF token before upload
csrf_token_name=$(awk '$6 ~ /^__RequestVerificationToken_/ {print $6}' cookies.txt | head -1)
csrf_token_value=$(grep -oP '(?<=<input name="__RequestVerificationToken" type="hidden" value=")[^"]*' sop_page.html)

status_code=$(curl -s -w "%{http_code}" -o tmp/upload_response.json "https://jgiquality.qualer.com/Sop/SaveSopFile" \
    -X POST \
    -b cookies.txt -c cookies.txt \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0" \
    -H "Accept: application/json, text/javascript, */*; q=0.01" \
    -H "X-Requested-With: XMLHttpRequest" \
    -H "Content-Type: multipart/form-data" \
    -H "Referer: https://jgiquality.qualer.com/Sop/Sop?sopId=2351" \
    -F "Documents=@$FILE_PATH" \
    -F "sopId=2351" \
    -F "__RequestVerificationToken=$csrf_token_value")


if [[ $status_code -ne 200 ]]; then
  echo "❌ Failed to upload the SOP file with status code $status_code"
  cat upload_response.json
  exit 1
fi

echo "✅ File upload attempted with status code: $status_code"

if grep -q '<h2>Object moved to <a href="/login?returnUrl=' upload_response.json; then
  echo "❌ Failed to upload SOP file."
  exit 2
fi

success=$(grep -o '"Success":true' tmp/upload_response.json)

# Print the result
cat upload_response.json

if [[ "$success" == "\"Success\":true" ]]; then
  echo "✅ SOP file uploaded successfully!"
else
  echo "❌ Upload failed"
  exit 3
fi