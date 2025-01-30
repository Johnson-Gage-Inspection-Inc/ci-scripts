#!/bin/bash
set -e  # Exit on first error

# Run shared authentication & file preparation
source "$(dirname "$0")/auth_and_prepare.sh"

# Step 6: Upload the SOP file
status_code=$(curl -s -w "%{http_code}" -o upload_response.json \
    "https://jgiquality.qualer.com/Sop/SaveSopFile" \
    -X POST -b cookies.txt -c cookies.txt \
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
    echo "❌ Failed to upload the SOP file with status code $status_code"
    exit 1
fi

if grep -q '<h2>Object moved to <a href="/login?returnUrl=' upload_response.json; then
    echo "❌ Failed to upload SOP file."
    exit 2
fi

success=$(grep -o '"Success":true' upload_response.json)

# Print the result
cat upload_response.json

if [[ "$success" == "\"Success\":true" ]]; then
    echo "✅ SOP file uploaded successfully!"
else
    echo "❌ Upload failed"
    exit 3
fi
