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

    # Iterate over the selectors and create/update them using the Nexus API
    for selector in selectors:
        endpoint = f"https://{nexus_host}/service/rest/v1/security/content-selectors"
        headers = {
            'Content-Type': 'application/json'
        }
        auth = (username, password)

        # Check if the content selector already exists
        selector_name = selector['name']
        existing_selector = get_existing_content_selector(endpoint, headers, auth, selector_name)
        if existing_selector:
            print(f"Content selector '{selector_name}' already exists.")
        else:
            response = requests.post(endpoint, headers=headers, json=selector, auth=auth)
            if response.status_code >= 201 and response.status_code <= 204:
                print(f"Content selector '{selector_name}' created successfully.")
            else:
                print(f"Failed to create content selector '{selector_name}'. Status Code: {response.status_code}, Error: {response.text}")

def get_existing_content_selector(endpoint, headers, auth, selector_name):
    response = requests.get(endpoint, headers=headers, auth=auth)
    if response.status_code == 200:
        selectors = response.json()
        for selector in selectors:
            if selector['name'] == selector_name:
                return selector
    return None

# Usage
create_content_selectors()

