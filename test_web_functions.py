"""
Test script for web interface functions.

This script tests the main utility functions without launching the Gradio UI.
Useful for debugging and validation.
"""

from pathlib import Path
from utils.gradio_helpers import (
    format_duration,
    sanitize_filename,
    create_parameter_presets,
    validate_text_file,
    validate_audio_file
)
from utils.voice_manager import (
    get_available_voices,
    get_voice_details
)
from utils.history_manager import HistoryManager
import config


def test_voice_detection():
    """Test voice detection."""
    print("\n=== Testing Voice Detection ===")
    voices = get_available_voices(config.VOICES_DIR)
    print(f"Found {len(voices)} voices: {voices}")

    for voice in voices:
        details = get_voice_details(config.VOICES_DIR, voice)
        if details:
            print(f"\nVoice: {voice}")
            print(f"  - Audio files: {details['audio_count']}")
            print(f"  - Duration: {format_duration(details['total_duration'])}")
            print(f"  - Files: {[f['name'] for f in details['files']]}")


def test_text_detection():
    """Test text file detection."""
    print("\n=== Testing Text Detection ===")

    if not config.TEXT_DIR.exists():
        print("Text directory not found")
        return

    text_files = sorted(config.TEXT_DIR.glob("*.txt"))
    print(f"Found {len(text_files)} text files")

    for text_file in text_files:
        with open(text_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n{text_file.name}:")
        print(f"  - Length: {len(content)} characters")
        print(f"  - Preview: {content[:50]}...")


def test_parameter_presets():
    """Test parameter presets."""
    print("\n=== Testing Parameter Presets ===")
    presets = create_parameter_presets()

    for preset_name, params in presets.items():
        print(f"\n{preset_name}:")
        for param, value in params.items():
            print(f"  - {param}: {value}")


def test_filename_sanitization():
    """Test filename sanitization."""
    print("\n=== Testing Filename Sanitization ===")

    test_names = [
        "Normal Name",
        "Name/With\\Slashes",
        "Name:With:Colons",
        "<Invalid>Name",
        "Name|With|Pipes",
        "...dots...",
        "  spaces  "
    ]

    for name in test_names:
        sanitized = sanitize_filename(name)
        print(f"{name:30} -> {sanitized}")


def test_history_manager():
    """Test history manager."""
    print("\n=== Testing History Manager ===")

    # Create test history
    history_file = config.OUTPUT_DIR / "test_history.json"
    hm = HistoryManager(history_file)

    # Add test generation
    hm.add_generation(
        voice_name="testVoice",
        text_source="testText.txt",
        text_length=250,
        wav_path="output/wav/test.wav",
        mp3_path="output/mp3/test.mp3",
        chunk_count=0,
        parameters={
            'temperature': 0.8,
            'cfg_weight': 0.5
        }
    )

    # Get all generations
    generations = hm.get_all_generations()
    print(f"Total generations: {len(generations)}")

    # Get statistics
    stats = hm.get_statistics()
    print(f"\nStatistics:")
    for key, value in stats.items():
        print(f"  - {key}: {value}")

    # Clean up test file
    if history_file.exists():
        history_file.unlink()
        print(f"\nTest history file removed: {history_file}")


def test_directory_structure():
    """Test and create directory structure."""
    print("\n=== Testing Directory Structure ===")

    directories = [
        config.VOICES_DIR,
        config.TEXT_DIR,
        config.OUTPUT_DIR,
        config.OUTPUT_WAV_DIR,
        config.OUTPUT_MP3_DIR
    ]

    for directory in directories:
        exists = directory.exists()
        status = "✓ Exists" if exists else "✗ Missing"
        print(f"{status}: {directory}")

        if not exists:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  -> Created: {directory}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("CHATTERBOX TTS STUDIO - Function Tests")
    print("=" * 60)

    try:
        test_directory_structure()
        test_voice_detection()
        test_text_detection()
        test_parameter_presets()
        test_filename_sanitization()
        test_history_manager()

        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)

    except Exception as e:
        import traceback
        print(f"\n❌ Error during tests: {e}")
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
