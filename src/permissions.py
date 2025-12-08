from __future__ import annotations
from pathlib import Path
import os
import stat
import logging

logger = logging.getLogger(__name__)

#mapping of permission bits for user, group, and others
PERM_BITS = {
    "user": {
        "read": stat.S_IRUSR,
        "write": stat.S_IWUSR,
        "execute": stat.S_IXUSR,
    },
    "group": {
        "read": stat.S_IRGRP,
        "write": stat.S_IWGRP,
        "execute": stat.S_IXGRP,
    },
    "others": {
        "read": stat.S_IROTH,
        "write": stat.S_IWOTH,
        "execute": stat.S_IXOTH,
    },
}

#get file permissions in different formats

def get_permissions_str(path: Path) -> str:
    """Get the file permissions in a human-readable format."""

    perm_str = path.stat().st_mode
    return stat.filemode(perm_str)

def get_permission_octal(path: Path) -> str:
    """Get the file permissions in octal format."""

    mode = path.stat().st_mode
    # keep special bits and format in 4 digits
    perm_octal = mode & 0o7777
    return format(perm_octal, "04o")

def set_permissions_octal(path: Path, perm_octal: str) -> None:
    """Set the file permissions using an octal string."""
    
    perm_octal = perm_octal.strip()

    if not perm_octal:
        raise ValueError("Permission octal string cannot be empty.")
    
    try:
        perm_int = int(perm_octal, 8)
    except ValueError:
        raise ValueError(f"Invalid octal permission string: {perm_octal}")
    
    path.chmod(perm_int)

    logger.info(f"Set permissions of {path} to {perm_octal}.")

def modify_permission(path: Path, entity: str, perms: list[str], action: str) -> None:
    """Modify specific permissions for user, group, or others."""

    entity = entity.lower()
    action = action.lower()
    perms = [p.lower() for p in perms]
    
    if entity not in PERM_BITS:
        raise ValueError(f"Invalid entity: {entity}. Must be 'user', 'group', or 'others'.")

    mode = path.stat().st_mode

    for perm in perms:
        if perm not in PERM_BITS[entity]:
            raise ValueError(f"Invalid permission: {perm}. Must be 'read', 'write', or 'execute'.")

        perm_bit = PERM_BITS[entity][perm]

        if action == "add":
            mode |= perm_bit
        elif action == "remove":
            mode &= ~perm_bit
        else:
            raise ValueError(f"Invalid action: {action}. Must be 'add' or 'remove'.")

    path.chmod(mode)

    logger.info(f"Modified permissions of {path}: {action} {perms} for {entity}.")