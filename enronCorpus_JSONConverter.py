import os
import re
import json
import chardet

def parse_email(file_path):
    """
    Parses the email from a given file and extracts details including optional fields.
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

    key = None
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        header_match = re.match(r'^(\w+-\w+|\w+):', line)
        if header_match:
            key = header_match.group(1)
            value = line[len(key)+1:].strip()
            if key in email_details:
                if key == 'Content':
                    email_details[key].append(value)
                else:
                    email_details[key] = value
            else:
                email_details['Content'].append(line)
        elif key == 'Content' or key is None:
            email_details['Content'].append(line)

    email_details['Content'] = "\n".join(email_details['Content'])
    return email_details

def save_as_json(email_data, file_path):
    """
    Saves the parsed email data as a JSON file.
    """
    base_file_path = os.path.splitext(file_path)[0] + ".json"
    with open(base_file_path, 'w', encoding='utf-8') as f:
        json.dump(email_data, f, indent=4)
    print(f"Converted and saved: {base_file_path}")

def process_directory(root_dir):
    """
    Walks through all files in the directory and subdirectories,
    parses each file assumed to be an email, converts it to JSON,
    and replaces the original file with the JSON version.
    """
    for subdir, dirs, files in os.walk(root_dir):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            if filepath.endswith("."):
                email_data = parse_email(filepath)
                save_as_json(email_data, filepath)

root_directory = "/manually/hard/code/in/directory"
process_directory(root_directory)
