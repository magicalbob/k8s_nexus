import os
import requests

# Get the username and password from environment variables
username = os.environ.get('NEXUS_USERNAME')
password = os.environ.get('NEXUS_PASSWORD')
nexus_host = os.environ.get('NEXUS_HOST')

def delete_user(user_id):
    url = f'https://{nexus_host}/service/rest/v1/security/users/{user_id}'
    print("Using URL:", url)
    headers = {
        'Accept': 'application/json',
        'NX-ANTI-CSRF-TOKEN': '0.763232663911438',
        'X-Nexus-UI': 'true'
    }
    response = requests.delete(url, headers=headers, auth=(username, password))
    response.raise_for_status()

def main():
    # Retrieve the list of users from Nexus
    url = f'https://{nexus_host}/service/rest/v1/security/users'
    headers = {
        'Accept': 'application/json',
        'NX-ANTI-CSRF-TOKEN': '0.763232663911438',
        'X-Nexus-UI': 'true'
    }
    response = requests.get(url, headers=headers, auth=(username, password))
    response.raise_for_status()
    users = response.json()

    # Delete all users except for "admin" and "anonymous"
    for user in users:
        if user['userId'] in  [ 'admin', 'anonymous' ]:
            print(f'Skip user {user["userId"]}')
        else:
            delete_user(user['userId'])
            print(f'Deleted user: {user["userId"]}')

if __name__ == '__main__':
    main()
