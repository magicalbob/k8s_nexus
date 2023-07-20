import os
import requests
import json

def create_content_selector_privileges():
    # Get Nexus username and password from environment variables
    username = os.environ.get('NEXUS_USERNAME')
    password = os.environ.get('NEXUS_PASSWORD')
    nexus_host = os.environ.get('NEXUS_HOST')
    json_file = os.environ.get('NEXUS_SELECTORS')

    # Read the JSON file
    with open(json_file, 'r') as f:
        privileges = json.load(f)

    # Iterate over the privileges and create/update them using the Nexus API
    for privilege in privileges:
        endpoint = f"https://{nexus_host}/service/rest/v1/security/privileges/repository-content-selector"
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(endpoint, headers=headers, json=privilege, auth=(username, password))
        if response.status_code == 201:
            print(f"Privilege '{privilege['name']}' created successfully.")
        elif response.status_code == 400:
            error_message = response.json().get('message')
            if error_message and f"Privilege '{privilege['name']}' already exists" in error_message:
                print(f"Privilege '{privilege['name']}' already exists.")
            else:
                print(f"Failed to create privilege '{privilege['name']}'. Error: {response.text}")
        else:
            print(f"Failed to create privilege '{privilege['name']}'. Error: {response.text}")

# Usage
create_content_selector_privileges()

