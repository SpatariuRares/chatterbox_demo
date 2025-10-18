"""
Voice management utilities for handling multiple voices.
"""
from pathlib import Path


def get_available_voices(voices_dir):
    """
    Get list of available voices from the voices directory.

    Args:
        voices_dir: Path to the voices directory

    Returns:
        List of voice names (folder names)
    """
    voices_dir = Path(voices_dir)

    if not voices_dir.exists():
        return []

    voices = [
        d.name for d in voices_dir.iterdir()
        if d.is_dir() and not d.name.startswith('.')
    ]
    return sorted(voices)


def validate_voice(voices_dir, voice_name):
    """
    Validate that the selected voice exists and contains audio files.

    Args:
        voices_dir: Path to the voices directory
        voice_name: Name of the voice to validate

    Returns:
        tuple: (is_valid: bool, voice_path or error_message: str)
    """
    voices_dir = Path(voices_dir)
    voice_path = voices_dir / voice_name

    if not voice_path.exists():
        return False, f"Cartella voce non trovata: {voice_path}"

    # Check for audio files
    audio_extensions = ['.wav', '.mp3', '.ogg', '.flac', '.m4a', '.opus']
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(list(voice_path.glob(f"*{ext}")))

    if not audio_files:
        return False, f"Nessun file audio trovato in: {voice_path}"

    return True, str(voice_path)


def list_voices_info(voices_dir):
    """
    Get detailed information about all available voices.

    Args:
        voices_dir: Path to the voices directory

    Returns:
        dict: Dictionary with voice names as keys and info as values
    """
    voices_dir = Path(voices_dir)
    voices_info = {}

    if not voices_dir.exists():
        return voices_info

    for voice_dir in voices_dir.iterdir():
        if not voice_dir.is_dir() or voice_dir.name.startswith('.'):
            continue

        # Count audio files
        audio_extensions = ['.wav', '.mp3', '.ogg', '.flac', '.m4a', '.opus']
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(list(voice_dir.glob(f"*{ext}")))

        voices_info[voice_dir.name] = {
            'path': str(voice_dir),
            'audio_files_count': len(audio_files),
            'audio_files': [f.name for f in sorted(audio_files)]
        }

    return voices_info
