#!/usr/bin/env python3
import os
import json
import requests
import random
import string

PASSWORD_LEN = 10

# Get the admin username and password from environment variables
username = os.environ.get('NEXUS_USERNAME')
password = os.environ.get('NEXUS_PASSWORD')
nexus_host = os.environ.get('NEXUS_HOST')
nexus_users = os.environ.get('NEXUS_USERS')  # JSON file containing user input data
nexus_output = os.environ.get('NEXUS_OUTPUT')  # Output file of users created

def generate_password(length=PASSWORD_LEN):
    """Generate a random password."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def user_exists(user_id):
    print(f'Checking for user: {user_id}')
    url = f'https://{nexus_host}/service/rest/v1/security/users'
    headers = {
        'Accept': 'application/json',
    }
    response = requests.get(url, headers=headers, auth=(username, password))
    response.raise_for_status()
    users = response.json()
    user_ids = [user['userId'] for user in users]
    return user_id in user_ids

def create_user(user):
    url = f'https://{nexus_host}/service/rest/v1/security/users'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    # Generate a random password for the user
    user['password'] = generate_password()

    response = requests.post(url, json=user, headers=headers, auth=(username, password))
    response.raise_for_status()

def main():
    with open(nexus_users) as file:
        users = json.load(file)
    
    created_users = []

    for user in users:
        user_id = user['userId']
        if user_exists(user_id):
            print(f'Skipping creation of user: {user_id} (already exists)')
        else:
            print(f'User {user_id} does not exist, creating...')
            create_user(user)
            created_users.append({
                'userId': user_id,
                'password': user['password']
            })
            print(f'Created user: {user_id}')

    # Write the created users' userId and password to the specified output file
    with open(nexus_output, 'w') as output_file:
        json.dump(created_users, output_file)

if __name__ == '__main__':
    main()
