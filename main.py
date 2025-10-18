"""
Chatterbox TTS Demo - Voice Synthesis with Multiple Audio References

This script demonstrates how to use Chatterbox TTS to generate speech
using multiple audio files as voice references.
Automatically handles both short and long texts by splitting into chunks when needed.
"""
from pathlib import Path
from typing import Optional

from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from utils.audio_utils import concatenate_audio_files
from utils.text_utils import read_text_from_file
from utils.voice_manager import get_available_voices, validate_voice
from utils.setup_utils import detect_device, setup_directories, print_section
from utils.audio_generator import (
    generate_single_audio,
    generate_chunked_audio,
    print_generation_params
)
from utils.output_manager import (
    combine_audio_chunks,
    convert_wav_to_mp3,
    generate_output_filenames,
    save_generation_summary
)
import config


# Constants
MAX_SINGLE_PASS_CHARS = 500


def validate_and_get_voice() -> Optional[Path]:
    """
    Detect, list, and validate the selected voice.

    Returns:
        Optional[Path]: Path to voice folder if valid, None otherwise
    """
    print_section("VOICE DETECTION")

    available_voices = get_available_voices(config.VOICES_DIR)

    if not available_voices:
        print(f"\n❌ ERROR: No voices found in {config.VOICES_DIR}")
        print(f"\nCreate a folder in {config.VOICES_DIR}/ and add audio files.")
        print("Example: input/voice/myVoice/audio1.wav")
        return None

    print(f"\n✓ Available voices ({len(available_voices)}):")
    for voice in available_voices:
        print(f"  - {voice}")

    # Validate selected voice
    print(f"\n🎤 Selected voice: {config.SELECTED_VOICE}")

    is_valid, result = validate_voice(config.VOICES_DIR, config.SELECTED_VOICE)
    if not is_valid:
        print(f"\n❌ ERROR: {result}")
        print(f"\nAvailable voices: {', '.join(available_voices)}")
        print(f"Update SELECTED_VOICE in config.py")
        return None

    voice_folder = result
    print(f"✓ Voice path: {voice_folder}")
    return voice_folder


def prepare_audio_reference(voice_folder: Path) -> Optional[str]:
    """
    Concatenate audio reference files into a single file.

    Args:
        voice_folder: Path to folder containing voice reference files

    Returns:
        Optional[str]: Path to combined audio file, None if error
    """
    print_section("STEP 1: Concatenating Audio Reference Files")

    combined_audio_path = config.OUTPUT_DIR / f"{config.SELECTED_VOICE}_{config.COMBINED_AUDIO_NAME}"

    try:
        combined_audio_path = concatenate_audio_files(
            audio_folder=voice_folder,
            output_path=str(combined_audio_path),
            target_sr=config.SAMPLE_RATE
        )
        return combined_audio_path
    except ValueError as e:
        print(f"\n❌ ERROR: {e}")
        return None


def load_text_file() -> Optional[str]:
    """
    Load text from the configured text file.

    Returns:
        Optional[str]: Text content if successful, None otherwise
    """
    print_section("STEP 2: Loading Text to Synthesize")

    text_file_path = config.TEXT_DIR / config.SELECTED_TEXT_FILE
    print(f"Text file: {config.SELECTED_TEXT_FILE}")

    try:
        text = read_text_from_file(text_file_path)
        print(f"Text loaded: {len(text)} characters")

        if len(text) <= 100:
            print(f"Content: {text}")
        else:
            print(f"Preview: {text[:100]}...")

        return text

    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print(f"Make sure the file exists in: {config.TEXT_DIR}")
        print(f"Available files:")

        if config.TEXT_DIR.exists():
            text_files = list(config.TEXT_DIR.glob("*.txt"))
            for tf in text_files:
                print(f"  - {tf.name}")

        return None


def process_short_text(
    model: ChatterboxMultilingualTTS,
    text: str,
    audio_prompt_path: str,
    filenames: dict
) -> Optional[Path]:
    """
    Process short text with single-pass generation.

    Args:
        model: TTS model instance
        text: Text to synthesize
        audio_prompt_path: Path to audio reference
        filenames: Dictionary with output filenames

    Returns:
        Optional[Path]: Path to generated WAV file
    """
    print_section("STEP 3: Speech Synthesis (Single-pass)")
    print_generation_params()

    output_wav_path = config.OUTPUT_WAV_DIR / filenames['wav']

    return generate_single_audio(
        model=model,
        text=text,
        audio_prompt_path=audio_prompt_path,
        output_path=output_wav_path,
        verbose=True
    )


def process_long_text(
    model: ChatterboxMultilingualTTS,
    text: str,
    audio_prompt_path: str,
    filenames: dict
) -> tuple[Optional[Path], int]:
    """
    Process long text with chunked generation.

    Args:
        model: TTS model instance
        text: Text to synthesize
        audio_prompt_path: Path to audio reference
        filenames: Dictionary with output filenames

    Returns:
        tuple: (Path to final combined WAV file, number of chunks generated)
    """
    print_section("STEP 3: Speech Synthesis (Chunked Mode)")

    # Generate chunks
    chunk_files = generate_chunked_audio(
        model=model,
        text=text,
        audio_prompt_path=audio_prompt_path,
        output_dir=config.OUTPUT_WAV_DIR,
        base_filename=filenames['base'],
        max_chars=MAX_SINGLE_PASS_CHARS,
        verbose=True
    )

    if not chunk_files:
        print("\n❌ No chunks generated")
        return None, 0

    chunk_count = len(chunk_files)

    # Combine chunks
    print_section("STEP 4: Combining Chunks")

    output_wav_path = config.OUTPUT_WAV_DIR / filenames['wav']

    combined_path = combine_audio_chunks(
        chunk_files=chunk_files,
        output_path=output_wav_path,
        sample_rate=model.sr,
        cleanup_chunks=config.CLEANUP_CHUNKS,
        verbose=True
    )

    return combined_path, chunk_count


def print_summary(
    text: str,
    combined_audio_path: str,
    output_wav: Path,
    output_mp3: Optional[Path],
    is_long_text: bool
) -> None:
    """
    Print final summary of generated files.

    Args:
        text: Original text that was synthesized
        combined_audio_path: Path to audio reference file
        output_wav: Path to generated WAV file
        output_mp3: Path to generated MP3 file (if any)
        is_long_text: Whether text was processed as long text
    """
    print_section("COMPLETED!")

    print(f"\nVoice used: {config.SELECTED_VOICE}")
    print(f"Text: {config.SELECTED_TEXT_FILE} ({len(text)} characters)")
    print(f"Processing mode: {'Chunked' if is_long_text else 'Single-pass'}")
    print(f"\nGenerated files:")
    print(f"  - Audio reference: {combined_audio_path}")
    print(f"  - Speech synthesis WAV: {output_wav}")

    if output_mp3 and output_mp3.exists():
        print(f"  - Speech synthesis MP3: {output_mp3}")

    print()


def main() -> None:
    """Main function to run the TTS pipeline."""
    # Setup
    print_section("CHATTERBOX TTS - Voice Synthesis Demo")

    # Detect device
    device = detect_device(config.DEVICE)
    print(f"\nUsing device: {device}")

    # Create directories
    setup_directories(
        config.VOICES_DIR,
        config.OUTPUT_DIR,
        config.OUTPUT_WAV_DIR,
        config.OUTPUT_MP3_DIR
    )

    # Validate voice
    voice_folder = validate_and_get_voice()
    if voice_folder is None:
        return

    # Load model
    print_section("LOADING MODEL")
    model = ChatterboxMultilingualTTS.from_pretrained(device=device)

    # Prepare audio reference
    combined_audio_path = prepare_audio_reference(voice_folder)
    if combined_audio_path is None:
        return

    # Load text
    text = load_text_file()
    if text is None:
        return

    # Determine processing mode
    text_basename = config.SELECTED_TEXT_FILE.replace('.txt', '')
    is_long_text = len(text) > MAX_SINGLE_PASS_CHARS

    # Generate output filenames
    filenames = generate_output_filenames(
        voice_name=config.SELECTED_VOICE,
        text_basename=text_basename,
        is_chunked=is_long_text
    )

    # Process text based on length
    chunk_count = 0
    if is_long_text:
        print(f"\n📚 Mode: LONG TEXT (chunked processing)")
        print(f"Text will be split into chunks of max {MAX_SINGLE_PASS_CHARS} characters")
        output_wav, chunk_count = process_long_text(model, text, combined_audio_path, filenames)
    else:
        print(f"\n📝 Mode: SHORT TEXT (single-pass)")
        output_wav = process_short_text(model, text, combined_audio_path, filenames)

    if output_wav is None:
        print("\n❌ Audio generation failed")
        return

    # Convert to MP3
    print_section("MP3 CONVERSION (optional)")

    output_mp3_path = config.OUTPUT_MP3_DIR / filenames['mp3']
    output_mp3 = convert_wav_to_mp3(
        wav_path=output_wav,
        mp3_path=output_mp3_path,
        bitrate=config.MP3_BITRATE,
        verbose=True
    )

    # Save summary file
    save_generation_summary(
        output_dir=config.OUTPUT_DIR,
        voice_name=config.SELECTED_VOICE,
        text_file=config.SELECTED_TEXT_FILE,
        text_length=len(text),
        wav_path=output_wav,
        mp3_path=output_mp3,
        chunk_count=chunk_count
    )

    # Print summary
    print_summary(text, combined_audio_path, output_wav, output_mp3, is_long_text)


if __name__ == "__main__":
    main()
