#!/usr/bin/env python3
import os
import json
import requests

# get the username and password from environment variables
username = os.environ.get('NEXUS_USERNAME')
password = os.environ.get('NEXUS_PASSWORD')
nexus_host = os.environ.get('NEXUS_HOST')

def create_privilege(privilege):
    url = f'https://{nexus_host}/service/rest/v1/security/privileges/repository-content-selector/{privilege["name"]}'
    print("Using URL %s" % (url))
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'NX-ANTI-CSRF-TOKEN': '0.763232663911438',
        'X-Nexus-UI': 'true'
    }
    response = requests.post(url, json=privilege, headers=headers, auth=('admin', 'LetMeIn'))
    response.raise_for_status()

def main():
    with open('nexus.priv.dwp.json') as file:
        privileges = json.load(file)
    
    for privilege in privileges:
        create_privilege(privilege)
        print(f'Created privilege: {privilege["name"]}')

if __name__ == '__main__':
    main()

