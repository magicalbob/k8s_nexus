#!/usr/bin/env python3
import os
import requests
import json

# get the username and password from environment variables
username = os.environ.get('NEXUS_USERNAME')
password = os.environ.get('NEXUS_PASSWORD')

# define url and headers
url = 'https://nexus.ellisbs.co.uk/service/rest/v1/repositories/maven/hosted'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'NX-ANTI-CSRF-TOKEN': '0.763232663911438',
    'X-Nexus-UI': 'true',
}

file_types=['proxy','hosted','group']
for file_type in file_types:
    for repo_type in os.listdir('repo_config/{}'.format(file_type)):
        print('{}/{}'.format(file_type,repo_type))
        for file in os.listdir('repo_config/{}/{}'.format(file_type,repo_type)):
            with open('repo_config/{}/{}/{}'.format(file_type,repo_type,file)) as file:
                data = json.load(file)
            print(json.dumps(data))
            response = requests.post(url, headers=headers, data=json.dumps(data), auth=(username, password))
            # print the response
            print(response.status_code)
            print(response.text)

