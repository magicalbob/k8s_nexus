#!/usr/bin/env python3
import os
import requests
import json

def create_roles():
    # Get Nexus username and password from environment variables
    username = os.environ.get('NEXUS_USERNAME')
    password = os.environ.get('NEXUS_PASSWORD')
    nexus_host = os.environ.get('NEXUS_HOST')
    json_file = os.environ.get('NEXUS_ROLES')

    # Read the JSON file
    with open(json_file, 'r') as f:
        roles = json.load(f)

    # Iterate over the roles and create them using the Nexus API
    for role in roles:
        role_name = role['name']
        endpoint = f"https://{nexus_host}/service/rest/v1/security/roles"
        headers = {
            'Content-Type': 'application/json'
        }
        auth = (username, password)
        # Check if the role already exists
        response = requests.get(endpoint, auth=auth)
        if response.status_code == 200:
            print(f"Role '{role_name}' already exists.")
            continue # Skip creating the role
        # Role doesn't exist, create it
        response = requests.post(endpoint, headers=headers, json=role, auth=auth)
        if response.status_code >= 200 and response.status_code <= 204:
            print(f"Role '{role_name}' created successfully.")
        else:
            print(f"Failed to create role '{role_name}'. Status Code: {response.status_code}, Error: {response.text}")

# Usage
create_roles()
