#!/usr/bin/env python3
import os
import requests

def delete_all_content_selectors(nexus_url):
    # Get Nexus username and password from environment variables
    username = os.environ.get('NEXUS_USERNAME')
    password = os.environ.get('NEXUS_PASSWORD')

    # Endpoint to retrieve the list of content selectors
    endpoint = f"{nexus_url}/service/rest/v1/security/content-selectors"

    # Send a GET request to retrieve the list of content selectors
    response = requests.get(endpoint, auth=(username, password))
    if response.status_code != 200:
        print(f"Failed to retrieve content selectors. Status Code: {response.status_code}, Error: {response.text}")
        return

    selectors = response.json()

    # Iterate over the selectors and delete them using the Nexus API
    for selector in selectors:
        selector_id = selector['name']
        delete_endpoint = f"{nexus_url}/service/rest/v1/security/content-selectors/{selector_id}"
        delete_response = requests.delete(delete_endpoint, auth=(username, password))
        if delete_response.status_code == 204:
            print(f"Content selector with ID '{selector_id}' deleted successfully.")
        else:
            print(f"Failed to delete content selector with ID '{selector_id}'. Status Code: {delete_response.status_code}, Error: {delete_response.text}")

# Usage
nexus_url = 'https://nexus.ellisbs.co.uk'
delete_all_content_selectors(nexus_url)

