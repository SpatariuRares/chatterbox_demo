"""
UI builder functions for Gradio web interface.

This module contains all the UI construction logic,
separated from business logic handlers for better maintainability.
"""

import gradio as gr
from utils.gradio_helpers import (
    create_parameter_presets,
    get_preset_values,
    create_voice_choices,
    create_text_choices
)
import config


def create_generation_tab(model_state):
    """
    Create the TTS Generation tab.

    Returns:
        Dictionary with UI components for event binding
    """
    components = {}

    gr.Markdown("## Text-to-Speech Generation")

    with gr.Row():
        with gr.Column(scale=1):
            components['voice_dropdown'] = gr.Dropdown(
                label="Select Voice",
                choices=create_voice_choices(config.VOICES_DIR),
                value=None,
                interactive=True
            )
            components['voice_info'] = gr.Markdown("Select a voice to see details")
            components['refresh_voices_btn'] = gr.Button("🔄 Refresh Voices", size="sm")

        with gr.Column(scale=1):
            components['text_dropdown'] = gr.Dropdown(
                label="Select Text",
                choices=create_text_choices(config.TEXT_DIR),
                value=None,
                interactive=True
            )
            components['text_info'] = gr.Markdown("Select a text to see details")
            components['refresh_texts_btn'] = gr.Button("🔄 Refresh Texts", size="sm")

    # Parameters
    with gr.Accordion("⚙️ Generation Parameters", open=False):
        components['preset_dropdown'] = gr.Dropdown(
            label="Parameter Preset",
            choices=list(create_parameter_presets().keys()),
            value="Neutral (Default)",
            interactive=True,
            info="15 preset ottimizzati per diversi casi d'uso: News, Podcast, Audiobook, Documentary, Advertisement, Tutorial, Sports, Character, Meditation, ecc."
        )

        with gr.Row():
            with gr.Column():
                components['temperature'] = gr.Slider(
                    0.05, 2.0, step=0.05, value=config.TEMPERATURE,
                    label="Temperature",
                    info="Controlla la variabilità della voce. Basso (0.5-0.7) = voce stabile, Alto (0.9-1.2) = più espressiva e variabile"
                )
                components['cfg_weight'] = gr.Slider(
                    0.0, 1.0, step=0.05, value=config.CFG_WEIGHT,
                    label="CFG Weight / Pace",
                    info="Fedeltà al prompt audio. Basso (0.3-0.5) = più creativo, Alto (0.6-0.8) = più fedele alla voce di riferimento"
                )
                components['exaggeration'] = gr.Slider(
                    0.25, 2.0, step=0.05, value=config.EXAGGERATION,
                    label="Exaggeration",
                    info="Espressività emotiva. Basso (0.3-0.5) = monotono/neutro, Medio (0.5-0.7) = naturale, Alto (0.8-1.2) = molto espressivo"
                )
            with gr.Column():
                components['repetition_penalty'] = gr.Slider(
                    1.0, 3.0, step=0.1, value=config.REPETITION_PENALTY,
                    label="Repetition Penalty",
                    info="Previene ripetizioni. Basso (1.0-1.3) = permette ripetizioni, Alto (1.5-2.5) = evita fortemente ripetizioni e loop"
                )
                components['min_p'] = gr.Slider(
                    0.0, 1.0, step=0.01, value=config.MIN_P,
                    label="Min P",
                    info="Filtra token improbabili. Basso (0.01-0.05) = più varietà, Alto (0.1-0.2) = più conservativo e prevedibile"
                )
                components['top_p'] = gr.Slider(
                    0.0, 1.0, step=0.01, value=config.TOP_P,
                    label="Top P",
                    info="Nucleus sampling. Basso (0.5-0.8) = più deterministico, Alto (0.9-1.0) = più varietà. 1.0 = disattivato"
                )

    # Generate button
    components['generate_btn'] = gr.Button("🎯 Generate Speech", variant="primary", size="lg")
    components['status_text'] = gr.Textbox(label="Status", interactive=False)

    # Output
    with gr.Row():
        components['wav_output'] = gr.Audio(label="Generated Audio (WAV)", type="filepath")
        components['mp3_output'] = gr.Audio(label="Generated Audio (MP3)", type="filepath")

    return components


def create_voice_tab():
    """
    Create the Voice Management tab.

    Returns:
        Dictionary with UI components for event binding
    """
    components = {}

    gr.Markdown("## Voice Management")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Existing Voices")
            components['voices_list'] = gr.Markdown()
            components['refresh_list_btn'] = gr.Button("🔄 Refresh List", size="sm")

        with gr.Column(scale=1):
            gr.Markdown("### Create New Voice")
            components['new_voice_name'] = gr.Textbox(label="Voice Name", placeholder="e.g., myVoice")
            components['new_voice_files'] = gr.File(
                label="Upload Audio Files",
                file_count="multiple",
                file_types=["audio"]
            )
            components['create_voice_btn'] = gr.Button("➕ Create Voice", variant="primary")
            components['create_voice_status'] = gr.Textbox(label="Status", interactive=False)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Add Files to Existing Voice")
            components['add_voice_dropdown'] = gr.Dropdown(
                label="Select Voice",
                choices=create_voice_choices(config.VOICES_DIR),
                value=None
            )
            components['add_audio_files'] = gr.File(
                label="Upload Audio Files to Add",
                file_count="multiple",
                file_types=["audio"]
            )
            components['add_audio_btn'] = gr.Button("➕ Add Files")
            components['add_audio_status'] = gr.Textbox(label="Status", interactive=False)

        with gr.Column():
            gr.Markdown("### Delete Voice")
            components['delete_voice_dropdown'] = gr.Dropdown(
                label="Select Voice to Delete",
                choices=create_voice_choices(config.VOICES_DIR),
                value=None
            )
            components['delete_voice_btn'] = gr.Button("🗑️ Delete Voice", variant="stop")
            components['delete_voice_status'] = gr.Textbox(label="Status", interactive=False)

    return components


def create_text_tab():
    """
    Create the Text Management tab.

    Returns:
        Dictionary with UI components for event binding
    """
    components = {}

    gr.Markdown("## Text Management")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Existing Texts")
            components['texts_list'] = gr.Markdown()
            components['refresh_text_list_btn'] = gr.Button("🔄 Refresh List", size="sm")

        with gr.Column():
            gr.Markdown("### Add New Text")

            with gr.Tabs():
                with gr.Tab("Type Text"):
                    components['input_text_name'] = gr.Textbox(label="Text Name", placeholder="e.g., myText")
                    components['input_text_content'] = gr.Textbox(
                        label="Text Content",
                        placeholder="Enter your text here...",
                        lines=10,
                        max_lines=20
                    )
                    components['char_counter'] = gr.Markdown("Characters: 0")
                    components['save_input_btn'] = gr.Button("💾 Save Text", variant="primary")
                    components['save_input_status'] = gr.Textbox(label="Status", interactive=False)

                with gr.Tab("Upload File"):
                    components['upload_text_file'] = gr.File(
                        label="Upload Text File (.txt)",
                        file_types=[".txt"]
                    )
                    components['upload_text_btn'] = gr.Button("📤 Upload", variant="primary")
                    components['upload_text_status'] = gr.Textbox(label="Status", interactive=False)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Delete Text")
            components['delete_text_dropdown'] = gr.Dropdown(
                label="Select Text to Delete",
                choices=create_text_choices(config.TEXT_DIR),
                value=None
            )
            components['delete_text_btn'] = gr.Button("🗑️ Delete Text", variant="stop")
            components['delete_text_status'] = gr.Textbox(label="Status", interactive=False)

    return components


def create_batch_tab(model_state):
    """
    Create the Batch Processing tab.

    Returns:
        Dictionary with UI components for event binding
    """
    components = {}

    gr.Markdown("## Batch Processing")
    gr.Markdown("Generate TTS for multiple text files at once")

    with gr.Row():
        with gr.Column():
            components['batch_voice'] = gr.Dropdown(
                label="Select Voice",
                choices=create_voice_choices(config.VOICES_DIR),
                value=None
            )

            components['batch_text_files'] = gr.File(
                label="Upload Text Files (.txt)",
                file_count="multiple",
                file_types=[".txt"]
            )

        with gr.Column():
            gr.Markdown("### Parameters")
            components['batch_temperature'] = gr.Slider(
                0.05, 2.0, step=0.05, value=config.TEMPERATURE,
                label="Temperature",
                info="Variabilità voce: Basso = stabile, Alto = variabile"
            )
            components['batch_cfg_weight'] = gr.Slider(
                0.0, 1.0, step=0.05, value=config.CFG_WEIGHT,
                label="CFG Weight",
                info="Fedeltà alla voce: Basso = creativo, Alto = fedele"
            )
            components['batch_exaggeration'] = gr.Slider(
                0.25, 2.0, step=0.05, value=config.EXAGGERATION,
                label="Exaggeration",
                info="Espressività: Basso = monotono, Alto = espressivo"
            )
            components['batch_repetition_penalty'] = gr.Slider(
                1.0, 3.0, step=0.1, value=config.REPETITION_PENALTY,
                label="Repetition Penalty",
                info="Previene ripetizioni: Alto = meno ripetizioni"
            )
            components['batch_min_p'] = gr.Slider(
                0.0, 1.0, step=0.01, value=config.MIN_P,
                label="Min P",
                info="Filtra token: Basso = varietà, Alto = conservativo"
            )
            components['batch_top_p'] = gr.Slider(
                0.0, 1.0, step=0.01, value=config.TOP_P,
                label="Top P",
                info="Sampling: Basso = deterministico, Alto = varietà"
            )

    components['batch_generate_btn'] = gr.Button("⚡ Start Batch Generation", variant="primary", size="lg")
    components['batch_results'] = gr.Markdown("Results will appear here")

    return components


def create_history_tab():
    """
    Create the History tab.

    Returns:
        Dictionary with UI components for event binding
    """
    components = {}

    gr.Markdown("## Generation History & Statistics")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Recent Generations")
            components['history_display'] = gr.Markdown()
            components['refresh_history_btn'] = gr.Button("🔄 Refresh History", size="sm")

        with gr.Column():
            gr.Markdown("### Statistics")
            components['stats_display'] = gr.Markdown()
            components['refresh_stats_btn'] = gr.Button("🔄 Refresh Stats", size="sm")

    components['clear_history_btn'] = gr.Button("🗑️ Clear All History", variant="stop")
    components['clear_history_status'] = gr.Textbox(label="Status", interactive=False)

    return components


def create_scripts_tab():
    """
    Create the Scripts tab.

    Returns:
        Dictionary with UI components for event binding
    """
    components = {}

    gr.Markdown("## Scripts per Clonazione Vocale")
    gr.Markdown("Seleziona uno script dalla dropdown per visualizzare il contenuto")

    with gr.Row():
        components['script_dropdown'] = gr.Dropdown(
            label="Seleziona Script",
            choices=[],
            value=None,
            interactive=True,
            info="Scegli tra: Base (25 frasi), Medio (50 frasi), Completo (100 frasi)"
        )
        components['refresh_scripts_btn'] = gr.Button("🔄 Aggiorna Lista", size="sm")

    # Single script display
    components['script_display'] = gr.Textbox(
        label="Contenuto Script",
        lines=25,
        max_lines=40,
        interactive=False,
        show_copy_button=True,
        placeholder="Seleziona uno script dalla dropdown per visualizzare il contenuto..."
    )

    return components
