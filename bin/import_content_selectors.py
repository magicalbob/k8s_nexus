#!/usr/bin/env python3
import os
import requests
import json

def create_content_selectors():
    # Get Nexus username and password from environment variables
    username = os.environ.get('NEXUS_USERNAME')
    password = os.environ.get('NEXUS_PASSWORD')
    nexus_host = os.environ.get('NEXUS_HOST')
    json_file = os.environ.get('NEXUS_SELECTORS')

    # Read the JSON file
    with open(json_file, 'r') as f:
        selectors = json.load(f)

    # Iterate over the selectors and create them using the Nexus API
    for selector in selectors:
        endpoint = f"https://{nexus_host}/service/rest/v1/security/content-selectors"
        headers = {
            'Content-Type': 'application/json'
        }
        auth = (username, password)
        response = requests.post(endpoint, headers=headers, json=selector, auth=auth)
        if response.status_code >= 201 and response.status_code <= 204:
            print(f"Content selector '{selector['name']}' created successfully.")
        else:
            print(f"Failed to create content selector '{selector['name']}'. Status Code: {response.status_code}, Error: {response.text}")

# Usage
create_content_selectors()
