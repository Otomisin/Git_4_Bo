import json

def load_dictionary(path):
    """
    Loads the JSON dictionary file and transforms it into a list of dictionaries
    with 'word', 'definition', and 'example' keys.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            raw_data = json.load(file)  # Load JSON as dictionary
            # Transform into a list of dictionaries
            dictionary_data = [
                {"word": key, "definition": value, "example": ""}  # Provide an empty example
                for key, value in raw_data.items()
            ]
            print(f"Loaded {len(dictionary_data)} words.")
            return dictionary_data
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"Error reading the file: {e}")
    return None
