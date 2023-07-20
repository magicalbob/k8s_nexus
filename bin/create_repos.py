import os
import requests
import json

# Get the username and password from environment variables
username = os.environ.get('NEXUS_USERNAME')
password = os.environ.get('NEXUS_PASSWORD')
nexus_host = os.environ.get('NEXUS_HOST')
repo_config = os.environ.get('NEXUS_REPO_CONFIG')

# Define URL and headers
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'NX-ANTI-CSRF-TOKEN': '0.763232663911438',
    'X-Nexus-UI': 'true',
}

file_types = ['proxy', 'hosted', 'group']
for file_type in file_types:
    file_type_path = os.path.join(repo_config, file_type)
    for repo_type in os.listdir(file_type_path):
        repo_type_path = os.path.join(file_type_path, repo_type)
        print('{}/{}'.format(file_type, repo_type))

        # Modify URL for each file_type and repo_type
        url = f'https://{nexus_host}/service/rest/v1/repositories/{repo_type}/{file_type}'

        for file in os.listdir(repo_type_path):
            file_path = os.path.join(repo_type_path, file)
            with open(file_path) as file:
                data = json.load(file)

            # Get existing repositories
            response = requests.get(f'https://{nexus_host}/service/rest/v1/repositories', auth=(username, password))
            repos = response.json()

            # Check if repository already exists
            if not any(repo['name'] == data['name'] for repo in repos):
                print(json.dumps(data))
                response = requests.post(url, headers=headers, data=json.dumps(data), auth=(username, password))
                # Print the response
                print(response.status_code)
                print(response.text)

