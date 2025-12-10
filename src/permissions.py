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
    "all": {
        "read": stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH,
        "write": stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH,
        "execute": stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
    },
    "special": {
        "suid": stat.S_ISUID,
        "sgid": stat.S_ISGID,
        "sticky": stat.S_ISVTX,
    }
}

#get file permissions in different formats

#human-readable string
def get_permissions_str(path: Path) -> str:
    """Get the file permissions in a human-readable format."""

    perm_str = path.stat().st_mode
    return stat.filemode(perm_str)
#octal format
def get_permission_octal(path: Path) -> str:
    """Get the file permissions in octal format."""

    mode = path.stat().st_mode
    # keep special bits and format in 4 digits
    perm_octal = mode & 0o7777
    return format(perm_octal, "04o")

#set file permissions using octal string
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

#add/remove specific permissions
def modify_permission(path: Path, entity: str, perms: list[str], action: str) -> None:
    """Modify specific permissions for user, group, or others."""

    entity = entity.lower()
    action = action.lower()
    perms = [p.lower() for p in perms]

    #check if entity is valid
    if entity not in PERM_BITS:
        raise ValueError(f"Invalid entity: {entity}. Must be 'user', 'group', 'others', 'all', 'special'.")

    mode = path.stat().st_mode

    #check if permissions are valid and modify mode accordingly
    for perm in perms:
        if perm not in PERM_BITS[entity]:
            raise ValueError(f"Invalid permission: {perm}. Must be 'read', 'write', 'execute', 'suid', 'sgid', 'sticky'.")

        perm_bit = PERM_BITS[entity][perm]

        if action == "add":
            mode |= perm_bit
        elif action == "remove":
            mode &= ~perm_bit
        else:
            raise ValueError(f"Invalid action: {action}. Must be 'add' or 'remove'.")

    path.chmod(mode)

    logger.info(f"Modified permissions of {path}: {action} {perms} for {entity}.")