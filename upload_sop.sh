#!/bin/bash

# Ensure script stops on first failure
set -e

# Load environment variables from .env file
if [[ -f .env ]]; then
    export $(grep -v '^#' .env | xargs)
fi

# Ensure necessary environment variables are set
if [[ -z "$MERGED_FILE" ]]; then
    echo "MERGED_FILE environment variable is not set. Exiting..."
    exit 1
fi

if [[ -z "$SOP_ID" ]]; then
    echo "SOP_ID environment variable is not set. Exiting..."
    exit 2
fi

# Get the login page to set cookies
curl -s -c cookies.txt 'https://jgiquality.qualer.com/login' -o /dev/null || exit 3

# Extract CSRF token
csrf_token_name=$(awk '$6 ~ /^__RequestVerificationToken_/ {print $6}' cookies.txt | head -1)
csrf_token_value=$(awk -v token="$csrf_token_name" '$6 == token {print $NF}' cookies.txt)

if [[ -z "$csrf_token_name" || -z "$csrf_token_value" ]]; then
  echo "Failed to extract CSRF token from cookies."
  exit 4
fi

echo "Extracted CSRF Token Name: $csrf_token_name"
echo "Extracted CSRF Token Value: $csrf_token_value"

# Authenticate
status_code=$(curl -s -o login_response.html -w "%{http_code}" \
    'https://jgiquality.qualer.com/login?returnUrl=%2FSop%2FSops_Read' \
    -b cookies.txt -c cookies.txt -X POST \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-raw "Email=$QUALER_EMAIL&Password=$QUALER_PASSWORD&$csrf_token_name=$csrf_token_value")

if [[ $status_code -ne 302 ]]; then
  echo "Authentication failed with status code $status_code"
  exit 5
fi

echo "Authentication succeeded (status: $status_code)"

# Verify redirect
if ! grep -q '<h2>Object moved to <a href="/Sop/Sops_Read">here</a>.</h2>' login_response.html; then
  echo "Unexpected response after login."
  exit 6
fi

echo "Login success confirmed."

# Rename file with date suffix
FILE_PATH="$MERGED_FILE"

if [[ ! -f "$FILE_PATH" ]]; then
  echo "Error: File not found: $FILE_PATH"
  exit 7
fi

FILE_DIR=$(dirname "$FILE_PATH")
FILE_NAME=$(basename "$FILE_PATH")
FILE_BASE="${FILE_NAME%.*}"
FILE_EXT="${FILE_NAME##*.}"
TODAY=$(date +%Y-%m-%d)
NEW_FILE_NAME="${FILE_BASE}_${TODAY}.${FILE_EXT}"
NEW_FILE_PATH="${FILE_DIR}/${NEW_FILE_NAME}"

mv "$FILE_PATH" "$NEW_FILE_PATH" || exit 8
echo "File renamed to: $NEW_FILE_PATH"

# Step 5: Update the CSRF token by making a request to the SOP page
status_code=$(curl -s -w "%{http_code}" "https://jgiquality.qualer.com/Sop/Sop?sopId=$SOP_ID" \
    -X GET \
    -b cookies.txt -c cookies.txt \
    -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0' \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
    -H 'Connection: keep-alive' \
    -o sop_page.html)

if [[ $status_code -ne 200 ]]; then
    echo "Failed to update CSRF token with status code $status_code"
    exit 9
fi

echo "CSRF token updated successfully (status: $status_code)"

# Extract CSRF token for file upload
csrf_token_value=$(awk '$6 ~ /^__RequestVerificationToken_/ {print $NF}' cookies.txt)

if [[ -z "$csrf_token_value" ]]; then
    echo "❌ Error: Failed to extract CSRF token for file upload."
    cat cookies.txt  # Debugging info
    exit 10
fi

status_code=$(curl -s -w "%{http_code}" -o upload_response.json "https://jgiquality.qualer.com/Sop/SaveSopFile" \
    -X POST \
    -b cookies.txt -c cookies.txt \
    -H 'Connection: keep-alive' \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0" \
    -H "Accept: application/json, text/javascript, */*; q=0.01" \
    -H "X-Requested-With: XMLHttpRequest" \
    -H "Content-Type: multipart/form-data" \
    -H "Referer: https://jgiquality.qualer.com/Sop/Sop?sopId=$SOP_ID" \
    -F "Documents=@$NEW_FILE_PATH" \
    -F "sopId=$SOP_ID" \
    -F "__RequestVerificationToken=$csrf_token_value")

if [[ $status_code -ne 200 ]]; then
    echo "Failed to upload the SOP file with status code $status_code"
    exit 11
fi

if grep -q '<h2>Object moved to <a href="/login?returnUrl=' upload_response.json; then
    echo "Failed to upload SOP file."
    exit 12
fi

echo "SOP file uploaded successfully"

success=$(grep -o '"Success":true' upload_response.json)

# Print the result
cat upload_response.json

if [[ "$success" == "\"Success\":true" ]]; then
    echo "Upload succeeded"
else
    echo "Upload failed"
    exit 13
fi
