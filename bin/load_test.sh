#!/usr/bin/env bash

# Env vars required
ENV_VAR_REQ=$(cat <<-EOM
You must provide the following environment variables:
  - NEXUS_HOST      : hostname of Nexus
  - NEXUS_USERNAME  : Nexus user to use
  - NEXUS_PASSWORD  : password for that Nexus user
EOM
)

# Ensure correct env vars have been supplied

if [ -z "$NEXUS_HOST" ]
then
  echo "$ENV_VAR_REQ"
  exit 1
fi

if [ -z "$NEXUS_USERNAME" ]
then
  echo "$ENV_VAR_REQ"
  exit 2
fi

if [ -z "$NEXUS_PASSWORD" ]
then
  echo "$ENV_VAR_REQ"
  exit 3
fi

# Define usage message
usage() {
  echo "Usage: $0 -c <concurrent_requests>" >&2
  exit 1
}

# Parse command-line options
while getopts ":c:" opt; do
  case $opt in
    c)
      concurrent_requests="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      usage
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      usage
      ;;
  esac
done

# Check if concurrent_requests is provided
if [ -z "$concurrent_requests" ]; then
  echo "Error: Missing mandatory argument -c <concurrent_requests>" >&2
  usage
fi
 
# Nexus Repository Manager URL
nexus_url="https://${NEXUS_HOST}/repository/repo-name"

# Nexus username and password
username="${NEXUS_USERNAME}"
password="${NEXUS_PASSWORD}"

# Function to upload a file to Nexus
upload_file() {
  local file_path="$1"
  local target_path="$2"
  curl -u "${username}:${password}" -X PUT "${nexus_url}/${target_path}" --upload-file "${file_path}"
}

# Function to download a file from Nexus
download_file() {
  local target_path="$1"
  curl -u "${username}:${password}" -OJ "${nexus_url}/${target_path}"
}

# Perform upload and download tests concurrently
for ((i = 1; i <= concurrent_requests; i++)); do
  (
    # Generate a unique filename for each request
    file_name="testfile_${i}.txt"
    file_content="This is test file ${i}."
    echo "${file_content}" > "${file_name}"

    # Upload a file to Nexus
    upload_file "${file_name}" "uploads/${file_name}"

    # Download the uploaded file from Nexus
    download_file "uploads/${file_name}"

    # Clean up the local file
    rm "${file_name}"
  ) &
done

# Wait for all concurrent requests to finish
wait

echo "Load test completed!"

