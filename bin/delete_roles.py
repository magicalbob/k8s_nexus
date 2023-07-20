#!/usr/bin/env python3
import os
import requests
import json

def delete_roles():
    # Get Nexus username and password from environment variables
    username = os.environ.get('NEXUS_USERNAME')
    password = os.environ.get('NEXUS_PASSWORD')
    nexus_host = os.environ.get('NEXUS_HOST')

    # Define the roles to keep (nx-admin and nx-anonymous)
    roles_to_keep = ['nx-admin', 'nx-anonymous']

    # Get the existing roles using the Nexus API
    endpoint = f"https://{nexus_host}/service/rest/v1/security/roles"
    auth = (username, password)
    response = requests.get(endpoint, auth=auth)

    if response.status_code == 200:
        try:
            roles = response.json()
        except ValueError:
            print("Failed to retrieve roles. Response is not valid JSON.")
            return
    else:
        print(f"Failed to retrieve roles. Status Code: {response.status_code}, Error: {response.text}")
        return

    if isinstance(roles, list):
        roles_list = roles
    elif isinstance(roles, dict):
        roles_list = roles.get('items', []) or roles.get('result', [])
    else:
        print("Failed to retrieve roles. Response does not contain a valid role list.")
        return

    # Iterate over the roles and delete those that are not in the 'roles_to_keep' list
    for role in roles_list:
        role_name = role['id']
        if role_name not in roles_to_keep:
            delete_endpoint = f"https://{nexus_host}/service/rest/v1/security/roles/{role_name}"
            response = requests.delete(delete_endpoint, auth=auth)
            if response.status_code >= 200 and response.status_code <= 204:
                print(f"Role '{role_name}' deleted successfully.")
            else:
                print(f"Failed to delete role '{role_name}'. Status Code: {response.status_code}, Error: {response.text}")
        else:
            print(f"Role '{role_name}' is in the roles_to_keep list. Skipping deletion.")

# Usage
delete_roles()

