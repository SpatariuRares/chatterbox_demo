"""
Gradio UI helper functions for the web interface.
"""
from pathlib import Path
from typing import List, Tuple, Optional
import gradio as gr


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string (e.g., "1m 30s" or "45s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


def get_voice_info_display(voice_name: str, voices_dir: Path) -> str:
    """
    Get formatted display string with voice information.

    Args:
        voice_name: Name of the voice
        voices_dir: Path to voices directory

    Returns:
        Formatted info string
    """
    from utils.voice_manager import get_voice_details

    details = get_voice_details(voices_dir, voice_name)
    if not details:
        return "Voice not found"

    return (f"**{voice_name}**\n"
            f"Audio files: {details['audio_count']}\n"
            f"Total duration: {format_duration(details['total_duration'])}")


def get_text_info_display(text_content: str, max_chars: int = 500) -> str:
    """
    Get formatted display string with text information.

    Args:
        text_content: The text content
        max_chars: Maximum characters for single-pass mode

    Returns:
        Formatted info string
    """
    char_count = len(text_content)
    is_long = char_count > max_chars

    if is_long:
        chunks = (char_count + max_chars - 1) // max_chars
        mode = f"CHUNKED ({chunks} chunks)"
    else:
        mode = "SINGLE-PASS"

    return (f"Length: {char_count} characters\n"
            f"Mode: {mode}\n"
            f"Preview: {text_content[:100]}..." if char_count > 100 else f"Text: {text_content}")


def validate_text_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate uploaded text file.

    Args:
        file_path: Path to uploaded file

    Returns:
        Tuple of (is_valid, message)
    """
    path = Path(file_path)

    # Check extension
    if path.suffix.lower() != '.txt':
        return False, "Only .txt files are allowed"

    # Check file size (max 1MB)
    if path.stat().st_size > 1_000_000:
        return False, "File too large (max 1MB)"

    # Try to read as text
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            return False, "File is empty"
        return True, "Valid text file"
    except UnicodeDecodeError:
        return False, "File is not valid UTF-8 text"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"


def validate_audio_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate uploaded audio file.

    Args:
        file_path: Path to uploaded file

    Returns:
        Tuple of (is_valid, message)
    """
    path = Path(file_path)

    # Check extension
    valid_extensions = ['.wav', '.mp3', '.ogg', '.flac', '.m4a', '.opus']
    if path.suffix.lower() not in valid_extensions:
        return False, f"Invalid audio format. Allowed: {', '.join(valid_extensions)}"

    # Check file size (max 50MB)
    if path.stat().st_size > 50_000_000:
        return False, "Audio file too large (max 50MB)"

    return True, "Valid audio file"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and invalid characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove path separators
    filename = filename.replace('/', '_').replace('\\', '_')

    # Remove invalid characters
    invalid_chars = '<>:"|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')

    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')

    # Ensure not empty
    if not filename:
        filename = "unnamed"

    return filename


def create_parameter_presets() -> dict:
    """
    Create preset configurations for TTS parameters.

    Returns:
        Dictionary of preset names and their parameters
    """
    return {
        "Neutral (Default)": {
            "temperature": 0.8,
            "cfg_weight": 0.5,
            "exaggeration": 0.5,
            "repetition_penalty": 1.2,
            "min_p": 0.05,
            "top_p": 1.0
        },
        "Expressive": {
            "temperature": 1.0,
            "cfg_weight": 0.6,
            "exaggeration": 0.8,
            "repetition_penalty": 1.1,
            "min_p": 0.08,
            "top_p": 0.95
        },
        "Very Expressive (Theatrical)": {
            "temperature": 1.2,
            "cfg_weight": 0.5,
            "exaggeration": 1.0,
            "repetition_penalty": 1.0,
            "min_p": 0.10,
            "top_p": 0.90
        },
        "Stable (Monotone)": {
            "temperature": 0.5,
            "cfg_weight": 0.7,
            "exaggeration": 0.3,
            "repetition_penalty": 1.5,
            "min_p": 0.02,
            "top_p": 1.0
        },
        "News Anchor": {
            "temperature": 0.6,
            "cfg_weight": 0.7,
            "exaggeration": 0.4,
            "repetition_penalty": 1.4,
            "min_p": 0.03,
            "top_p": 0.98
        },
        "Audiobook": {
            "temperature": 0.7,
            "cfg_weight": 0.6,
            "exaggeration": 0.6,
            "repetition_penalty": 1.3,
            "min_p": 0.05,
            "top_p": 0.98
        },
        "Audiobook (Dramatic)": {
            "temperature": 0.9,
            "cfg_weight": 0.55,
            "exaggeration": 0.75,
            "repetition_penalty": 1.2,
            "min_p": 0.06,
            "top_p": 0.95
        },
        "Podcast": {
            "temperature": 0.9,
            "cfg_weight": 0.5,
            "exaggeration": 0.7,
            "repetition_penalty": 1.2,
            "min_p": 0.06,
            "top_p": 0.95
        },
        "Conversational": {
            "temperature": 0.85,
            "cfg_weight": 0.5,
            "exaggeration": 0.65,
            "repetition_penalty": 1.1,
            "min_p": 0.05,
            "top_p": 0.95
        },
        "Documentary": {
            "temperature": 0.65,
            "cfg_weight": 0.65,
            "exaggeration": 0.5,
            "repetition_penalty": 1.35,
            "min_p": 0.04,
            "top_p": 0.98
        },
        "Advertisement": {
            "temperature": 0.95,
            "cfg_weight": 0.55,
            "exaggeration": 0.85,
            "repetition_penalty": 1.15,
            "min_p": 0.07,
            "top_p": 0.92
        },
        "Meditation/Calm": {
            "temperature": 0.4,
            "cfg_weight": 0.75,
            "exaggeration": 0.25,
            "repetition_penalty": 1.6,
            "min_p": 0.02,
            "top_p": 1.0
        },
        "Tutorial/Educational": {
            "temperature": 0.7,
            "cfg_weight": 0.6,
            "exaggeration": 0.55,
            "repetition_penalty": 1.3,
            "min_p": 0.04,
            "top_p": 0.97
        },
        "Sports Commentary": {
            "temperature": 1.1,
            "cfg_weight": 0.5,
            "exaggeration": 0.9,
            "repetition_penalty": 1.0,
            "min_p": 0.08,
            "top_p": 0.90
        },
        "Character Voice": {
            "temperature": 1.0,
            "cfg_weight": 0.45,
            "exaggeration": 0.95,
            "repetition_penalty": 1.1,
            "min_p": 0.09,
            "top_p": 0.88
        }
    }


def get_preset_values(preset_name: str) -> Tuple:
    """
    Get parameter values for a given preset.

    Args:
        preset_name: Name of the preset

    Returns:
        Tuple of parameter values (temperature, cfg_weight, exaggeration,
                                   repetition_penalty, min_p, top_p)
    """
    presets = create_parameter_presets()
    params = presets.get(preset_name, presets["Neutral (Default)"])

    return (
        params["temperature"],
        params["cfg_weight"],
        params["exaggeration"],
        params["repetition_penalty"],
        params["min_p"],
        params["top_p"]
    )


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in bytes to human-readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def create_voice_choices(voices_dir: Path) -> List[str]:
    """
    Get list of available voices for dropdown.

    Args:
        voices_dir: Path to voices directory

    Returns:
        List of voice names
    """
    from utils.voice_manager import get_available_voices

    voices = get_available_voices(voices_dir)
    return voices if voices else ["No voices available"]


def create_text_choices(texts_dir: Path) -> List[str]:
    """
    Get list of available text files for dropdown.

    Args:
        texts_dir: Path to texts directory

    Returns:
        List of text file names
    """
    if not texts_dir.exists():
        return ["No texts available"]

    text_files = sorted([f.name for f in texts_dir.glob("*.txt")])
    return text_files if text_files else ["No texts available"]


def estimate_generation_time(char_count: int, is_chunked: bool) -> str:
    """
    Estimate generation time based on text length.

    Args:
        char_count: Number of characters
        is_chunked: Whether text will be processed in chunks

    Returns:
        Estimated time string
    """
    # Rough estimate: ~0.5s per character on GPU, 2s on CPU
    # This is very approximate and depends on hardware
    base_time = char_count * 0.5  # Assuming GPU

    if is_chunked:
        # Add overhead for chunking
        base_time *= 1.2

    if base_time < 60:
        return f"~{int(base_time)}s"
    elif base_time < 3600:
        return f"~{int(base_time/60)}m"
    else:
        return f"~{int(base_time/3600)}h {int((base_time%3600)/60)}m"
