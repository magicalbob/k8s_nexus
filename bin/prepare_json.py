#!/usr/bin/env python3
import os
import json
import sys

# Read JSON data from stdin
json_data = json.load(sys.stdin)

# Go through each item in the JSON data
for item in json_data:
    # Get the name, type, and format values
    name = item.get('name')
    type_ = item.get('type')
    format_ = item.get('format')

    # If the format is maven2, change it to maven
    if format_ == 'maven2':
        format_ = 'maven'
        item['format'] = format_  # Update the format in the item as well

    # Remove the unwanted keys
    item.pop('url', None)
    item.pop('cleanup', None)
    item.pop('format', None)

    # Construct the file path
    file_path = f'repo_config/{type_}/{format_}/{name}.json'

    # Create the necessary directories
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write the item to the file
    with open(file_path, 'w') as f:
        json.dump(item, f, indent=2)

