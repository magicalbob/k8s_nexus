#!/usr/bin/env python3
import os
import requests
import json

# Get the username and password from environment variables
username = os.environ.get('NEXUS_USERNAME')
password = os.environ.get('NEXUS_PASSWORD')
nexus_host = os.environ.get('NEXUS_HOST')

# Define URL and headers
url = f'https://{nexus_host}/service/rest/v1/repositories' # Nexus repositories endpoint
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

# Get the list of all repositories
response = requests.get(url, auth=(username, password))
if response.status_code == 200:
    repositories = response.json()

    # Loop through each repository and delete it
    for repo in repositories:
        repo_name = repo['name']
        delete_url = url + '/' + repo_name
        delete_response = requests.delete(delete_url, headers=headers, auth=(username, password))
        if delete_response.status_code == 204:
            print(f'Successfully deleted repository: {repo_name}')
        else:
            print(f'Failed to delete repository: {repo_name}')
else:
    print('Failed to get repository list.')

