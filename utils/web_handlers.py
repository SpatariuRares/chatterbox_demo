"""
Handler functions for Gradio web interface.

This module contains all the business logic handlers for the web interface,
separated from UI construction for better maintainability.
"""

import gradio as gr
from pathlib import Path
from typing import Optional, List, Tuple
import shutil

from utils.audio_utils import concatenate_audio_files
from utils.text_utils import read_text_from_file
from utils.voice_manager import (
    get_available_voices,
    get_voice_details,
    create_voice,
    add_audio_to_voice,
    delete_voice
)
from utils.audio_generator import (
    generate_single_audio,
    generate_chunked_audio
)
from utils.output_manager import (
    combine_audio_chunks,
    convert_wav_to_mp3,
    generate_output_filenames
)
from utils.gradio_helpers import (
    format_duration,
    get_voice_info_display,
    get_text_info_display,
    validate_text_file,
    validate_audio_file,
    sanitize_filename,
    create_voice_choices,
    create_text_choices
)
from utils.history_manager import HistoryManager
import config

# Constants
MAX_SINGLE_PASS_CHARS = 500
history_manager = HistoryManager(config.OUTPUT_DIR / "generation_history.json")


# =============================================================================
# GENERATION HANDLERS (Tab 1)
# =============================================================================

def refresh_voice_dropdown():
    """Refresh the list of available voices."""
    voices = create_voice_choices(config.VOICES_DIR)
    return gr.Dropdown(choices=voices, value=voices[0] if voices else None)


def refresh_all_voice_dropdowns():
    """Refresh all voice dropdowns (for auto-update after CRUD operations)."""
    voices = create_voice_choices(config.VOICES_DIR)
    dropdown = gr.Dropdown(choices=voices, value=voices[0] if voices else None)
    # Return same dropdown 3 times (for gen, add, delete)
    return dropdown, dropdown, dropdown


def refresh_text_dropdown():
    """Refresh the list of available text files."""
    texts = create_text_choices(config.TEXT_DIR)
    return gr.Dropdown(choices=texts, value=texts[0] if texts else None)


def refresh_all_text_dropdowns():
    """Refresh all text dropdowns (for auto-update after CRUD operations)."""
    texts = create_text_choices(config.TEXT_DIR)
    dropdown = gr.Dropdown(choices=texts, value=texts[0] if texts else None)
    # Return same dropdown 2 times (for gen, delete)
    return dropdown, dropdown


def update_voice_info(voice_name: str) -> str:
    """Update voice information display."""
    if not voice_name or voice_name == "No voices available":
        return "No voice selected"
    return get_voice_info_display(voice_name, config.VOICES_DIR)


def update_text_info(text_file: str) -> str:
    """Update text information display."""
    if not text_file or text_file == "No texts available":
        return "No text selected"

    try:
        text_path = config.TEXT_DIR / text_file
        text = read_text_from_file(text_path)
        return get_text_info_display(text, MAX_SINGLE_PASS_CHARS)
    except Exception as e:
        return f"Error loading text: {e}"


def generate_tts(
    model,
    voice_name: str,
    text_file: str,
    temperature: float,
    cfg_weight: float,
    exaggeration: float,
    repetition_penalty: float,
    min_p: float,
    top_p: float,
    progress=gr.Progress()
) -> Tuple[Optional[str], Optional[str], str]:
    """
    Generate TTS audio from selected voice and text.

    Returns:
        Tuple of (wav_path, mp3_path, status_message)
    """
    try:
        # Validation
        if not voice_name or voice_name == "No voices available":
            return None, None, "Please select a voice"

        if not text_file or text_file == "No texts available":
            return None, None, "Please select a text file"

        progress(0.1, desc="Loading text and preparing voice...")

        # Load text
        text_path = config.TEXT_DIR / text_file
        text = read_text_from_file(text_path)

        # Prepare audio reference
        voice_folder = config.VOICES_DIR / voice_name
        combined_audio_path = config.OUTPUT_DIR / f"{voice_name}_{config.COMBINED_AUDIO_NAME}"

        progress(0.2, desc="Concatenating voice references...")
        combined_audio_path = concatenate_audio_files(
            audio_folder=voice_folder,
            output_path=str(combined_audio_path),
            target_sr=config.SAMPLE_RATE
        )

        # Determine processing mode
        text_basename = text_file.replace('.txt', '')
        is_long_text = len(text) > MAX_SINGLE_PASS_CHARS

        # Generate filenames
        filenames = generate_output_filenames(
            voice_name=voice_name,
            text_basename=text_basename,
            is_chunked=is_long_text
        )

        # Generate audio
        chunk_count = 0
        if is_long_text:
            progress(0.3, desc=f"Generating audio (chunked mode)...")

            chunk_files = generate_chunked_audio(
                model=model,
                text=text,
                audio_prompt_path=combined_audio_path,
                output_dir=config.OUTPUT_WAV_DIR,
                base_filename=filenames['base'],
                max_chars=MAX_SINGLE_PASS_CHARS,
                temperature=temperature,
                cfg_weight=cfg_weight,
                exaggeration=exaggeration,
                repetition_penalty=repetition_penalty,
                min_p=min_p,
                top_p=top_p,
                verbose=False
            )

            if not chunk_files:
                return None, None, "Failed to generate audio chunks"

            chunk_count = len(chunk_files)

            progress(0.7, desc=f"Combining {chunk_count} chunks...")

            output_wav_path = config.OUTPUT_WAV_DIR / filenames['wav']
            output_wav_path = combine_audio_chunks(
                chunk_files=chunk_files,
                output_path=output_wav_path,
                sample_rate=model.sr,
                cleanup_chunks=config.CLEANUP_CHUNKS,
                verbose=False
            )
        else:
            progress(0.3, desc="Generating audio (single-pass)...")

            output_wav_path = config.OUTPUT_WAV_DIR / filenames['wav']
            output_wav_path = generate_single_audio(
                model=model,
                text=text,
                audio_prompt_path=combined_audio_path,
                output_path=output_wav_path,
                temperature=temperature,
                cfg_weight=cfg_weight,
                exaggeration=exaggeration,
                repetition_penalty=repetition_penalty,
                min_p=min_p,
                top_p=top_p,
                verbose=False
            )

        if output_wav_path is None:
            return None, None, "Audio generation failed"

        progress(0.85, desc="Converting to MP3...")

        # Convert to MP3
        output_mp3_path = config.OUTPUT_MP3_DIR / filenames['mp3']
        output_mp3_path = convert_wav_to_mp3(
            wav_path=output_wav_path,
            mp3_path=output_mp3_path,
            bitrate=config.MP3_BITRATE,
            verbose=False
        )

        progress(0.95, desc="Saving to history...")

        # Save to history
        parameters = {
            'temperature': temperature,
            'cfg_weight': cfg_weight,
            'exaggeration': exaggeration,
            'repetition_penalty': repetition_penalty,
            'min_p': min_p,
            'top_p': top_p
        }

        history_manager.add_generation(
            voice_name=voice_name,
            text_source=text_file,
            text_length=len(text),
            wav_path=str(output_wav_path),
            mp3_path=str(output_mp3_path) if output_mp3_path else None,
            chunk_count=chunk_count,
            parameters=parameters
        )

        progress(1.0, desc="Complete!")

        # Return audio paths
        wav_audio = str(output_wav_path)
        mp3_audio = str(output_mp3_path) if output_mp3_path else None

        mode = "chunked" if is_long_text else "single-pass"
        status = f"✓ Generation complete! ({mode}, {len(text)} chars"
        if chunk_count > 0:
            status += f", {chunk_count} chunks"
        status += ")"

        return wav_audio, mp3_audio, status

    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return None, None, f"Generation failed: {str(e)}"


# =============================================================================
# VOICE MANAGEMENT HANDLERS (Tab 2)
# =============================================================================

def list_voices_details() -> str:
    """Get detailed list of all voices."""
    voices = get_available_voices(config.VOICES_DIR)

    if not voices:
        return "No voices available"

    output = "# Available Voices\n\n"
    for voice in voices:
        details = get_voice_details(config.VOICES_DIR, voice)
        if details:
            output += f"## {voice}\n"
            output += f"- Audio files: {details['audio_count']}\n"
            output += f"- Total duration: {format_duration(details['total_duration'])}\n"
            output += f"- Files:\n"
            for file_info in details['files']:
                output += f"  - {file_info['name']} ({format_duration(file_info['duration'])})\n"
            output += "\n"

    return output


def create_new_voice(voice_name: str, audio_files: List) -> str:
    """Create a new voice."""
    if not voice_name:
        return "Please enter a voice name"

    if not audio_files:
        return "Please upload at least one audio file"

    voice_name = sanitize_filename(voice_name)

    file_paths = []
    for audio_file in audio_files:
        is_valid, msg = validate_audio_file(audio_file.name)
        if not is_valid:
            return f"Invalid file {audio_file.name}: {msg}"
        file_paths.append(audio_file.name)

    success, message = create_voice(config.VOICES_DIR, voice_name, file_paths)

    if success:
        return f"✓ {message}"
    else:
        return f"✗ {message}"


def add_audio_files_to_voice(voice_name: str, audio_files: List) -> str:
    """Add audio files to existing voice."""
    if not voice_name:
        return "Please select a voice"

    if not audio_files:
        return "Please upload at least one audio file"

    file_paths = [f.name for f in audio_files]
    success, message = add_audio_to_voice(config.VOICES_DIR, voice_name, file_paths)

    if success:
        return f"✓ {message}"
    else:
        return f"✗ {message}"


def delete_selected_voice(voice_name: str) -> str:
    """Delete a voice."""
    if not voice_name:
        return "Please select a voice to delete"

    success, message = delete_voice(config.VOICES_DIR, voice_name)

    if success:
        return f"✓ {message}"
    else:
        return f"✗ {message}"


# =============================================================================
# TEXT MANAGEMENT HANDLERS (Tab 3)
# =============================================================================

def list_texts_details() -> str:
    """Get detailed list of all text files."""
    if not config.TEXT_DIR.exists():
        return "Text directory not found"

    text_files = sorted(config.TEXT_DIR.glob("*.txt"))

    if not text_files:
        return "No text files available"

    output = "# Available Texts\n\n"
    for text_file in text_files:
        try:
            text = read_text_from_file(text_file)
            char_count = len(text)
            is_long = char_count > MAX_SINGLE_PASS_CHARS
            mode = "CHUNKED" if is_long else "SINGLE-PASS"

            output += f"## {text_file.name}\n"
            output += f"- Length: {char_count} characters\n"
            output += f"- Mode: {mode}\n"
            if is_long:
                chunks = (char_count + MAX_SINGLE_PASS_CHARS - 1) // MAX_SINGLE_PASS_CHARS
                output += f"- Estimated chunks: {chunks}\n"
            output += f"- Preview: {text[:100]}...\n\n"
        except Exception as e:
            output += f"## {text_file.name}\n- Error: {e}\n\n"

    return output


def save_text_from_input(text_name: str, text_content: str) -> str:
    """Save text from textbox input."""
    if not text_name:
        return "Please enter a name for the text"

    if not text_content or not text_content.strip():
        return "Please enter some text content"

    text_name = sanitize_filename(text_name)
    if not text_name.endswith('.txt'):
        text_name += '.txt'

    text_path = config.TEXT_DIR / text_name

    try:
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_content.strip())
        return f"✓ Text saved as {text_name} ({len(text_content)} characters)"
    except Exception as e:
        return f"✗ Failed to save text: {e}"


def save_uploaded_text(text_file) -> str:
    """Save uploaded text file."""
    if not text_file:
        return "Please upload a text file"

    is_valid, msg = validate_text_file(text_file.name)
    if not is_valid:
        return f"✗ {msg}"

    src = Path(text_file.name)
    dst = config.TEXT_DIR / sanitize_filename(src.name)

    try:
        shutil.copy2(src, dst)
        with open(dst, 'r', encoding='utf-8') as f:
            char_count = len(f.read())
        return f"✓ Text file uploaded: {dst.name} ({char_count} characters)"
    except Exception as e:
        return f"✗ Failed to upload text: {e}"


def delete_text_file(text_file: str) -> str:
    """Delete a text file."""
    if not text_file:
        return "Please select a text file to delete"

    text_path = config.TEXT_DIR / text_file

    try:
        text_path.unlink()
        return f"✓ Deleted {text_file}"
    except Exception as e:
        return f"✗ Failed to delete text: {e}"


# =============================================================================
# BATCH PROCESSING HANDLERS (Tab 4)
# =============================================================================

def batch_generate(
    model,
    voice_name: str,
    text_files: List,
    temperature: float,
    cfg_weight: float,
    exaggeration: float,
    repetition_penalty: float,
    min_p: float,
    top_p: float,
    progress=gr.Progress()
) -> str:
    """Generate TTS for multiple text files."""
    if not voice_name or voice_name == "No voices available":
        return "Please select a voice"

    if not text_files:
        return "Please upload text files for batch processing"

    results = []
    total_files = len(text_files)

    for idx, text_file in enumerate(text_files):
        progress((idx / total_files), desc=f"Processing {idx+1}/{total_files}...")

        try:
            with open(text_file.name, 'r', encoding='utf-8') as f:
                text = f.read()

            voice_folder = config.VOICES_DIR / voice_name
            combined_audio_path = config.OUTPUT_DIR / f"{voice_name}_{config.COMBINED_AUDIO_NAME}"
            combined_audio_path = concatenate_audio_files(
                audio_folder=voice_folder,
                output_path=str(combined_audio_path),
                target_sr=config.SAMPLE_RATE
            )

            text_basename = Path(text_file.name).stem
            is_long_text = len(text) > MAX_SINGLE_PASS_CHARS
            filenames = generate_output_filenames(
                voice_name=voice_name,
                text_basename=text_basename,
                is_chunked=is_long_text
            )

            if is_long_text:
                chunk_files = generate_chunked_audio(
                    model=model,
                    text=text,
                    audio_prompt_path=combined_audio_path,
                    output_dir=config.OUTPUT_WAV_DIR,
                    base_filename=filenames['base'],
                    max_chars=MAX_SINGLE_PASS_CHARS,
                    temperature=temperature,
                    cfg_weight=cfg_weight,
                    exaggeration=exaggeration,
                    repetition_penalty=repetition_penalty,
                    min_p=min_p,
                    top_p=top_p,
                    verbose=False
                )

                output_wav_path = config.OUTPUT_WAV_DIR / filenames['wav']
                output_wav_path = combine_audio_chunks(
                    chunk_files=chunk_files,
                    output_path=output_wav_path,
                    sample_rate=model.sr,
                    cleanup_chunks=config.CLEANUP_CHUNKS,
                    verbose=False
                )
            else:
                output_wav_path = config.OUTPUT_WAV_DIR / filenames['wav']
                output_wav_path = generate_single_audio(
                    model=model,
                    text=text,
                    audio_prompt_path=combined_audio_path,
                    output_path=output_wav_path,
                    temperature=temperature,
                    cfg_weight=cfg_weight,
                    exaggeration=exaggeration,
                    repetition_penalty=repetition_penalty,
                    min_p=min_p,
                    top_p=top_p,
                    verbose=False
                )

            output_mp3_path = config.OUTPUT_MP3_DIR / filenames['mp3']
            convert_wav_to_mp3(
                wav_path=output_wav_path,
                mp3_path=output_mp3_path,
                bitrate=config.MP3_BITRATE,
                verbose=False
            )

            results.append(f"✓ {text_basename}: {len(text)} chars → {filenames['wav']}")

        except Exception as e:
            results.append(f"✗ {Path(text_file.name).stem}: Error - {str(e)}")

    progress(1.0, desc="Batch processing complete!")

    output = f"# Batch Processing Results ({total_files} files)\n\n"
    output += "\n".join(results)
    output += f"\n\nFiles saved to:\n- WAV: {config.OUTPUT_WAV_DIR}\n- MP3: {config.OUTPUT_MP3_DIR}"

    return output


# =============================================================================
# HISTORY HANDLERS (Tab 5)
# =============================================================================

def display_history() -> str:
    """Display generation history."""
    history = history_manager.get_all_generations()

    if not history:
        return "No generation history"

    output = "# Generation History\n\n"
    for record in history:
        output += f"## ID: {record['id']} - {record.get('timestamp', 'N/A')}\n"
        output += f"- Voice: {record.get('voice_name', 'N/A')}\n"
        output += f"- Text: {record.get('text_source', 'N/A')} ({record.get('text_length', 0)} chars)\n"
        output += f"- Mode: {record.get('mode', 'N/A')}\n"
        if record.get('chunk_count', 0) > 0:
            output += f"- Chunks: {record['chunk_count']}\n"
        output += f"- WAV: {record.get('wav_path', 'N/A')}\n"
        if record.get('mp3_path'):
            output += f"- MP3: {record['mp3_path']}\n"
        output += "\n"

    return output


def display_statistics() -> str:
    """Display generation statistics."""
    stats = history_manager.get_statistics()

    output = "# Statistics\n\n"
    output += f"- Total generations: {stats['total_generations']}\n"
    output += f"- Unique voices used: {stats['unique_voices']}\n"
    output += f"- Total characters processed: {stats['total_characters']:,}\n"
    output += f"- Chunked generations: {stats['chunked_generations']}\n"
    output += f"- Single-pass generations: {stats['single_pass_generations']}\n"

    if stats.get('voices_used'):
        output += f"\nVoices used:\n"
        for voice in stats['voices_used']:
            output += f"- {voice}\n"

    return output


def clear_all_history() -> str:
    """Clear all generation history."""
    success = history_manager.clear_history()
    if success:
        return "✓ History cleared"
    else:
        return "✗ Failed to clear history"


# =============================================================================
# SCRIPTS HANDLERS (Tab 6)
# =============================================================================

def get_script_choices() -> List[str]:
    """Get list of available script .md files in the project root."""
    from pathlib import Path

    # Get project root (parent of utils)
    project_root = Path(__file__).parent.parent

    # Find all script*.md files in project root
    md_files = list(project_root.glob("script*.md"))

    if not md_files:
        return ["No scripts available"]

    # Return just the filename, sorted
    return sorted([md.name for md in md_files])


def get_all_scripts() -> List[Path]:
    """Get all script files as Path objects."""
    from pathlib import Path

    project_root = Path(__file__).parent.parent
    md_files = list(project_root.glob("script*.md"))
    return sorted(md_files)


def refresh_script_dropdown():
    """Refresh the list of available scripts."""
    scripts = get_script_choices()
    return gr.Dropdown(choices=scripts, value=scripts[0] if scripts else None)


def load_all_scripts() -> Tuple[str, str, str]:
    """
    Load all 3 scripts for display.

    Returns:
        Tuple of (script_base, script_medio, script_completo)
    """
    from pathlib import Path
    project_root = Path(__file__).parent.parent

    # Define the 3 expected scripts
    scripts = {
        'base': project_root / 'script_base_clonazione_vocale.md',
        'medio': project_root / 'script_medio_clonazione_vocale.md',
        'completo': project_root / 'script_clonazione_vocale.md'
    }

    results = []

    for key, script_path in scripts.items():
        try:
            if script_path.exists():
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                results.append(content)
            else:
                results.append(f"Script {key} not found: {script_path.name}")
        except Exception as e:
            results.append(f"Error loading script {key}: {str(e)}")

    return tuple(results)


def load_script_content(script_name: str) -> str:
    """
    Load the content of selected script.

    Returns:
        String with script content
    """
    if not script_name or script_name == "No scripts available":
        return "Seleziona uno script dalla dropdown"

    try:
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        script_path = project_root / script_name

        if not script_path.exists():
            return f"Script non trovato: {script_name}"

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return content

    except Exception as e:
        return f"Errore nel caricamento dello script: {str(e)}"
