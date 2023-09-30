#!/bin/bash

# Nexus Repository Manager URL
nexus_url="https://${NEXUS_HOST}/repository/repo-name"

# Number of concurrent requests
concurrent_requests=10

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

