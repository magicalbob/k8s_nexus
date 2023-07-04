import os
import requests
import json

def create_content_selector_privileges(json_file, nexus_url):
    # Get Nexus username and password from environment variables
    username = os.environ.get('NEXUS_USERNAME')
    password = os.environ.get('NEXUS_PASSWORD')

    # Read the JSON file
    with open(json_file, 'r') as f:
        privileges = json.load(f)

    # Iterate over the privileges and create them using the Nexus API
    for privilege in privileges:
        endpoint = f"{nexus_url}/service/rest/v1/security/privileges/repository-content-selector"
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(endpoint, headers=headers, json=privilege, auth=(username, password))
        print(response.status_code)
        if response.status_code >= 201 and response.status_code <= 204:
            print(f"Privilege '{privilege['name']}' created successfully.")
        else:
            print(f"Failed to create privilege '{privilege['name']}'. Error: {response.text}")

# Usage
json_file = 'privileges.json'
nexus_url = 'https://nexus.ellisbs.co.uk'
create_content_selector_privileges(json_file, nexus_url)

