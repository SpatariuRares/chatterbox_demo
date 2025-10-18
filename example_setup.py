"""
Script di esempio per mostrare come configurare e usare il sistema.
Esegui questo file per vedere un esempio completo di configurazione.
"""
from pathlib import Path
import shutil

def setup_example():
    """Crea un esempio di configurazione."""
    print("=" * 60)
    print("ESEMPIO DI SETUP - Chatterbox TTS")
    print("=" * 60)

    base_dir = Path(__file__).parent

    # Controlla struttura cartelle
    print("\n1. Verifica struttura cartelle:")
    folders = [
        base_dir / "input",
        base_dir / "output",
        base_dir / "output" / "wav",
        base_dir / "output" / "mp3",
    ]

    for folder in folders:
        if folder.exists():
            print(f"   ✓ {folder.name}/ esiste")
        else:
            folder.mkdir(parents=True, exist_ok=True)
            print(f"   ✓ {folder.name}/ creata")

    # Controlla file di testo
    print("\n2. Verifica file di testo:")
    text_file = base_dir / "text_to_generate.txt"
    if text_file.exists():
        print(f"   ✓ text_to_generate.txt esiste")
        with open(text_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"   Contenuto: {content[:50]}..." if len(content) > 50 else f"   Contenuto: {content}")
    else:
        print("   ✗ text_to_generate.txt non trovato")
        print("   Creazione file di esempio...")
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("Ciao, questo è un esempio di sintesi vocale con Chatterbox TTS.")
        print("   ✓ File creato!")

    # Controlla file audio nella cartella input
    print("\n3. Verifica file audio di riferimento:")
    input_dir = base_dir / "input"
    audio_extensions = ['.wav', '.mp3', '.ogg', '.flac', '.m4a', '.opus']
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(list(input_dir.glob(f"*{ext}")))

    if audio_files:
        print(f"   ✓ Trovati {len(audio_files)} file audio:")
        for audio_file in audio_files:
            print(f"     - {audio_file.name}")
    else:
        print("   ✗ Nessun file audio trovato nella cartella input/")
        print("\n   AZIONE RICHIESTA:")
        print("   1. Copia i tuoi file audio nella cartella 'input/'")
        print("   2. Formati supportati: .wav, .mp3, .ogg, .flac, .m4a, .opus")
        print("   3. Raccomandato: almeno 3-5 secondi di audio pulito per file")

    # Controlla config
    print("\n4. Configurazione:")
    try:
        import config
        print(f"   ✓ Lingua: {config.LANGUAGE_ID}")
        print(f"   ✓ Temperature: {config.TEMPERATURE}")
        print(f"   ✓ Exaggeration: {config.EXAGGERATION}")
        print(f"   ✓ Sample rate: {config.SAMPLE_RATE} Hz")
    except Exception as e:
        print(f"   ✗ Errore nel caricamento config: {e}")

    # Prossimi passi
    print("\n" + "=" * 60)
    print("PROSSIMI PASSI:")
    print("=" * 60)
    if audio_files:
        print("\n✓ Tutto pronto! Esegui:")
        print("  python main.py")
    else:
        print("\n1. Aggiungi file audio nella cartella 'input/'")
        print("2. (Opzionale) Modifica 'text_to_generate.txt' con il tuo testo")
        print("3. (Opzionale) Personalizza le impostazioni in 'config.py'")
        print("4. Esegui: python main.py")
    print()

if __name__ == "__main__":
    setup_example()
