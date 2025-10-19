"""
Chatterbox TTS Studio - Web Interface (Simplified)

A clean, modular implementation of the Gradio web interface.
Business logic is in utils/web_handlers.py
UI construction is in utils/web_ui.py
"""

import gradio as gr
import torch

from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from utils.web_handlers import (
    # Generation handlers
    refresh_voice_dropdown,
    refresh_text_dropdown,
    refresh_all_voice_dropdowns,
    refresh_all_text_dropdowns,
    update_voice_info,
    update_text_info,
    generate_tts,
    # Voice handlers
    list_voices_details,
    create_new_voice,
    add_audio_files_to_voice,
    delete_selected_voice,
    # Text handlers
    list_texts_details,
    save_text_from_input,
    save_uploaded_text,
    delete_text_file,
    # Batch handlers
    batch_generate,
    # History handlers
    display_history,
    display_statistics,
    clear_all_history,
    # Scripts handlers
    get_script_choices,
    refresh_script_dropdown,
    load_script_content
)
from utils.web_ui import (
    create_generation_tab,
    create_voice_tab,
    create_text_tab,
    create_batch_tab,
    create_history_tab,
    create_scripts_tab
)
from utils.gradio_helpers import get_preset_values
import config

# Device detection
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def load_tts_model():
    """Load the TTS model (called once on app start)."""
    print("Loading Chatterbox TTS model...")
    model = ChatterboxMultilingualTTS.from_pretrained(device=DEVICE)
    print(f"Model loaded successfully on {DEVICE}")
    return model


def create_interface():
    """Create the Gradio interface."""

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
                gen = create_generation_tab(model_state)

                # Event handlers
                gen['voice_dropdown'].change(
                    fn=update_voice_info,
                    inputs=[gen['voice_dropdown']],
                    outputs=[gen['voice_info']]
                )

                gen['text_dropdown'].change(
                    fn=update_text_info,
                    inputs=[gen['text_dropdown']],
                    outputs=[gen['text_info']]
                )

                gen['refresh_voices_btn'].click(
                    fn=refresh_voice_dropdown,
                    inputs=[],
                    outputs=[gen['voice_dropdown']]
                )

                gen['refresh_texts_btn'].click(
                    fn=refresh_text_dropdown,
                    inputs=[],
                    outputs=[gen['text_dropdown']]
                )

                gen['preset_dropdown'].change(
                    fn=get_preset_values,
                    inputs=[gen['preset_dropdown']],
                    outputs=[
                        gen['temperature'],
                        gen['cfg_weight'],
                        gen['exaggeration'],
                        gen['repetition_penalty'],
                        gen['min_p'],
                        gen['top_p']
                    ]
                )

                gen['generate_btn'].click(
                    fn=generate_tts,
                    inputs=[
                        model_state,
                        gen['voice_dropdown'],
                        gen['text_dropdown'],
                        gen['temperature'],
                        gen['cfg_weight'],
                        gen['exaggeration'],
                        gen['repetition_penalty'],
                        gen['min_p'],
                        gen['top_p']
                    ],
                    outputs=[gen['wav_output'], gen['mp3_output'], gen['status_text']]
                )

            # ===== TAB 2: VOICES =====
            with gr.Tab("🎤 Voices"):
                voice = create_voice_tab()

                # Set initial values
                app.load(fn=list_voices_details, inputs=[], outputs=[voice['voices_list']])

                # Event handlers
                voice['refresh_list_btn'].click(
                    fn=list_voices_details,
                    inputs=[],
                    outputs=[voice['voices_list']]
                )

                voice['create_voice_btn'].click(
                    fn=create_new_voice,
                    inputs=[voice['new_voice_name'], voice['new_voice_files']],
                    outputs=[voice['create_voice_status']]
                ).then(
                    fn=list_voices_details,
                    inputs=[],
                    outputs=[voice['voices_list']]
                ).then(
                    fn=refresh_all_voice_dropdowns,
                    inputs=[],
                    outputs=[gen['voice_dropdown'], voice['add_voice_dropdown'], voice['delete_voice_dropdown']]
                )

                voice['add_audio_btn'].click(
                    fn=add_audio_files_to_voice,
                    inputs=[voice['add_voice_dropdown'], voice['add_audio_files']],
                    outputs=[voice['add_audio_status']]
                ).then(
                    fn=list_voices_details,
                    inputs=[],
                    outputs=[voice['voices_list']]
                ).then(
                    fn=refresh_all_voice_dropdowns,
                    inputs=[],
                    outputs=[gen['voice_dropdown'], voice['add_voice_dropdown'], voice['delete_voice_dropdown']]
                )

                voice['delete_voice_btn'].click(
                    fn=delete_selected_voice,
                    inputs=[voice['delete_voice_dropdown']],
                    outputs=[voice['delete_voice_status']]
                ).then(
                    fn=list_voices_details,
                    inputs=[],
                    outputs=[voice['voices_list']]
                ).then(
                    fn=refresh_all_voice_dropdowns,
                    inputs=[],
                    outputs=[gen['voice_dropdown'], voice['add_voice_dropdown'], voice['delete_voice_dropdown']]
                )

            # ===== TAB 3: TEXTS =====
            with gr.Tab("📝 Texts"):
                text = create_text_tab()

                # Set initial values
                app.load(fn=list_texts_details, inputs=[], outputs=[text['texts_list']])

                # Event handlers
                text['input_text_content'].change(
                    fn=lambda txt: f"Characters: {len(txt)}",
                    inputs=[text['input_text_content']],
                    outputs=[text['char_counter']]
                )

                text['refresh_text_list_btn'].click(
                    fn=list_texts_details,
                    inputs=[],
                    outputs=[text['texts_list']]
                )

                text['save_input_btn'].click(
                    fn=save_text_from_input,
                    inputs=[text['input_text_name'], text['input_text_content']],
                    outputs=[text['save_input_status']]
                ).then(
                    fn=list_texts_details,
                    inputs=[],
                    outputs=[text['texts_list']]
                ).then(
                    fn=refresh_all_text_dropdowns,
                    inputs=[],
                    outputs=[gen['text_dropdown'], text['delete_text_dropdown']]
                )

                text['upload_text_btn'].click(
                    fn=save_uploaded_text,
                    inputs=[text['upload_text_file']],
                    outputs=[text['upload_text_status']]
                ).then(
                    fn=list_texts_details,
                    inputs=[],
                    outputs=[text['texts_list']]
                ).then(
                    fn=refresh_all_text_dropdowns,
                    inputs=[],
                    outputs=[gen['text_dropdown'], text['delete_text_dropdown']]
                )

                text['delete_text_btn'].click(
                    fn=delete_text_file,
                    inputs=[text['delete_text_dropdown']],
                    outputs=[text['delete_text_status']]
                ).then(
                    fn=list_texts_details,
                    inputs=[],
                    outputs=[text['texts_list']]
                ).then(
                    fn=refresh_all_text_dropdowns,
                    inputs=[],
                    outputs=[gen['text_dropdown'], text['delete_text_dropdown']]
                )

            # ===== TAB 4: BATCH =====
            with gr.Tab("⚡ Batch"):
                batch = create_batch_tab(model_state)

                # Event handler
                batch['batch_generate_btn'].click(
                    fn=batch_generate,
                    inputs=[
                        model_state,
                        batch['batch_voice'],
                        batch['batch_text_files'],
                        batch['batch_temperature'],
                        batch['batch_cfg_weight'],
                        batch['batch_exaggeration'],
                        batch['batch_repetition_penalty'],
                        batch['batch_min_p'],
                        batch['batch_top_p']
                    ],
                    outputs=[batch['batch_results']]
                )

            # ===== TAB 5: HISTORY =====
            with gr.Tab("📊 History"):
                hist = create_history_tab()

                # Set initial values
                app.load(fn=display_history, inputs=[], outputs=[hist['history_display']])
                app.load(fn=display_statistics, inputs=[], outputs=[hist['stats_display']])

                # Event handlers
                hist['refresh_history_btn'].click(
                    fn=display_history,
                    inputs=[],
                    outputs=[hist['history_display']]
                )

                hist['refresh_stats_btn'].click(
                    fn=display_statistics,
                    inputs=[],
                    outputs=[hist['stats_display']]
                )

                hist['clear_history_btn'].click(
                    fn=clear_all_history,
                    inputs=[],
                    outputs=[hist['clear_history_status']]
                ).then(
                    fn=display_history,
                    inputs=[],
                    outputs=[hist['history_display']]
                ).then(
                    fn=display_statistics,
                    inputs=[],
                    outputs=[hist['stats_display']]
                )

            # ===== TAB 6: SCRIPTS =====
            with gr.Tab("📜 Scripts"):
                scripts = create_scripts_tab()

                # Set initial values - populate dropdown only
                app.load(
                    fn=lambda: gr.Dropdown(choices=get_script_choices(), value=None),
                    inputs=[],
                    outputs=[scripts['script_dropdown']]
                )

                # Event handlers
                scripts['script_dropdown'].change(
                    fn=load_script_content,
                    inputs=[scripts['script_dropdown']],
                    outputs=[scripts['script_display']]
                )

                scripts['refresh_scripts_btn'].click(
                    fn=refresh_script_dropdown,
                    inputs=[],
                    outputs=[scripts['script_dropdown']]
                )

        # Footer
        gr.Markdown(
            f"""
            ---
            **Chatterbox TTS Studio** | Built with Gradio | Device: {DEVICE}
            """
        )

    return app


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
