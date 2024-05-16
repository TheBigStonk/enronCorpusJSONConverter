import os
import re
import json
import chardet

def parse_email(file_path):
    """
    Parses the email from a given file and extracts details including the full content.
    """
    email_details = {
        'Message-ID': None,
        'Date': None,
        'From': None,
        'To': None,
        'Subject': None,
        'Cc': None,
        'Bcc': None,
        'Mime-Version': None,
        'Content-Type': None,
        'Content-Transfer-Encoding': None,
        'X-From': None,
        'X-To': None,
        'X-cc': None,
        'X-bcc': None,
        'X-Folder': None,
        'X-Origin': None,
        'X-FileName': None,
        'Content': []
    }
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    with open(file_path, 'r', encoding=encoding) as file:
        lines = file.readlines()

# Use a flag to note when headers are complete and content begins
    headers_complete = False
    for line in lines:
        line = line.strip()
        if line == '':
            if not headers_complete:
                # An empty line typically means headers are complete
                headers_complete = True
            continue
        
        if headers_complete:
            email_details['Content'].append(line)
        else:
            header_match = re.match(r'^(\w+-\w+|\w+):(.*)', line)
            if header_match:
                key = header_match.group(1)
                value = header_match.group(2).strip()
                if key in email_details:
                    email_details[key] = value
                else:
                    headers_complete = True  # Assume headers end if unexpected header found
                    email_details['Content'].append(line)
            else:
                # No header pattern matched and headers are deemed complete
                headers_complete = True
                email_details['Content'].append(line)

    # Convert the list of Content lines into a single string
    email_details['Content'] = "\n".join(email_details['Content'])
    return email_details

def save_as_json(email_data, file_path):
    """
    Saves the parsed email data as a JSON file, overwriting the original file.
    """
    # Change the file extension to .json and overwrite the original
    base_file_path = os.path.splitext(file_path)[0] + ".json"
    with open(base_file_path, 'w', encoding='utf-8') as f:
        json.dump(email_data, f, indent=4)
    print(f"Converted and saved: {base_file_path}")
    os.remove(file_path)  # Delete the original file

def process_directory(root_dir):
    """
    Walks through all files in the directory and subdirectories,
    parses each file assumed to be an email, converts it to JSON,
    and replaces the original file with the JSON version.
    """
    for subdir, dirs, files in os.walk(root_dir):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            if filepath.endswith("."):  # assuming text files are emails
                email_data = parse_email(filepath)
                save_as_json(email_data, filepath)

# Set the root directory containing email files
root_directory = "/add/in/directory"
process_directory(root_directory)
