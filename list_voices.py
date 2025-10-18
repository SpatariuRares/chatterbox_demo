"""
Script per elencare tutte le voci disponibili nel sistema.
"""
from utils.voice_manager import list_voices_info
import config


def main():
    """Lista tutte le voci disponibili con dettagli."""
    print("=" * 70)
    print("VOCI DISPONIBILI - Chatterbox TTS")
    print("=" * 70)

    voices_info = list_voices_info(config.VOICES_DIR)

    if not voices_info:
        print(f"\n❌ Nessuna voce trovata in: {config.VOICES_DIR}")
        print("\nPer aggiungere una nuova voce:")
        print(f"  1. Crea una cartella in: {config.VOICES_DIR}/")
        print("  2. Aggiungi file audio nella cartella")
        print("  3. Esempio: input/voice/miaVoce/sample1.wav")
        return

    print(f"\nCartella voci: {config.VOICES_DIR}")
    print(f"Totale voci: {len(voices_info)}\n")

    for voice_name, info in sorted(voices_info.items()):
        is_selected = voice_name == config.SELECTED_VOICE
        marker = "🎤 [SELEZIONATA]" if is_selected else "  "

        print(f"{marker} {voice_name}")
        print(f"     Percorso: {info['path']}")
        print(f"     File audio: {info['audio_files_count']}")

        if info['audio_files']:
            print(f"     Campioni:")
            for audio_file in info['audio_files'][:5]:  # Mostra max 5 file
                print(f"       - {audio_file}")
            if len(info['audio_files']) > 5:
                print(f"       ... e altri {len(info['audio_files']) - 5} file")
        print()

    print("=" * 70)
    print("COME CAMBIARE VOCE")
    print("=" * 70)
    print(f"\nModifica il file config.py:")
    print(f"  SELECTED_VOICE = \"nomeVoce\"")
    print(f"\nVoci disponibili:")
    for voice_name in sorted(voices_info.keys()):
        print(f"  - {voice_name}")
    print()


if __name__ == "__main__":
    main()
