#!/usr/bin/env python3
import os
import json

# The input JSON data
json_data = [ ... ]  # replace with your JSON data

# Go through each item in the JSON data
for item in json_data:
    # Get the name, type and format values
    name = item.get('name')
    type_ = item.get('type')
    format_ = item.get('format')

    # Construct the file path
    file_path = f'repo_config/{type_}/{format_}/{name}.json'

    # Create the necessary directories
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write the item to the file
    with open(file_path, 'w') as f:
        json.dump(item, f, indent=2)

