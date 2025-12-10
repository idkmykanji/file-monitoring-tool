from __future__ import annotations
import logging
from pathlib import Path
from typing import Iterator

#colors for CLI output
RESET = "\033[0m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

#setup logging
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
            #logging.StreamHandler()
        ],
    )



#classify event type and return color and severity
def classify_event(event: str) -> tuple[str, str]:
    """Classify event type for colored output."""

    #i consider hash changes and missing files as critical, owner/group/permission changes as warning, size/modification as info
    if "[HASH_CHANGED]" in event or "[MISSING]" in event:
        return RED, "CRITICAL"
    elif any(tag in event for tag in ["[OWNER_CHANGED]", "[GROUP_CHANGED]", "[PERMISSIONS_CHANGED]"]):
        return YELLOW, "WARNING"
    elif any(tag in event for tag in ["[SIZE_CHANGED]", "[MODIFIED]"]):
        return CYAN, "INFO"
    else:
        return "", "INFO"

def format_event(event: str) -> str:
    """Format event with color coding."""
    color, severity = classify_event(event)
    if color:
        return f"{color}{severity}{event}{RESET}"
    return event


def normalize_path(path: str) -> Path:
    """Normalize a file path to its absolute resolved form."""
    return Path(path).expanduser().resolve()


#iterate over files in a directory (with optional recursion) for adding multiple files to monitoring
def iter_directory_files(directory: Path, recursive: bool = False) -> Iterator[Path]:
    """Iterate over all files in a directory. If recursive is True, include subdirectories."""
    if recursive:
        for p in directory.rglob("*"):
            if p.is_file():
                yield p
    else:
        for p in directory.iterdir():
            if p.is_file():
                yield p