import os
import requests
import json
import mimetypes

def get_field_name_for_repository(repo_name):
    # Define a mapping of repository names to field names
    repository_to_field = {
        'pypi-hosted': 'pypi.asset',
        'npm-hosted': 'npm.asset',
        'maven-hosted': 'maven.asset',
        # Add more mappings for other repositories as needed
    }
    
    # Check if the repo_name exists in the mapping
    if repo_name in repository_to_field:
        return repository_to_field[repo_name]
    else:
        # If not found, you can return a default field name or raise an error
        # For example, return a generic field name:
        return 'asset'

# Get the old Nexus and new Nexus credentials and hosts from environment variables
old_nexus_username = os.environ.get('NEXUS_USERNAME')
old_nexus_password = os.environ.get('NEXUS_PASSWORD')
old_nexus_host = os.environ.get('NEXUS_HOST')

new_nexus_username = os.environ.get('NEW_NEXUS_USERNAME')
new_nexus_password = os.environ.get('NEW_NEXUS_PASSWORD')
new_nexus_host = os.environ.get('NEW_NEXUS_HOST')

# Define a base directory where assets will be saved locally
base_directory = 'downloaded_assets'

# Create the base directory if it doesn't exist
if not os.path.exists(base_directory):
    os.makedirs(base_directory)

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

    # Iterate through assets and download them to the local directory
    for asset in assets.get('items', []):
        asset_url = asset['downloadUrl'].replace("http://", "https://")
        asset_path = asset['path']

        # Create the full local path for saving the asset
        local_asset_path = os.path.join(base_directory, asset_path)

        # Create the directory structure if it doesn't exist
        local_asset_dir = os.path.dirname(local_asset_path)
        if not os.path.exists(local_asset_dir):
            os.makedirs(local_asset_dir)

        # Fetch the asset content
        asset_content = requests.get(asset_url, auth=(old_nexus_username, old_nexus_password))
        asset_content.raise_for_status()

        # Save the asset locally
        with open(local_asset_path, 'wb') as local_file:
            local_file.write(asset_content.content)

        print(f'Downloaded asset {asset_path} to {local_asset_path}')

