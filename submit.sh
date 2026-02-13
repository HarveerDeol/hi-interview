#!/usr/bin/env bash
set -euo pipefail

SUBMIT_URL="${INTERVIEW_SUBMIT_URL:-https://api.hifinance.ca/interview/submit}"

cd "$(dirname "$0")"

echo "=== Hi Interview Submission ==="
echo

read -rp "Your name: " name
read -rp "Your email: " email

echo
echo "In a few sentences, describe what you changed and why:"
read -rp "> " description

if [[ -z "$name" || -z "$email" || -z "$description" ]]; then
    echo "Error: All fields are required."
    exit 1
fi

echo
echo "Zipping project..."
tmpfile=$(mktemp /tmp/interview-submission-XXXXXX)
rm "$tmpfile"
tmpfile="$tmpfile.zip"
trap 'rm -f "$tmpfile"' EXIT

zip -r -q "$tmpfile" . -x "node_modules/*" "frontend/.next/*" "frontend/node_modules/*" "__pycache__/*" ".venv/*" "*.pyc"

echo "Uploading submission..."
response=$(curl -s -w "\n%{http_code}" -X POST "$SUBMIT_URL" \
    -F "file=@$tmpfile" \
    -F "name=$name" \
    -F "email=$email" \
    -F "description=$description")

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [[ "$http_code" == "200" ]]; then
    echo
    echo "Submission uploaded successfully! Thanks, $name."
else
    echo
    echo "Submission failed (HTTP $http_code)."
    echo "$body"
    exit 1
fi
