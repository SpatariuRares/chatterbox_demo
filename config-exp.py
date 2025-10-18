"""
Configuration file for Chatterbox TTS Demo.
"""
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
VOICES_DIR = INPUT_DIR / "voice"  # Cartella contenente le sottocartelle delle voci
TEXT_DIR = INPUT_DIR / "textToGenerate"  # Cartella contenente i file di testo
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_WAV_DIR = OUTPUT_DIR / "wav"
OUTPUT_MP3_DIR = OUTPUT_DIR / "mp3"

# Voice Management
# Seleziona quale voce usare (nome della cartella in input/voice/)
SELECTED_VOICE = "joeDoe"

# Text Management
# Seleziona quale file di testo usare (nome del file in input/textToGenerate/)
# Per testi brevi (<500 caratteri) usa main.py
# Per testi lunghi (>500 caratteri) usa generate_long_text.py
SELECTED_TEXT_FILE = "text_to_generate.txt"  # Cambia questo per usare file diversi
# SELECTED_TEXT_FILE = "canto1DC.txt"  # Testo lungo - usa generate_long_text.py

# Audio settings
COMBINED_AUDIO_NAME = "combined_voice.wav"
OUTPUT_WAV_NAME = "generated_speech.wav"
OUTPUT_MP3_NAME = "generated_speech.mp3"
SAMPLE_RATE = 24000
MP3_BITRATE = "192k"

# Chunk management
# Se True, elimina i file chunk dopo aver creato il file combinato
# Se False, mantiene i chunk individuali per riferimento
CLEANUP_CHUNKS = True

# TTS settings
# Lingua del testo da sintetizzare (codice ISO 639-1)
# Esempi: "it"=Italiano, "en"=Inglese, "fr"=Francese, "es"=Spagnolo
LANGUAGE_ID = "it"

# Variabilità della sintesi (0.0-1.0)
# Basso (0.3-0.6) = più ripetitivo e stabile
# Alto (0.8-1.0) = più variabile e imprevedibile
TEMPERATURE = 0.8

# Peso del conditioning/guida del modello (0.0-1.0)
# Basso (0.0-0.3) = più creativo ma meno fedele al prompt
# Alto (0.5-1.0) = più fedele al prompt audio di riferimento
CFG_WEIGHT = 0.5

# Espressività emotiva della voce (0.0-1.0)
# Basso (0.0-0.3) = voce neutra/monotona (es. notizie, annunci)
# Medio (0.4-0.6) = voce naturale (es. conversazione)
# Alto (0.7-1.0) = voce molto espressiva (es. narrazione, teatro)
EXAGGERATION = 0.8

# Penalità per ripetizioni (1.0-3.0)
# Basso (1.0-1.5) = permette più ripetizioni
# Alto (2.0-3.0) = evita fortemente le ripetizioni
REPETITION_PENALTY = 2.0

# Probabilità minima per token (0.0-1.0)
# Filtra token con probabilità inferiore a questa soglia
# Basso (0.01-0.05) = più varietà
# Alto (0.1-0.2) = più conservativo
MIN_P = 0.05

# Top-p sampling/nucleus sampling (0.0-1.0)
# Considera solo i token con probabilità cumulativa fino a questo valore
# Basso (0.5-0.8) = più deterministico
# Alto (0.9-1.0) = più varietà
TOP_P = 1.0

# Device settings (auto-detect by default, or set manually: "cuda", "cpu", "mps")
DEVICE = None  # None = auto-detect
