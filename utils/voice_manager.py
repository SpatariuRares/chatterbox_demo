"""
Voice management utilities for handling multiple voices.
"""
from pathlib import Path
import shutil
import librosa
from typing import Dict, List, Optional, Tuple


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


def get_voice_details(voices_dir: Path, voice_name: str) -> Optional[Dict]:
    """
    Get detailed information about a specific voice.

    Args:
        voices_dir: Path to the voices directory
        voice_name: Name of the voice

    Returns:
        Dictionary with voice details or None if not found
    """
    voices_dir = Path(voices_dir)
    voice_path = voices_dir / voice_name

    if not voice_path.exists():
        return None

    # Get audio files
    audio_extensions = ['.wav', '.mp3', '.ogg', '.flac', '.m4a', '.opus']
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(list(voice_path.glob(f"*{ext}")))

    # Calculate total duration
    total_duration = 0.0
    file_details = []

    for audio_file in sorted(audio_files):
        try:
            duration = librosa.get_duration(path=str(audio_file))
            total_duration += duration
            file_details.append({
                'name': audio_file.name,
                'path': str(audio_file),
                'duration': duration,
                'size': audio_file.stat().st_size
            })
        except Exception as e:
            print(f"Warning: Could not read {audio_file.name}: {e}")

    return {
        'name': voice_name,
        'path': str(voice_path),
        'audio_count': len(audio_files),
        'total_duration': total_duration,
        'files': file_details
    }


def create_voice(voices_dir: Path, voice_name: str, audio_files: List[str]) -> Tuple[bool, str]:
    """
    Create a new voice by copying audio files to a new folder.

    Args:
        voices_dir: Path to the voices directory
        voice_name: Name for the new voice
        audio_files: List of paths to audio files to include

    Returns:
        Tuple of (success, message)
    """
    voices_dir = Path(voices_dir)
    voice_path = voices_dir / voice_name

    # Check if voice already exists
    if voice_path.exists():
        return False, f"Voice '{voice_name}' already exists"

    # Create voice directory
    try:
        voice_path.mkdir(parents=True, exist_ok=False)
    except Exception as e:
        return False, f"Failed to create voice directory: {e}"

    # Copy audio files
    copied_count = 0
    for audio_file in audio_files:
        try:
            src = Path(audio_file)
            dst = voice_path / src.name
            shutil.copy2(src, dst)
            copied_count += 1
        except Exception as e:
            print(f"Warning: Failed to copy {audio_file}: {e}")

    if copied_count == 0:
        # Clean up empty directory
        voice_path.rmdir()
        return False, "No audio files were copied successfully"

    return True, f"Voice '{voice_name}' created with {copied_count} audio files"


def add_audio_to_voice(voices_dir: Path, voice_name: str, audio_files: List[str]) -> Tuple[bool, str]:
    """
    Add audio files to an existing voice.

    Args:
        voices_dir: Path to the voices directory
        voice_name: Name of the voice
        audio_files: List of paths to audio files to add

    Returns:
        Tuple of (success, message)
    """
    voices_dir = Path(voices_dir)
    voice_path = voices_dir / voice_name

    if not voice_path.exists():
        return False, f"Voice '{voice_name}' does not exist"

    copied_count = 0
    for audio_file in audio_files:
        try:
            src = Path(audio_file)
            dst = voice_path / src.name

            # Check if file already exists
            if dst.exists():
                # Add number suffix
                counter = 1
                while dst.exists():
                    dst = voice_path / f"{src.stem}_{counter}{src.suffix}"
                    counter += 1

            shutil.copy2(src, dst)
            copied_count += 1
        except Exception as e:
            print(f"Warning: Failed to copy {audio_file}: {e}")

    if copied_count == 0:
        return False, "No audio files were added"

    return True, f"Added {copied_count} audio files to '{voice_name}'"


def remove_audio_from_voice(voices_dir: Path, voice_name: str, audio_filename: str) -> Tuple[bool, str]:
    """
    Remove an audio file from a voice.

    Args:
        voices_dir: Path to the voices directory
        voice_name: Name of the voice
        audio_filename: Name of the audio file to remove

    Returns:
        Tuple of (success, message)
    """
    voices_dir = Path(voices_dir)
    voice_path = voices_dir / voice_name
    audio_path = voice_path / audio_filename

    if not audio_path.exists():
        return False, f"Audio file '{audio_filename}' not found in voice '{voice_name}'"

    try:
        audio_path.unlink()
        return True, f"Removed '{audio_filename}' from '{voice_name}'"
    except Exception as e:
        return False, f"Failed to remove audio file: {e}"


def delete_voice(voices_dir: Path, voice_name: str) -> Tuple[bool, str]:
    """
    Delete a voice and all its audio files.

    Args:
        voices_dir: Path to the voices directory
        voice_name: Name of the voice to delete

    Returns:
        Tuple of (success, message)
    """
    voices_dir = Path(voices_dir)
    voice_path = voices_dir / voice_name

    if not voice_path.exists():
        return False, f"Voice '{voice_name}' does not exist"

    try:
        shutil.rmtree(voice_path)
        return True, f"Voice '{voice_name}' deleted successfully"
    except Exception as e:
        return False, f"Failed to delete voice: {e}"


def rename_voice(voices_dir: Path, old_name: str, new_name: str) -> Tuple[bool, str]:
    """
    Rename a voice.

    Args:
        voices_dir: Path to the voices directory
        old_name: Current name of the voice
        new_name: New name for the voice

    Returns:
        Tuple of (success, message)
    """
    voices_dir = Path(voices_dir)
    old_path = voices_dir / old_name
    new_path = voices_dir / new_name

    if not old_path.exists():
        return False, f"Voice '{old_name}' does not exist"

    if new_path.exists():
        return False, f"Voice '{new_name}' already exists"

    try:
        old_path.rename(new_path)
        return True, f"Voice renamed from '{old_name}' to '{new_name}'"
    except Exception as e:
        return False, f"Failed to rename voice: {e}"
