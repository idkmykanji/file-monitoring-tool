#src/storage.py
from __future__ import annotations
from pathlib import Path
import json
from typing import List, Dict

DATA_FILE = Path("data") / "monitored_files.json"

#files will be stored as a list of dictionaries in the JSON file

def load_files() -> List[Dict]:
    """Load the list of monitored files from the JSON file."""

    #ensure the data directory exists or create it if not
    DATA_FILE.parent.mkdir(exist_ok=True)

    #check if the data file exists or return an empty list
    if not DATA_FILE.exists():
        return []

    #open and read the JSON file. we attempt to parse it and convert JSON -> python objects, returning an empty list on failure
    with DATA_FILE.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
        
    #data should be a list of dictionaries
    return data

def save_files(files: List[Dict]) -> None:
    """Save the list of monitored files to the JSON file."""

    #ensure the data directory exists or create it if not
    DATA_FILE.parent.mkdir(exist_ok=True)

    #open and write the JSON file. we convert python objects -> JSON
    with DATA_FILE.open("w", encoding="utf-8") as f:

        #write the list of dictionaries to the file as JSON with indentation for readability
        json.dump(files, f, indent=4)


def add_file(file_info: Dict) -> None:
    """Add a new file to the monitored files list."""

    #load existing files
    files = load_files()

    #check for dupes
    if any(f.get("path") == file_info.get("path") for f in files):
        return  #file already exists, do not add again
    
    #add new file to list
    files.append(file_info)

    #save new list
    save_files(files)

def remove_file(file_path: str) -> None:
    """Remove a file from the monitored files list by its path."""

    #load existing files
    files = load_files()

    #filter out the file to be removed
    files = [f for f in files if f.get("path") != file_path]

    #save updated list
    save_files(files)


