"""
Script per elencare tutti i file di testo disponibili nel sistema.
"""
import config


def main():
    """Lista tutti i file di testo disponibili con dettagli."""
    print("=" * 70)
    print("FILE DI TESTO DISPONIBILI - Chatterbox TTS")
    print("=" * 70)

    if not config.TEXT_DIR.exists():
        print(f"\n❌ Cartella testi non trovata: {config.TEXT_DIR}")
        print("\nCrea la cartella e aggiungi file .txt:")
        print(f"  mkdir {config.TEXT_DIR}")
        return

    text_files = sorted(config.TEXT_DIR.glob("*.txt"))

    if not text_files:
        print(f"\n❌ Nessun file di testo trovato in: {config.TEXT_DIR}")
        print("\nAggiungi file .txt nella cartella:")
        print(f"  {config.TEXT_DIR}/mio_testo.txt")
        return

    print(f"\nCartella testi: {config.TEXT_DIR}")
    print(f"Totale file: {len(text_files)}\n")

    for text_file in text_files:
        is_selected = text_file.name == config.SELECTED_TEXT_FILE
        marker = "📄 [SELEZIONATO]" if is_selected else "  "

        # Read file to show preview
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                char_count = len(content)
                preview = content[:80] + "..." if len(content) > 80 else content

            print(f"{marker} {text_file.name}")
            print(f"     Caratteri: {char_count}")
            print(f"     Anteprima: {preview}")
            print()
        except Exception as e:
            print(f"{marker} {text_file.name}")
            print(f"     Errore: {e}")
            print()

    print("=" * 70)
    print("COME CAMBIARE FILE DI TESTO")
    print("=" * 70)
    print(f"\nModifica il file config.py:")
    print(f"  SELECTED_TEXT_FILE = \"nome_file.txt\"")
    print(f"\nFile disponibili:")
    for text_file in text_files:
        print(f"  - {text_file.name}")
    print()


if __name__ == "__main__":
    main()
