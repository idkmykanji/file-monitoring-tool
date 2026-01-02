#src/main.py

from __future__ import annotations
from pathlib import Path
import logging
import time
from typing import List, Dict
from src.monitor import get_file_metadata, scan_once
from src.storage import load_files, save_files, add_file, remove_file
from src.permissions import get_permissions_str, get_permission_octal, set_permissions_octal, modify_permission
from src.utils import setup_logging, format_event, iter_directory_files, normalize_path


def list_monitored_files() -> None:
    """List all monitored files."""
    files = load_files()
    if not files:
        print("No files are currently being monitored.")
        return
    print("\nMonitored Files:\n")
    for file_info in files:
        print(f"  Filename: {file_info['filename']}")
        print(f"  Path: {file_info['path']}")
        # print(f"  Size: {file_info['size']} bytes")
        # print(f"  Permissions: {file_info['permissions']}")
        # print(f"  Owner: {file_info['owner']}")
        # print(f"  Group: {file_info['group']}")
        # print(f"  Created: {file_info['created']}")
        # print(f"  Created_ts: {file_info['created_ts']}")
        # print(f"  Modified: {file_info['last_modified']}")
        # print(f"  Modified_ts: {file_info['last_modified_ts']}")
        # print(f"  Hash_Algorithm: {file_info['hash_algorithm']}")
        # print(f"  Hash: {file_info['hash_value']}")
        # print(f"  Last_Hash: {file_info['last_hash']}")
        # print(f"  Last_Hash_ts: {file_info['last_hash_ts']}")
        print("")

def add_monitored_file() -> None:
    """Add a new file to be monitored."""
    path_str = input("Enter the path of the file to monitor: ").strip()
    path = normalize_path(path_str)
    if not path.exists():
        print(f"File {path_str} does not exist.")
        return

    file_info = get_file_metadata(path)
    add_file(file_info)
    print(f"Started monitoring {path_str}.")

def add_monitored_directory() -> None:
    """Add all files in a directory to be monitored."""
    dir_str = input("Enter the path of the directory to monitor: ").strip()
    directory = normalize_path(dir_str)
    if not directory.is_dir():
        print(f"{dir_str} is not a valid directory.")
        return

    recursive_str = input("Monitor recursively? (y/n): ").strip().lower()
    recursive = recursive_str == "y"

    added_files = 0
    for file_path in iter_directory_files(directory, recursive):
        file_info = get_file_metadata(file_path)
        add_file(file_info)
        added_files += 1

    print(f"Started monitoring {added_files} files in {dir_str}.")

def remove_monitored_file() -> None:
    """Remove a file from being monitored."""
    path_str = input("Enter the path of the file to stop monitoring: ").strip()
    path = normalize_path(path_str)
    remove_file(str(path))
    print(f"Stopped monitoring {path_str}.")

def remove_monitored_directory() -> None:
    """Remove all files in a directory from being monitored."""
    dir_str = input("Enter the path of the directory to stop monitoring: ").strip()
    directory = normalize_path(dir_str)
    if not directory.is_dir():
        print(f"{dir_str} is not a valid directory.")
        return

    recursive_str = input("Remove recursively? (y/n): ").strip().lower()
    recursive = recursive_str == "y"

    removed_files = 0
    monitored_files = load_files()
    paths_to_remove = {str(p) for p in iter_directory_files(directory, recursive)}

    new_monitored_files = []
    for file_info in monitored_files:
        if file_info["path"] in paths_to_remove:
            removed_files += 1
        else:
            new_monitored_files.append(file_info)

    save_files(new_monitored_files)
    print(f"Stopped monitoring {removed_files} files in {dir_str}.")

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
            print(" --- ", format_event(event))

def continuous_scan(interval: int = 5) -> None:
    """Continuously scan monitored files at specified intervals."""

    files = load_files()
    if not files:
        print("No files are currently being monitored.")
        return

    print(f"Starting continuous scan every {interval} seconds. Press Ctrl+C to stop.")

    try:
        while True:
            events = scan_once(files)
            save_files(files)

            if events:
                print("Changes detected:")
                for event in events:
                    print(" --- ", format_event(event))
            else:
                print("No changes detected.")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("Continuous scanning stopped by user.")


def main_menu() -> None:
    """Display the main menu and handle user input."""

    while True:
        
        print("\nFile Monitor Menu:")
        print("1. List monitored files")
        print("2. Add/remove a file from monitoring")
        print("3. Add/remove a directory from monitoring")
        print("4. Scan monitored files once")
        print("5. Change file permissions")
        print("6. Get file permissions")
        print("7. Start continuous scanning")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            list_monitored_files()
        elif choice == "2":
            file_action = input("Add or Remove file? (a/r): ").strip().lower()
            if file_action == "a":
                add_monitored_file()
            elif file_action == "r":
                remove_monitored_file()
        elif choice == "3":
            dir_action = input("Add or Remove directory? (a/r): ").strip().lower()
            if dir_action == "a":
                add_monitored_directory()
            elif dir_action == "r":
                remove_monitored_directory()
            else:
                print("Invalid choice. Please enter 'a' to add or 'r' to remove.")
        elif choice == "4":
            scan_once_and_report()
        elif choice == "5":
            try:
                path_str = input("Enter the path of the file to change permissions: ").strip()
                path = normalize_path(path_str)
                entity = input("Enter the entity (user/group/others/all/special): ").strip()
                perms_str = input("Enter the permissions to modify (read/write/execute or suid/sgid/sticky for special permissions) separated by commas: ").strip()
                perms = [p.strip() for p in perms_str.split(",")]
                action = input("Enter the action (add/remove): ").strip()
                modify_permission(path, entity, perms, action)
            except Exception as exc:
                print(f"Error changing permissions: {exc}")
        elif choice == "6":
            try:
                mode = input("Get permissions in (s)tring or (o)ctal format? ").strip().lower()
                if mode == "o":
                    path_str = input("Enter the path of the file to get permissions: ").strip()
                    path = normalize_path(path_str)
                    print(get_permission_octal(path))
                elif mode == "s":
                    path_str = input("Enter the path of the file to get permissions: ").strip()
                    path = normalize_path(path_str)
                    print(get_permissions_str(path))
            except Exception as exc:
                print(f"Error retrieving permissions: {exc}")
        elif choice == "7":
            try:
                interval_str = input("Enter the scan interval in seconds (default 5): ").strip()
                interval = int(interval_str) if interval_str.isdigit() else 5
                continuous_scan(interval)
            except Exception as exc:
                print(f"Error starting continuous scan: {exc}")
        
        elif choice == "8":
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
