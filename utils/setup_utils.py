"""
Setup and initialization utilities.
"""
import torch
from pathlib import Path


def detect_device(device_config=None):
    """
    Auto-detect the best available device for inference.

    Args:
        device_config: Manual device selection (None for auto-detect)

    Returns:
        str: Device name ('cuda', 'mps', or 'cpu')
    """
    if device_config:
        return device_config

    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"


def setup_directories(*paths):
    """
    Create necessary directories if they don't exist.

    Args:
        *paths: Variable number of Path objects to create
    """
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)


def print_section(title: str, separator_char: str = "=", width: int = 60) -> None:
    """
    Print a formatted section header.

    Args:
        title: Section title to print
        separator_char: Character to use for separator line
        width: Width of the separator line
    """
    separator = separator_char * width
    print(f"\n{separator}")
    print(title)
    print(separator)
