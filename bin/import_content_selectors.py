#!/usr/bin/env python3
import os
import requests
import json

def create_content_selectors(json_file, nexus_url):
    # Read the JSON file
    with open(json_file, 'r') as f:
        selectors = json.load(f)

    # Get Nexus username and password from environment variables
    username = os.environ.get('NEXUS_USERNAME')
    password = os.environ.get('NEXUS_PASSWORD')

    # Iterate over the selectors and create them using the Nexus API
    for selector in selectors:
        endpoint = f"{nexus_url}/service/rest/v1/security/content-selectors"
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
json_file = 'selectors.json'
nexus_url = 'https://nexus.ellisbs.co.uk'
create_content_selectors(json_file, nexus_url)

