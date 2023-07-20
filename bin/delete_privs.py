import os
import requests

def delete_all_content_selector_privileges(nexus_url):
    # Get Nexus username and password from environment variables
    username = os.environ.get('NEXUS_USERNAME')
    password = os.environ.get('NEXUS_PASSWORD')
    nexus_host = os.environ.get('NEXUS_HOST')

    # Endpoint to retrieve the list of content selector privileges
    endpoint = f"https://{nexus_host}/service/rest/v1/security/privileges"

    # Send a GET request to retrieve the list of content selector privileges
    response = requests.get(endpoint, auth=(username, password))
    if response.status_code != 200:
        print(f"Failed to retrieve content selector privileges. Status Code: {response.status_code}, Error: {response.text}")
        return

    privileges = response.json()

    # Iterate over the privileges and delete them using the Nexus API
    for privilege in privileges:
        privilege_id = privilege['name']
        delete_endpoint = f"{nexus_url}/service/rest/v1/security/privileges/{privilege_id}"
        delete_response = requests.delete(delete_endpoint, auth=(username, password))
        if delete_response.status_code == 204:
            print(f"Content selector privilege with ID '{privilege_id}' deleted successfully.")
        else:
            print(f"Failed to delete content selector privilege with ID '{privilege_id}'. Status Code: {delete_response.status_code}, Error: {delete_response.text}")

delete_all_content_selector_privileges()

