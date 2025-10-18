"""
Audio utilities for voice processing and conversion.
"""
import subprocess
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path


def concatenate_audio_files(audio_folder, output_path="combined_voice.wav", target_sr=24000):
    """
    Concatena tutti i file audio in una cartella in un singolo file.

    Args:
        audio_folder: Path alla cartella contenente i file audio
        output_path: Path del file audio combinato
        target_sr: Sample rate target (default 24000 Hz)

    Returns:
        Path del file audio combinato
    """
    audio_folder = Path(audio_folder)

    # Estensioni audio supportate
    audio_extensions = ['.wav', '.mp3', '.ogg', '.flac', '.m4a', '.opus']

    # Trova tutti i file audio nella cartella
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(audio_folder.glob(f"*{ext}"))

    if not audio_files:
        raise ValueError(f"Nessun file audio trovato in {audio_folder}")

    # Ordina i file per nome
    audio_files = sorted(audio_files)

    print(f"Trovati {len(audio_files)} file audio:")
    for f in audio_files:
        print(f"  - {f.name}")

    # Carica e concatena tutti gli audio
    combined_audio = []
    for audio_file in audio_files:
        try:
            audio, sr = librosa.load(str(audio_file), sr=target_sr)
            combined_audio.append(audio)
            print(f"Caricato: {audio_file.name} ({len(audio)/sr:.2f}s)")
        except Exception as e:
            print(f"Errore nel caricare {audio_file.name}: {e}")

    if not combined_audio:
        raise ValueError("Nessun audio caricato con successo")

    # Concatena tutti gli audio
    final_audio = np.concatenate(combined_audio)

    # Salva il file combinato
    sf.write(output_path, final_audio, target_sr)
    print(f"\nAudio combinato salvato in: {output_path}")
    print(f"Durata totale: {len(final_audio)/target_sr:.2f} secondi")

    return output_path


def convert_to_mp3(input_file, output_file=None, bitrate="192k"):
    """
    Converte un file audio in MP3 usando ffmpeg.

    Args:
        input_file: Path del file audio di input
        output_file: Path del file MP3 di output (opzionale, usa .mp3 se non specificato)
        bitrate: Bitrate per la codifica MP3 (default 192k)

    Returns:
        Path del file MP3 creato

    Raises:
        FileNotFoundError: Se ffmpeg non è installato
        subprocess.CalledProcessError: Se la conversione fallisce
    """
    input_path = Path(input_file)

    if output_file is None:
        output_file = input_path.with_suffix('.mp3')

    output_path = Path(output_file)

    # Comando ffmpeg per convertire in MP3
    cmd = [
        'ffmpeg',
        '-i', str(input_path),
        '-vn',  # No video
        '-acodec', 'libmp3lame',
        '-b:a', bitrate,
        '-y',  # Sovrascrivi se esiste
        str(output_path)
    ]

    print(f"Conversione in MP3: {input_path.name} -> {output_path.name}")
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )
    print(f"MP3 creato: {output_path}")
    return str(output_path)
