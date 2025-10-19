"""
Chatterbox TTS Web Interface - Gradio Application

A comprehensive web interface for managing voices, texts, and generating TTS audio.
Features:
- Voice management (add, edit, delete voices)
- Text management (upload, edit texts)
- TTS generation with advanced parameters
- Batch processing
- Generation history
"""

import gradio as gr
from pathlib import Path
from typing import Optional, List, Tuple
import torch
import json

from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from utils.audio_utils import concatenate_audio_files
from utils.text_utils import read_text_from_file
from utils.voice_manager import (
    get_available_voices,
    get_voice_details,
    create_voice,
    add_audio_to_voice,
    remove_audio_from_voice,
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
    create_parameter_presets,
    get_preset_values,
    create_voice_choices,
    create_text_choices,
    estimate_generation_time
)
from utils.history_manager import HistoryManager
import config

# Constants
MAX_SINGLE_PASS_CHARS = 500
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize history manager
HISTORY_FILE = config.OUTPUT_DIR / "generation_history.json"
history_manager = HistoryManager(HISTORY_FILE)


# =============================================================================
# MODEL MANAGEMENT
# =============================================================================

def load_tts_model():
    """Load the TTS model (called once on app start)."""
    print("Loading Chatterbox TTS model...")
    model = ChatterboxMultilingualTTS.from_pretrained(device=DEVICE)
    print(f"Model loaded successfully on {DEVICE}")
    return model


# =============================================================================
# TAB 1: TTS GENERATION
# =============================================================================

def refresh_voice_dropdown():
    """Refresh the list of available voices."""
    voices = create_voice_choices(config.VOICES_DIR)
    return gr.Dropdown(choices=voices, value=voices[0] if voices else None)


def refresh_text_dropdown():
    """Refresh the list of available text files."""
    texts = create_text_choices(config.TEXT_DIR)
    return gr.Dropdown(choices=texts, value=texts[0] if texts else None)


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


def apply_preset(preset_name: str):
    """Apply parameter preset."""
    return get_preset_values(preset_name)


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
) -> Tuple[Optional[Tuple], Optional[Tuple], str]:
    """
    Generate TTS audio from selected voice and text.

    Returns:
        Tuple of (wav_audio, mp3_audio, status_message)
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

            # Generate chunks
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

            # Combine chunks
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

        # Return audio for playback (Gradio expects just the file path as string)
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
# TAB 2: VOICE MANAGER
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


def get_voice_audio_files(voice_name: str) -> List[Tuple[str, str]]:
    """Get list of audio files for a voice (for dropdown/checklist)."""
    if not voice_name:
        return []

    details = get_voice_details(config.VOICES_DIR, voice_name)
    if not details:
        return []

    return [(f['name'], f['path']) for f in details['files']]


def create_new_voice(voice_name: str, audio_files: List) -> str:
    """Create a new voice."""
    if not voice_name:
        return "Please enter a voice name"

    if not audio_files:
        return "Please upload at least one audio file"

    # Sanitize voice name
    voice_name = sanitize_filename(voice_name)

    # Validate audio files
    file_paths = []
    for audio_file in audio_files:
        is_valid, msg = validate_audio_file(audio_file.name)
        if not is_valid:
            return f"Invalid file {audio_file.name}: {msg}"
        file_paths.append(audio_file.name)

    # Create voice
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
# TAB 3: TEXT MANAGER
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

    # Sanitize filename
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

    # Validate
    is_valid, msg = validate_text_file(text_file.name)
    if not is_valid:
        return f"✗ {msg}"

    # Copy to text directory
    import shutil
    src = Path(text_file.name)
    dst = config.TEXT_DIR / sanitize_filename(src.name)

    try:
        shutil.copy2(src, dst)
        # Read to get character count
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
# TAB 4: BATCH PROCESSING
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
            # Read text
            with open(text_file.name, 'r', encoding='utf-8') as f:
                text = f.read()

            # Prepare voice reference
            voice_folder = config.VOICES_DIR / voice_name
            combined_audio_path = config.OUTPUT_DIR / f"{voice_name}_{config.COMBINED_AUDIO_NAME}"
            combined_audio_path = concatenate_audio_files(
                audio_folder=voice_folder,
                output_path=str(combined_audio_path),
                target_sr=config.SAMPLE_RATE
            )

            # Generate filename
            text_basename = Path(text_file.name).stem
            is_long_text = len(text) > MAX_SINGLE_PASS_CHARS
            filenames = generate_output_filenames(
                voice_name=voice_name,
                text_basename=text_basename,
                is_chunked=is_long_text
            )

            # Generate audio
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

            # Convert to MP3
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
# TAB 5: HISTORY
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
# GRADIO INTERFACE
# =============================================================================

def create_interface():
    """Create the Gradio interface."""

    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .tab-nav button {
        font-size: 16px;
        font-weight: 600;
    }
    """

    with gr.Blocks(title="Chatterbox TTS Studio", css=custom_css, theme=gr.themes.Soft()) as app:

        # Shared state for model
        model_state = gr.State(None)

        # Header
        gr.Markdown(
            """
            # 🎙️ Chatterbox TTS Studio
            ### Professional Text-to-Speech Generation & Management
            """
        )

        # Load model on startup
        app.load(fn=load_tts_model, inputs=[], outputs=model_state)

        with gr.Tabs():

            # ===== TAB 1: GENERATION =====
            with gr.Tab("🎬 Generate"):
                gr.Markdown("## Text-to-Speech Generation")

                with gr.Row():
                    with gr.Column(scale=1):
                        voice_dropdown = gr.Dropdown(
                            label="Select Voice",
                            choices=create_voice_choices(config.VOICES_DIR),
                            value=None,
                            interactive=True
                        )
                        voice_info_display = gr.Markdown("Select a voice to see details")
                        refresh_voices_btn = gr.Button("🔄 Refresh Voices", size="sm")

                    with gr.Column(scale=1):
                        text_dropdown = gr.Dropdown(
                            label="Select Text",
                            choices=create_text_choices(config.TEXT_DIR),
                            value=None,
                            interactive=True
                        )
                        text_info_display = gr.Markdown("Select a text to see details")
                        refresh_texts_btn = gr.Button("🔄 Refresh Texts", size="sm")

                # Parameters
                with gr.Accordion("⚙️ Generation Parameters", open=False):
                    preset_dropdown = gr.Dropdown(
                        label="Parameter Preset",
                        choices=list(create_parameter_presets().keys()),
                        value="Neutral (Default)",
                        interactive=True
                    )

                    with gr.Row():
                        with gr.Column():
                            temperature_slider = gr.Slider(
                                0.05, 2.0, step=0.05, value=config.TEMPERATURE,
                                label="Temperature"
                            )
                            cfg_weight_slider = gr.Slider(
                                0.0, 1.0, step=0.05, value=config.CFG_WEIGHT,
                                label="CFG Weight / Pace"
                            )
                            exaggeration_slider = gr.Slider(
                                0.25, 2.0, step=0.05, value=config.EXAGGERATION,
                                label="Exaggeration"
                            )
                        with gr.Column():
                            repetition_penalty_slider = gr.Slider(
                                1.0, 3.0, step=0.1, value=config.REPETITION_PENALTY,
                                label="Repetition Penalty"
                            )
                            min_p_slider = gr.Slider(
                                0.0, 1.0, step=0.01, value=config.MIN_P,
                                label="Min P"
                            )
                            top_p_slider = gr.Slider(
                                0.0, 1.0, step=0.01, value=config.TOP_P,
                                label="Top P"
                            )

                # Generate button
                generate_btn = gr.Button("🎯 Generate Speech", variant="primary", size="lg")
                status_text = gr.Textbox(label="Status", interactive=False)

                # Output
                with gr.Row():
                    wav_output = gr.Audio(label="Generated Audio (WAV)", type="filepath")
                    mp3_output = gr.Audio(label="Generated Audio (MP3)", type="filepath")

                # Event handlers for Tab 1
                voice_dropdown.change(
                    fn=update_voice_info,
                    inputs=[voice_dropdown],
                    outputs=[voice_info_display]
                )

                text_dropdown.change(
                    fn=update_text_info,
                    inputs=[text_dropdown],
                    outputs=[text_info_display]
                )

                refresh_voices_btn.click(
                    fn=refresh_voice_dropdown,
                    inputs=[],
                    outputs=[voice_dropdown]
                )

                refresh_texts_btn.click(
                    fn=refresh_text_dropdown,
                    inputs=[],
                    outputs=[text_dropdown]
                )

                preset_dropdown.change(
                    fn=apply_preset,
                    inputs=[preset_dropdown],
                    outputs=[
                        temperature_slider,
                        cfg_weight_slider,
                        exaggeration_slider,
                        repetition_penalty_slider,
                        min_p_slider,
                        top_p_slider
                    ]
                )

                generate_btn.click(
                    fn=generate_tts,
                    inputs=[
                        model_state,
                        voice_dropdown,
                        text_dropdown,
                        temperature_slider,
                        cfg_weight_slider,
                        exaggeration_slider,
                        repetition_penalty_slider,
                        min_p_slider,
                        top_p_slider
                    ],
                    outputs=[wav_output, mp3_output, status_text]
                )

            # ===== TAB 2: VOICE MANAGER =====
            with gr.Tab("🎤 Voices"):
                gr.Markdown("## Voice Management")

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### Existing Voices")
                        voices_list_display = gr.Markdown(list_voices_details())
                        refresh_voice_list_btn = gr.Button("🔄 Refresh List", size="sm")

                    with gr.Column(scale=1):
                        gr.Markdown("### Create New Voice")
                        new_voice_name = gr.Textbox(label="Voice Name", placeholder="e.g., myVoice")
                        new_voice_files = gr.File(
                            label="Upload Audio Files",
                            file_count="multiple",
                            file_types=["audio"]
                        )
                        create_voice_btn = gr.Button("➕ Create Voice", variant="primary")
                        create_voice_status = gr.Textbox(label="Status", interactive=False)

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Add Files to Existing Voice")
                        add_voice_dropdown = gr.Dropdown(
                            label="Select Voice",
                            choices=create_voice_choices(config.VOICES_DIR),
                            value=None
                        )
                        add_audio_files = gr.File(
                            label="Upload Audio Files to Add",
                            file_count="multiple",
                            file_types=["audio"]
                        )
                        add_audio_btn = gr.Button("➕ Add Files")
                        add_audio_status = gr.Textbox(label="Status", interactive=False)

                    with gr.Column():
                        gr.Markdown("### Delete Voice")
                        delete_voice_dropdown = gr.Dropdown(
                            label="Select Voice to Delete",
                            choices=create_voice_choices(config.VOICES_DIR),
                            value=None
                        )
                        delete_voice_btn = gr.Button("🗑️ Delete Voice", variant="stop")
                        delete_voice_status = gr.Textbox(label="Status", interactive=False)

                # Event handlers for Tab 2
                refresh_voice_list_btn.click(
                    fn=list_voices_details,
                    inputs=[],
                    outputs=[voices_list_display]
                )

                create_voice_btn.click(
                    fn=create_new_voice,
                    inputs=[new_voice_name, new_voice_files],
                    outputs=[create_voice_status]
                ).then(
                    fn=list_voices_details,
                    inputs=[],
                    outputs=[voices_list_display]
                )

                add_audio_btn.click(
                    fn=add_audio_files_to_voice,
                    inputs=[add_voice_dropdown, add_audio_files],
                    outputs=[add_audio_status]
                ).then(
                    fn=list_voices_details,
                    inputs=[],
                    outputs=[voices_list_display]
                )

                delete_voice_btn.click(
                    fn=delete_selected_voice,
                    inputs=[delete_voice_dropdown],
                    outputs=[delete_voice_status]
                ).then(
                    fn=list_voices_details,
                    inputs=[],
                    outputs=[voices_list_display]
                )

            # ===== TAB 3: TEXT MANAGER =====
            with gr.Tab("📝 Texts"):
                gr.Markdown("## Text Management")

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Existing Texts")
                        texts_list_display = gr.Markdown(list_texts_details())
                        refresh_text_list_btn = gr.Button("🔄 Refresh List", size="sm")

                    with gr.Column():
                        gr.Markdown("### Add New Text")

                        with gr.Tabs():
                            with gr.Tab("Type Text"):
                                input_text_name = gr.Textbox(label="Text Name", placeholder="e.g., myText")
                                input_text_content = gr.Textbox(
                                    label="Text Content",
                                    placeholder="Enter your text here...",
                                    lines=10,
                                    max_lines=20
                                )
                                char_counter = gr.Markdown("Characters: 0")
                                save_input_btn = gr.Button("💾 Save Text", variant="primary")
                                save_input_status = gr.Textbox(label="Status", interactive=False)

                            with gr.Tab("Upload File"):
                                upload_text_file = gr.File(
                                    label="Upload Text File (.txt)",
                                    file_types=[".txt"]
                                )
                                upload_text_btn = gr.Button("📤 Upload", variant="primary")
                                upload_text_status = gr.Textbox(label="Status", interactive=False)

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Delete Text")
                        delete_text_dropdown = gr.Dropdown(
                            label="Select Text to Delete",
                            choices=create_text_choices(config.TEXT_DIR),
                            value=None
                        )
                        delete_text_btn = gr.Button("🗑️ Delete Text", variant="stop")
                        delete_text_status = gr.Textbox(label="Status", interactive=False)

                # Event handlers for Tab 3
                input_text_content.change(
                    fn=lambda text: f"Characters: {len(text)}",
                    inputs=[input_text_content],
                    outputs=[char_counter]
                )

                refresh_text_list_btn.click(
                    fn=list_texts_details,
                    inputs=[],
                    outputs=[texts_list_display]
                )

                save_input_btn.click(
                    fn=save_text_from_input,
                    inputs=[input_text_name, input_text_content],
                    outputs=[save_input_status]
                ).then(
                    fn=list_texts_details,
                    inputs=[],
                    outputs=[texts_list_display]
                )

                upload_text_btn.click(
                    fn=save_uploaded_text,
                    inputs=[upload_text_file],
                    outputs=[upload_text_status]
                ).then(
                    fn=list_texts_details,
                    inputs=[],
                    outputs=[texts_list_display]
                )

                delete_text_btn.click(
                    fn=delete_text_file,
                    inputs=[delete_text_dropdown],
                    outputs=[delete_text_status]
                ).then(
                    fn=list_texts_details,
                    inputs=[],
                    outputs=[texts_list_display]
                )

            # ===== TAB 4: BATCH PROCESSING =====
            with gr.Tab("⚡ Batch"):
                gr.Markdown("## Batch Processing")
                gr.Markdown("Generate TTS for multiple text files at once")

                with gr.Row():
                    with gr.Column():
                        batch_voice_dropdown = gr.Dropdown(
                            label="Select Voice",
                            choices=create_voice_choices(config.VOICES_DIR),
                            value=None
                        )

                        batch_text_files = gr.File(
                            label="Upload Text Files (.txt)",
                            file_count="multiple",
                            file_types=[".txt"]
                        )

                    with gr.Column():
                        gr.Markdown("### Parameters")
                        batch_temperature = gr.Slider(0.05, 2.0, step=0.05, value=config.TEMPERATURE, label="Temperature")
                        batch_cfg_weight = gr.Slider(0.0, 1.0, step=0.05, value=config.CFG_WEIGHT, label="CFG Weight")
                        batch_exaggeration = gr.Slider(0.25, 2.0, step=0.05, value=config.EXAGGERATION, label="Exaggeration")
                        batch_repetition_penalty = gr.Slider(1.0, 3.0, step=0.1, value=config.REPETITION_PENALTY, label="Repetition Penalty")
                        batch_min_p = gr.Slider(0.0, 1.0, step=0.01, value=config.MIN_P, label="Min P")
                        batch_top_p = gr.Slider(0.0, 1.0, step=0.01, value=config.TOP_P, label="Top P")

                batch_generate_btn = gr.Button("⚡ Start Batch Generation", variant="primary", size="lg")
                batch_results = gr.Markdown("Results will appear here")

                # Event handler for Tab 4
                batch_generate_btn.click(
                    fn=batch_generate,
                    inputs=[
                        model_state,
                        batch_voice_dropdown,
                        batch_text_files,
                        batch_temperature,
                        batch_cfg_weight,
                        batch_exaggeration,
                        batch_repetition_penalty,
                        batch_min_p,
                        batch_top_p
                    ],
                    outputs=[batch_results]
                )

            # ===== TAB 5: HISTORY =====
            with gr.Tab("📊 History"):
                gr.Markdown("## Generation History & Statistics")

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Recent Generations")
                        history_display = gr.Markdown(display_history())
                        refresh_history_btn = gr.Button("🔄 Refresh History", size="sm")

                    with gr.Column():
                        gr.Markdown("### Statistics")
                        stats_display = gr.Markdown(display_statistics())
                        refresh_stats_btn = gr.Button("🔄 Refresh Stats", size="sm")

                clear_history_btn = gr.Button("🗑️ Clear All History", variant="stop")
                clear_history_status = gr.Textbox(label="Status", interactive=False)

                # Event handlers for Tab 5
                refresh_history_btn.click(
                    fn=display_history,
                    inputs=[],
                    outputs=[history_display]
                )

                refresh_stats_btn.click(
                    fn=display_statistics,
                    inputs=[],
                    outputs=[stats_display]
                )

                clear_history_btn.click(
                    fn=clear_all_history,
                    inputs=[],
                    outputs=[clear_history_status]
                ).then(
                    fn=display_history,
                    inputs=[],
                    outputs=[history_display]
                ).then(
                    fn=display_statistics,
                    inputs=[],
                    outputs=[stats_display]
                )

        # Footer
        gr.Markdown(
            """
            ---
            **Chatterbox TTS Studio** | Built with Gradio | Device: {}
            """.format(DEVICE)
        )

    return app


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Ensure directories exist
    config.VOICES_DIR.mkdir(parents=True, exist_ok=True)
    config.TEXT_DIR.mkdir(parents=True, exist_ok=True)
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.OUTPUT_WAV_DIR.mkdir(parents=True, exist_ok=True)
    config.OUTPUT_MP3_DIR.mkdir(parents=True, exist_ok=True)

    print("Starting Chatterbox TTS Studio...")
    print(f"Device: {DEVICE}")

    app = create_interface()
    app.queue(max_size=50, default_concurrency_limit=1).launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
