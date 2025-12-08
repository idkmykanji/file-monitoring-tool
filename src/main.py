#src/main.py

from __future__ import annotations
from pathlib import Path
import logging
from typing import List, Dict
from src.monitor import get_file_metadata, scan_once
from src.storage import load_files, save_files, add_file, remove_file

def setup_logging() -> None:
    """Setup logging configuration."""

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "file_monitor.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ],
    )

def list_monitored_files() -> None:
    """List all monitored files."""
    files = load_files()
    if not files:
        print("No files are currently being monitored.")
        return

    for file_info in files:
        print(f"  Filename: {file_info['filename']}")
        print(f"  Path: {file_info['path']}")
        print(f"  Size: {file_info['size']} bytes")
        print(f"  Permissions: {file_info['permissions']}")
        print(f"  Owner: {file_info['owner']}")
        print(f"  Group: {file_info['group']}")
        print(f"  Created: {file_info['created']}")
        print(f"  Created_ts: {file_info['created_ts']}")
        print(f"  Modified: {file_info['last_modified']}")
        print(f"  Modified_ts: {file_info['last_modified_ts']}")
        print(f"  Hash_Algorithm: {file_info['hash_algorithm']}")
        print(f"  Hash: {file_info['hash_value']}")
        print(f"  Last_Hash: {file_info['last_hash']}")
        print(f"  Last_Hash_ts: {file_info['last_hash_ts']}")
        print("")

def add_monitored_file() -> None:
    """Add a new file to be monitored."""
    path_str = input("Enter the path of the file to monitor: ").strip()
    path = Path(path_str).expanduser().resolve()
    if not path.exists():
        print(f"File {path_str} does not exist.")
        return

    file_info = get_file_metadata(path)
    add_file(file_info)
    print(f"Started monitoring {path_str}.")

def remove_monitored_file() -> None:
    """Remove a file from being monitored."""
    path_str = input("Enter the path of the file to stop monitoring: ").strip()
    path = Path(path_str).expanduser().resolve()
    remove_file(str(path))
    print(f"Stopped monitoring {path_str}.")

def scan_once_and_report() -> None:
    """Perform a single scan of monitored files and report changes."""
    files = load_files()
    if not files:
        print("No files are currently being monitored.")
        return

    events = scan_once(files)
    save_files(files)

    if not events:
        print("No changes detected.")
    else:
        print("Changes detected:")
        for event in events:
            print(event)

def main_menu() -> None:
    """Display the main menu and handle user input."""

    while True:
        print("\nFile Monitor Menu:")
        print("1. List monitored files")
        print("2. Add a file to monitor")
        print("3. Remove a file from monitoring")
        print("4. Scan monitored files once")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            list_monitored_files()
        elif choice == "2":
            add_monitored_file()
        elif choice == "3":
            remove_monitored_file()
        elif choice == "4":
            scan_once_and_report()
        elif choice == "5":
            print("Exiting File Monitor.")
            break
        else:
            print("Invalid choice. Please try again.")

def main() -> None:
    """Main entry point for the file monitoring application."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting File Monitor Application")
    main_menu()

if __name__ == "__main__":
    main()