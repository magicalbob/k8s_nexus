#!/bin/bash

# Define usage message
usage() {
  echo "Usage: $0 -c <concurrent_requests>" >&2
  exit 1
}

# Initialize variables
concurrent_requests=""
nexus_host="$NEXUS_HOST"
nexus_username="$NEXUS_USERNAME"
nexus_password="$NEXUS_PASSWORD"
success_count=0
failure_count=0

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

# Check if NEXUS_HOST environment variable is provided
if [ -z "$nexus_host" ]; then
  echo "Error: NEXUS_HOST environment variable is not set. Please provide a value for NEXUS_HOST." >&2
  usage
fi

# Check if other required environment variables are provided
if [ -z "$nexus_username" ] || [ -z "$nexus_password" ]; then
  echo "Error: NEXUS_USERNAME and/or NEXUS_PASSWORD environment variables are not set. Please provide values for both." >&2
  usage
fi

# Function to perform a test request
perform_test_request() {
  local response_code
  response_code=$(curl -s -o /dev/null -w "%{http_code}" --user "$nexus_username:$nexus_password" "https://${nexus_host}/your-api-endpoint")

  if [ "$response_code" == "200" ]; then
    echo "Request successful (HTTP $response_code)"
    success_count=$((success_count + 1))
  else
    echo "Request failed (HTTP $response_code)"
    failure_count=$((failure_count + 1))
  fi
}

# Run concurrent requests
for ((i = 1; i <= concurrent_requests; i++)); do
  perform_test_request
done

# Display summary
echo "Summary:"
echo "Successful requests: $success_count"
echo "Failed requests: $failure_count"

# Check if any requests failed and exit with an appropriate message
if [ "$failure_count" -gt 0 ]; then
  echo "Load test encountered failures. Please investigate."
  exit 1
fi

echo "Load test completed successfully."

