import json

from project.utils.File.file import File


def read_json_file(path: str):
    with File(path, 'r') as json_file:
        # Load existing data into a dict
        return json.loads(json_file.read())


def add_to_json_file(path: str, new_data: dict):
    with File(path, 'r+') as json_file:
        # Load existing data into a dict.
        file_data = json.loads(json_file.read())
        # Adds new_data to file_data
        file_data.append(new_data)
        # Sets file's current position at offset.
        json_file.seek(0)
        # Convert back to json.
        json.dump(file_data, json_file, indent=4)
        return True


def rewrite_json_file(path: str, data: dict):
    with File(path, 'w') as json_file:
        # Serializing json
        json_object = json.dumps(data, indent=4)
        # Writing
        json_file.write(json_object)
        return True