"""
Audio generation utilities for Chatterbox TTS.

This module handles the generation of speech audio from text,
including both single-pass and chunked processing for long texts.
"""
import torch
import torchaudio as ta
from pathlib import Path
from typing import Optional, List

from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from utils.text_splitter import split_text_smart
import config


def generate_audio_chunk(
    model: ChatterboxMultilingualTTS,
    text: str,
    audio_prompt_path: str
) -> torch.Tensor:
    """
    Generate audio for a single text chunk.

    Args:
        model: TTS model instance
        text: Text to synthesize
        audio_prompt_path: Path to audio reference file

    Returns:
        torch.Tensor: Generated audio waveform
    """
    return model.generate(
        text,
        language_id=config.LANGUAGE_ID,
        audio_prompt_path=audio_prompt_path,
        temperature=config.TEMPERATURE,
        cfg_weight=config.CFG_WEIGHT,
        exaggeration=config.EXAGGERATION,
        repetition_penalty=config.REPETITION_PENALTY,
        min_p=config.MIN_P,
        top_p=config.TOP_P,
    )


def save_audio_chunk(
    wav: torch.Tensor,
    sample_rate: int,
    output_path: Path
) -> str:
    """
    Save a single audio chunk to file.

    Args:
        wav: Audio waveform tensor
        sample_rate: Audio sample rate
        output_path: Path where to save the audio file

    Returns:
        str: Path to saved chunk file
    """
    ta.save(str(output_path), wav, sample_rate)
    return str(output_path)


def generate_single_audio(
    model: ChatterboxMultilingualTTS,
    text: str,
    audio_prompt_path: str,
    output_path: Path,
    verbose: bool = True
) -> Optional[Path]:
    """
    Generate audio for short text (single pass).

    Args:
        model: TTS model instance
        text: Text to synthesize
        audio_prompt_path: Path to audio reference file
        output_path: Path where to save the generated audio
        verbose: Whether to print progress information

    Returns:
        Optional[Path]: Path to generated WAV file
    """
    if verbose:
        print("\nGenerating audio...")

    try:
        wav = generate_audio_chunk(model, text, audio_prompt_path)
        save_audio_chunk(wav, model.sr, output_path)

        if verbose:
            print(f"✓ Audio saved: {output_path.name}")

        return output_path

    except Exception as e:
        if verbose:
            print(f"❌ Error generating audio: {e}")
        return None


def generate_chunked_audio(
    model: ChatterboxMultilingualTTS,
    text: str,
    audio_prompt_path: str,
    output_dir: Path,
    base_filename: str,
    max_chars: int = 500,
    verbose: bool = True
) -> List[Path]:
    """
    Generate audio for long text (chunked processing).

    Args:
        model: TTS model instance
        text: Text to synthesize
        audio_prompt_path: Path to audio reference file
        output_dir: Directory where to save the chunks
        base_filename: Base name for chunk files (without extension)
        max_chars: Maximum characters per chunk
        verbose: Whether to print progress information

    Returns:
        List[Path]: List of paths to generated chunk files
    """
    # Split text into chunks
    chunks = split_text_smart(text, max_chars=max_chars, method='sentences')

    if verbose:
        print(f"\n✓ Text split into {len(chunks)} chunks")
        avg_length = sum(len(c) for c in chunks) // len(chunks)
        print(f"Average chunk length: {avg_length} characters")

    chunk_files = []

    for i, chunk in enumerate(chunks, 1):
        if verbose:
            print(f"\n[{i}/{len(chunks)}] Generating chunk {i}...")
            print(f"  Characters: {len(chunk)}")
            print(f"  Preview: {chunk[:60]}...")

        try:
            # Generate audio for chunk
            wav = generate_audio_chunk(model, chunk, audio_prompt_path)

            # Save chunk
            chunk_filename = f"{base_filename}_chunk{i:03d}.wav"
            chunk_path = output_dir / chunk_filename
            save_audio_chunk(wav, model.sr, chunk_path)

            chunk_files.append(chunk_path)

            if verbose:
                print(f"  ✓ Saved: {chunk_filename}")

        except Exception as e:
            if verbose:
                print(f"  ❌ Error: {e}")
            continue

    return chunk_files


def print_generation_params() -> None:
    """Print current generation parameters."""
    print(f"Voice: {config.SELECTED_VOICE}")
    print(f"Language: {config.LANGUAGE_ID}")
    print(f"Temperature: {config.TEMPERATURE}")
    print(f"CFG Weight: {config.CFG_WEIGHT}")
    print(f"Exaggeration: {config.EXAGGERATION}")
