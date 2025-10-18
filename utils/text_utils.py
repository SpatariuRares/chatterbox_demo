"""
Text utilities for reading and processing text files.
"""
from pathlib import Path


def read_text_from_file(text_file):
    """
    Legge il testo da un file txt.

    Args:
        text_file: Path del file di testo

    Returns:
        Il contenuto del file come stringa

    Raises:
        FileNotFoundError: Se il file non esiste
        ValueError: Se il file è vuoto
    """
    text_path = Path(text_file)

    if not text_path.exists():
        raise FileNotFoundError(f"File non trovato: {text_file}")

    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read().strip()

    if not text:
        raise ValueError(f"Il file {text_file} è vuoto")

    print(f"Testo caricato da {text_path.name}: {len(text)} caratteri")
    return text
