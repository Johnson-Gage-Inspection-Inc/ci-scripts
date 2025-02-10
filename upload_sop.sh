#!/bin/bash
set -e  # Exit on first error

# Run shared authentication & file preparation
source "$(dirname "$0")/auth_and_prepare.sh"

echo "✅ Pre-merge validation passed!"

# Get the current date in the format MM/DD/YYYY
current_date=$(date +"%m/%d/%Y")

echo "✅ Current date: $current_date"

# Ensure EXCEL_FILE is set
if [ -z "$EXCEL_FILE" ]; then
  echo "❌ EXCEL_FILE is not set. Exiting."
  exit 1
fi

# Ensure there's a file there
if [ ! -f "$EXCEL_FILE" ]; then
  echo "❌ File not found: $EXCEL_FILE"
  exit 1
fi

echo "ℹ️ Uploading file: $EXCEL_FILE"

status_code=$(curl -s -w "%{http_code}" -o tmp/upload_response.json "https://jgiquality.qualer.com/Sop/SaveSopFile" \
    -X POST \
    -b tmp/cookies.txt -c tmp/cookies.txt \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0" \
    -H "Accept: */*" \
    -H "X-Requested-With: XMLHttpRequest" \
    -H "Referer: https://jgiquality.qualer.com/Sop/Sop?sopId=$SOP_ID" \
    -F "documents=@\"$EXCEL_FILE\";type=application/vnd.ms-excel.sheet.macroEnabled.12" \
    -F "sopId=$SOP_ID" \
    -F "__RequestVerificationToken=$csrf_token_value") || echo "Curl failed with exit code $?"

cat tmp/upload_response.json

if [[ $status_code -ne 200 ]]; then
  echo "❌ Failed to upload the SOP file with status code $status_code"
  cat tmp/upload_response.json
  exit 1
fi

echo "✅ File upload attempted with status code: $status_code"

if grep -q '<h2>Object moved to <a href="/login?returnUrl=' tmp/upload_response.json; then
  echo "❌ Failed to upload SOP file."
  exit 2
fi

success=$(grep -o '"Success":true' tmp/upload_response.json)

# Print the result
cat tmp/upload_response.json

if [[ "$success" == "\"Success\":true" ]]; then
  echo "✅ SOP file uploaded successfully!"
else
  echo "❌ Upload failed"
  exit 3
fi

# Replace "\n" with a proper line break in DOC_DETAILS
DOC_DETAILS=$(echo "$DOC_DETAILS" | sed 's/\\n/\n/g')

status_code=$(curl 'https://jgiquality.qualer.com/Sop/Sop' \
  -X POST -b tmp/cookies.txt -c tmp/cookies.txt \
  -o tmp/update_response.json \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache, must-revalidate' \
  -H 'clientrequesttime: 2025-01-30T19:11:20' \
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'origin: https://jgiquality.qualer.com' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H "referer: https://jgiquality.qualer.com/Sop/Sop?sopId=$SOP_ID" \
  -H 'sec-ch-ua: "Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0' \
  -H 'x-requested-with: XMLHttpRequest' \
  --data-raw "SopId=$SOP_ID&SopTypeId=1544&AttachmentName=\"$EXCEL_FILE\"&SopTypeName=Approved+Software&title=$DOC_TITLE&code=$DOC_ID&EffectiveDate=$current_date&revision=$COMMIT_HASH&author=$AUTHOR_NAME&details=$DOC_DETAILS&__RequestVerificationToken=$csrf_token_value")

cat tmp/update_response.json
echo \

success=$(grep -o '"Success":true' tmp/update_response.json)

# Print the result
echo "🔍 Upload response:"
cat tmp/upload_response.json

echo \

if [[ "$success" == "\"Success\":true" ]]; then
  echo "✅ SOP file updated successfully!"
else
  echo "❌ Failed to update the SOP with status code $status_code"
  exit 4
fi