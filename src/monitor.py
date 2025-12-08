#src/monitor.py
from __future__ import annotations
from pathlib import Path
import time
import os
import hashlib
import stat
from datetime import datetime
import logging
from typing import List, Dict
import pwd
import grp

logger = logging.getLogger(__name__)

HASH_ALGORITHM: str = "sha256"

def calculate_hash(path: Path) -> str:
    """Calculate the hash of a file using the specified hashing algorithm. Default is SHA-256."""
    
    #create hash object
    hash = hashlib.new(HASH_ALGORITHM)

    with path.open("rb") as f:
        #read file in chunks until EOF
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    #return hash digest as hexadecimal string        
    return hash.hexdigest()

def get_file_metadata(path: Path) -> Dict:
    """Retrieve metadata for a given file path."""
    
    #retrieve file metadata 
    stats = path.stat()
    filename = path.name

    #get size in bytes
    size = stats.st_size

    #get human-readable file mode
    perm_str = stat.filemode(stats.st_mode)

    #get owner name 
    owner_name = pwd.getpwuid(stats.st_uid).pw_name

    #get group name
    group_name = grp.getgrgid(stats.st_gid).gr_name

    #get time created as human-readable string
    ctime_ts = stats.st_ctime
    ctime_dt = datetime.fromtimestamp(ctime_ts)
    ctime_iso = ctime_dt.isoformat(timespec='seconds')

    #get last modified time as human-readable string
    mtime_ts = stats.st_mtime
    mtime_dt = datetime.fromtimestamp(mtime_ts)
    mtime_iso = mtime_dt.isoformat(timespec='seconds')

    #calculate file hash and timestamp
    hash_value = calculate_hash(path)
    hash_time_dt = datetime.now()
    hash_time_ts = hash_time_dt.timestamp()
    hash_time_iso = hash_time_dt.isoformat(timespec='seconds')

    return {
        "filename": filename,
        "path": str(path),
        "owner": owner_name,
        "group": group_name,
        "permissions": perm_str,
        "size": size,
        "created_ts": ctime_ts,
        "created": ctime_iso,
        "last_modified_ts": mtime_ts,
        "last_modified": mtime_iso,
        "hash_algorithm": HASH_ALGORITHM,
        "hash_value": hash_value,
        "last_hash_ts": hash_time_ts,
        "last_hash": hash_time_iso,
    }

def scan_once(monitored_files: List[Dict]) -> List[str]:
    """Perform a single scan of the monitored files, updating their metadata and recording the changes."""

    events: List[str] = []

    for file_info in monitored_files:
        path = Path(file_info["path"])

        #check existence
        if not path.exists():
            msg = f"[MISSING] {path} does not exist."
            events.append(msg)
            logger.warning(msg)
            continue

        current_info = get_file_metadata(path)

        if file_info["owner"] != current_info["owner"]:
            msg = f"[OWNER_CHANGED] {path} owner changed from {file_info['owner']} -> {current_info['owner']}."
            events.append(msg)
            logger.info(msg)
            file_info["owner"] = current_info["owner"]

        if file_info["group"] != current_info["group"]:
            msg = f"[GROUP_CHANGED] {path} group changed from {file_info['group']} -> {current_info['group']}."
            events.append(msg)
            logger.info(msg)
            file_info["group"] = current_info["group"]
        
        if file_info["permissions"] != current_info["permissions"]:
            msg = f"[PERMISSIONS_CHANGED] {path} permissions changed from {file_info['permissions']} -> {current_info['permissions']}."
            events.append(msg)
            logger.info(msg)
            file_info["permissions"] = current_info["permissions"]
        
        if file_info["size"] != current_info["size"]:
            msg = f"[SIZE_CHANGED] {path} size changed from {file_info['size']} -> {current_info['size']}."
            events.append(msg)
            logger.info(msg)
            file_info["size"] = current_info["size"]
        
        if file_info["last_modified_ts"] != current_info["last_modified_ts"]:
            msg = f"[MODIFIED] {path} last modified time changed from {file_info['last_modified']} -> {current_info['last_modified']}."
            events.append(msg)
            logger.info(msg)
            file_info["last_modified_ts"] = current_info["last_modified_ts"]
            file_info["last_modified"] = current_info["last_modified"]

        if file_info["hash_value"] != current_info["hash_value"]:
            msg = f"[HASH_CHANGED] {path} hash value changed."
            events.append(msg)
            logger.info(msg)
            file_info["hash_value"] = current_info["hash_value"]
            
        file_info["last_hash_ts"] = current_info["last_hash_ts"]
        file_info["last_hash"] = current_info["last_hash"]

        return events


