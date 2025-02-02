#!/bin/bash
set -e  # Exit on first error

# Load environment variables
set -o allexport
source .env
set +o allexport


# Ensure necessary environment variables are set
required_vars=("EXCEL_FILE" "SOP_ID" "AUTHOR_NAME" "COMMIT_HASH" "DOC_ID" "DOC_TITLE" "DOC_DETAILS")

for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        echo "❌ $var environment variable is not set. Exiting..."
        exit 1
    fi
done

mkdir -p tmp

# Step 1: Get the login page to set cookies
curl -s -c tmp/cookies.txt 'https://jgiquality.qualer.com/login' -o /dev/null || exit 2

# Step 2: Extract CSRF token
csrf_token_name=$(awk '$6 ~ /^__RequestVerificationToken_/ {print $6}' tmp/cookies.txt | head -1)
csrf_token_value=$(awk -v token="$csrf_token_name" '$6 == token {print $NF}' tmp/cookies.txt)

if [[ -z "$csrf_token_name" || -z "$csrf_token_value" ]]; then
  echo "❌ Failed to extract CSRF token from cookies."
  exit 3
fi

echo "✅ Extracted CSRF Token Name: $csrf_token_name"
echo "✅ Extracted CSRF Token Value: $csrf_token_value"

# Step 3: Authenticate
status_code=$(curl -s -o tmp/login_response.html -w "%{http_code}" \
    'https://jgiquality.qualer.com/login?returnUrl=%2FSop%2FSops_Read' \
    -b tmp/cookies.txt -c tmp/cookies.txt -X POST \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-raw "Email=$QUALER_EMAIL&Password=$QUALER_PASSWORD&$csrf_token_name=$csrf_token_value")

if [[ $status_code -ne 302 ]]; then
  echo "❌ Authentication failed with status code $status_code"
  exit 4
fi

echo "✅ Authentication succeeded (status: $status_code)"

# Verify redirect
if ! grep -q '<h2>Object moved to <a href="/Sop/Sops_Read">here</a>.</h2>' tmp/login_response.html; then
  echo "❌ Unexpected response after login."
  exit 5
fi

echo "✅ Login success confirmed."

if [[ ! -f "$EXCEL_FILE" ]]; then
  echo "❌ Error: File not found: $EXCEL_FILE"
  exit 6
fi

# Step 4: Update the CSRF token by making a request to the SOP page
status_code=$(curl -s -w "%{http_code}" -o tmp/sop_page.html \
    "https://jgiquality.qualer.com/Sop/Sop?sopId=$SOP_ID" \
    -X GET -b tmp/cookies.txt -c tmp/cookies.txt \
    -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0' \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
    -H 'Connection: keep-alive')

if [[ $status_code -ne 200 ]]; then
    echo "Failed to update CSRF token with status code $status_code"
    exit 8
fi

# Step 5: Verify the response
if grep -q '<h2>Object moved to <a href="/login?returnUrl=' tmp/sop_page.html; then
    echo "Unexpected response after updating CSRF token."
else
    # Extract CSRF token for file upload
    csrf_token_value=$(grep -oP '(?<=<input name="__RequestVerificationToken" type="hidden" value=")[^"]*' tmp/sop_page.html)
    echo "✅ CSRF token updated successfully (status: $status_code)"
fi

if [[ -z "$csrf_token_value" ]]; then
  echo "❌ Error: Failed to extract CSRF token for file upload."
  exit 9
fi

# Export variables for the upload script
export csrf_token_value
