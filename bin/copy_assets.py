import os
import requests
import json
import mimetypes

# Get the old Nexus and new Nexus credentials and hosts from environment variables
old_nexus_username = os.environ.get('NEXUS_USERNAME')
old_nexus_password = os.environ.get('NEXUS_PASSWORD')
old_nexus_host = os.environ.get('NEXUS_HOST')

new_nexus_username = os.environ.get('NEW_NEXUS_USERNAME')
new_nexus_password = os.environ.get('NEW_NEXUS_PASSWORD')
new_nexus_host = os.environ.get('NEW_NEXUS_HOST')

# Define URL and headers
headers = {
    'NX-ANTI-CSRF-TOKEN': '0.763232663911438',
    'X-Nexus-UI': 'true',
}

# Get repository settings from the old Nexus
response = requests.get(f'https://{old_nexus_host}/service/rest/v1/repositorySettings', auth=(old_nexus_username, old_nexus_password))
repository_settings = response.json()

# Iterate through repository settings and copy assets
for repo_settings in repository_settings:
    repo_type = repo_settings.get('type')

    # Check if the repository is hosted (exclude groups and proxies)
    if repo_type != 'hosted':
        continue

    repo_name = repo_settings['name']
    print(f'Processing repository: {repo_name}')

    # Modify URL for each repository in both old and new Nexus
    old_nexus_url = f'https://{old_nexus_host}/service/rest/v1/assets?repository={repo_name}'
    new_nexus_url = f'https://{new_nexus_host}/service/rest/v1/components?repository={repo_name}'

    # Fetch the assets from the old Nexus repository
    response = requests.get(f'{old_nexus_url}', auth=(old_nexus_username, old_nexus_password))
    assets = response.json()

    # Iterate through assets and upload to the new Nexus repository
    for asset in assets.get('items', []):
        asset_url = asset['downloadUrl'].replace("http://", "https://")
        asset_path = asset['path']

        # Create a dictionary for the multipart/form-data request
        files = {'pypi.asset': (asset_path, requests.get(asset_url).content, mimetypes.guess_type(asset_url)[0])}

        # Add error handling for the upload process
        try:
            upload_response = requests.post(new_nexus_url, files=files, headers=headers, auth=(new_nexus_username, new_nexus_password))
            upload_response.raise_for_status()
            if upload_response.status_code != 204:
                print(f'Error uploading asset {asset_path} to new Nexus repository {repo_name}. Status Code: {upload_response.status_code}')
            else:
                print(f'Uploaded asset {asset_path} to new Nexus repository {repo_name}')
        except requests.exceptions.RequestException as upload_error:
            print(f'Error uploading asset {asset_path} to new Nexus repository {repo_name}: {upload_error}')

