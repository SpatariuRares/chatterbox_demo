"""
Output management utilities for audio file operations.

This module handles combining audio chunks and converting between formats.
"""
import numpy as np
import soundfile as sf
from pathlib import Path
from typing import List, Optional

from utils.audio_utils import convert_to_mp3
import config


def combine_audio_chunks(
    chunk_files: List[Path],
    output_path: Path,
    sample_rate: int,
    cleanup_chunks: bool = True,
    verbose: bool = True
) -> Optional[Path]:
    """
    Combine multiple audio chunks into a single file.

    Args:
        chunk_files: List of paths to chunk files
        output_path: Path where to save the combined audio
        sample_rate: Audio sample rate
        cleanup_chunks: Whether to delete chunk files after combining
        verbose: Whether to print progress information

    Returns:
        Optional[Path]: Path to combined audio file, None if error
    """
    if not chunk_files:
        if verbose:
            print("❌ No chunks to combine")
        return None

    if len(chunk_files) == 1:
        # Only one chunk, just return it
        return chunk_files[0]

    if verbose:
        print(f"\nCombining {len(chunk_files)} chunks...")

    try:
        # Load and concatenate all chunks
        combined_audio = []
        for chunk_file in chunk_files:
            audio, sr = sf.read(str(chunk_file))
            combined_audio.append(audio)

        final_audio = np.concatenate(combined_audio)

        # Save combined file
        sf.write(str(output_path), final_audio, sample_rate)

        if verbose:
            duration = len(final_audio) / sample_rate
            print(f"✓ Combined audio saved: {output_path.name}")
            print(f"  Total duration: {duration:.2f} seconds")

        # Cleanup chunk files if requested
        if cleanup_chunks:
            cleanup_chunk_files(chunk_files, verbose=verbose)
        elif verbose:
            print(f"  Individual chunks kept in: {chunk_files[0].parent}")

        return output_path

    except Exception as e:
        if verbose:
            print(f"❌ Error combining chunks: {e}")
        return None


def cleanup_chunk_files(
    chunk_files: List[Path],
    verbose: bool = True
) -> int:
    """
    Delete chunk files after combining.

    Args:
        chunk_files: List of paths to chunk files to delete
        verbose: Whether to print progress information

    Returns:
        int: Number of files successfully deleted
    """
    if verbose:
        print(f"\nCleaning up {len(chunk_files)} chunk files...")

    deleted_count = 0

    for chunk_file in chunk_files:
        try:
            if chunk_file.exists():
                chunk_file.unlink()
                deleted_count += 1
        except Exception as e:
            if verbose:
                print(f"  ⚠ Could not delete {chunk_file.name}: {e}")

    if verbose:
        print(f"✓ Deleted {deleted_count}/{len(chunk_files)} chunk files")

    return deleted_count


def convert_wav_to_mp3(
    wav_path: Path,
    mp3_path: Path,
    bitrate: str = "192k",
    verbose: bool = True
) -> Optional[Path]:
    """
    Convert WAV file to MP3 format.

    Args:
        wav_path: Path to WAV file
        mp3_path: Path where to save the MP3 file
        bitrate: MP3 bitrate (default: "192k")
        verbose: Whether to print progress information

    Returns:
        Optional[Path]: Path to MP3 file if successful, None otherwise
    """
    try:
        mp3_result = convert_to_mp3(
            str(wav_path),
            str(mp3_path),
            bitrate=bitrate
        )

        if verbose:
            print(f"✓ MP3 file saved: {mp3_path.name}")

        return Path(mp3_result)

    except FileNotFoundError:
        if verbose:
            print("\n⚠ ffmpeg not installed - MP3 conversion skipped")
            print("The WAV file is available and ready to use.")
            print("\nTo enable MP3 conversion:")
            print("  1. Install ffmpeg: https://ffmpeg.org/download.html")
            print("  2. Or use: winget install ffmpeg")
            print("  3. Restart the terminal")
        return None

    except Exception as e:
        if verbose:
            print(f"\n⚠ Error during MP3 conversion: {e}")
            print("The WAV file is available.")
        return None


def generate_output_filenames(
    voice_name: str,
    text_basename: str,
    is_chunked: bool = False
) -> dict:
    """
    Generate standardized output filenames.

    Args:
        voice_name: Name of the voice used
        text_basename: Base name of the text file (without extension)
        is_chunked: Whether the audio was generated in chunks

    Returns:
        dict: Dictionary with 'wav' and 'mp3' filename keys
    """
    suffix = "_full" if is_chunked else ""

    return {
        'wav': f"{voice_name}_{text_basename}{suffix}.wav",
        'mp3': f"{voice_name}_{text_basename}{suffix}.mp3",
        'base': f"{voice_name}_{text_basename}"
    }


def save_generation_summary(
    output_dir: Path,
    voice_name: str,
    text_file: str,
    text_length: int,
    wav_path: Path,
    mp3_path: Optional[Path] = None,
    chunk_count: int = 0
) -> None:
    """
    Save a summary file with generation details.

    Args:
        output_dir: Directory where to save the summary
        voice_name: Name of the voice used
        text_file: Name of the text file
        text_length: Length of the text in characters
        wav_path: Path to generated WAV file
        mp3_path: Path to generated MP3 file (if any)
        chunk_count: Number of chunks generated (0 for single-pass)
    """
    summary_path = output_dir / f"{voice_name}_{text_file.replace('.txt', '')}_summary.txt"

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("CHATTERBOX TTS - Generation Summary\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Voice: {voice_name}\n")
        f.write(f"Text file: {text_file}\n")
        f.write(f"Text length: {text_length} characters\n")
        f.write(f"Processing mode: {'Chunked' if chunk_count > 0 else 'Single-pass'}\n")

        if chunk_count > 0:
            f.write(f"Number of chunks: {chunk_count}\n")

        f.write("\nGeneration Parameters:\n")
        f.write(f"  Language: {config.LANGUAGE_ID}\n")
        f.write(f"  Temperature: {config.TEMPERATURE}\n")
        f.write(f"  CFG Weight: {config.CFG_WEIGHT}\n")
        f.write(f"  Exaggeration: {config.EXAGGERATION}\n")

        f.write("\nGenerated Files:\n")
        f.write(f"  WAV: {wav_path.name}\n")
        if mp3_path and mp3_path.exists():
            f.write(f"  MP3: {mp3_path.name}\n")

    print(f"\n✓ Summary saved: {summary_path.name}")
