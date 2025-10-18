# Chatterbox TTS Demo

Demo di sintesi vocale utilizzando [Chatterbox](https://github.com/resemble-ai/chatterbox) con supporto per riferimenti audio multipli e gestione di voci diverse.

## Caratteristiche

- ✨ **Sintesi vocale multilingue** - Supporto per 23 lingue
- 🎙️ **Multiple voci** - Gestisci e cambia facilmente tra diverse voci
- 📝 **Multiple testi** - Gestisci e organizza diversi file di testo
- 📁 **Riferimenti audio multipli** - Concatena automaticamente più file audio per voce
- 🎵 **Export multiplo** - Output in formato WAV e MP3
- ⚙️ **Configurazione centralizzata** - Tutte le impostazioni in un unico file
- 📊 **Nomenclatura intelligente** - File output con nome `{voce}_{testo}.wav`

## Struttura del Progetto

```
chatterbox_demo/
├── main.py                      # Script principale
├── list_voices.py               # Elenca voci disponibili
├── list_texts.py                # Elenca testi disponibili
├── config.py                    # Configurazioni
├── USAGE_GUIDE.md               # Guida rapida all'uso
├── utils/
│   ├── audio_utils.py          # Utility per audio
│   ├── text_utils.py           # Utility per testo
│   └── voice_manager.py        # Gestione voci
├── input/
│   ├── voice/                  # Cartelle delle voci
│   │   ├── joeDoe/             # Voce 1
│   │   │   ├── sample1.ogg
│   │   │   └── sample2.ogg
│   │   └── janeDoe/            # Voce 2
│   │       ├── sample1.wav
│   │       └── sample2.wav
│   └── textToGenerate/         # File di testo
│       ├── text_to_generate.txt
│       └── canto1DC.txt
└── output/                     # File generati
    ├── joeDoe_combined_voice.wav
    ├── wav/
    │   ├── joeDoe_text_to_generate.wav
    │   └── joeDoe_canto1DC.wav
    └── mp3/
        ├── joeDoe_text_to_generate.mp3
        └── joeDoe_canto1DC.mp3
```

## Installazione

### Requisiti

- Python 3.11+
- PyTorch
- CUDA (opzionale, per GPU)

### Setup

1. **Clona o scarica il progetto**

2. **Crea un ambiente virtuale**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # oppure
   source venv/bin/activate  # Linux/Mac
   ```

3. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

4. **Installa ffmpeg (opzionale, per export MP3)**
   ```bash
   # Windows
   winget install ffmpeg

   # Mac
   brew install ffmpeg

   # Linux
   sudo apt install ffmpeg
   ```

## Utilizzo

### Quick Start

1. **Prepara le voci**

   Crea una cartella per ogni voce in `input/voice/`:
   ```
   input/voice/miaVoce/
   ├── sample1.wav
   ├── sample2.wav
   └── sample3.ogg
   ```

   - Formati supportati: `.wav`, `.mp3`, `.ogg`, `.flac`, `.m4a`, `.opus`
   - Raccomandazione: audio puliti, senza rumore di fondo
   - Durata consigliata: almeno 3-5 secondi per file
   - Più file = migliore qualità

2. **Elenca le voci disponibili**
   ```bash
   python list_voices.py
   ```

   Output:
   ```
   🎤 [SELEZIONATA] joeDoe
        Percorso: input/voice/joeDoe
        File audio: 5
        Campioni:
          - sample1.ogg
          - sample2.ogg
          ...

      janeDoe
        Percorso: input/voice/janeDoe
        File audio: 3
   ```

3. **Prepara i file di testo**

   Aggiungi file `.txt` in `input/textToGenerate/`:
   ```bash
   echo "Ciao, questo è un test." > input/textToGenerate/test1.txt
   ```

4. **Elenca i testi disponibili**
   ```bash
   python list_texts.py
   ```

   Output:
   ```
   📄 [SELEZIONATO] text_to_generate.txt
        Caratteri: 58
        Anteprima: Ciao, questo è un test di sintesi vocale...

      canto1DC.txt
        Caratteri: 1234
        Anteprima: Nel mezzo del cammin di nostra vita...
   ```

5. **Seleziona voce e testo**

   Modifica `config.py`:
   ```python
   SELECTED_VOICE = "joeDoe"                # Voce da usare
   SELECTED_TEXT_FILE = "canto1DC.txt"      # Testo da sintetizzare
   ```

6. **Esegui lo script**
   ```bash
   python main.py
   ```

7. **Trova i file generati**

   I file saranno nella cartella `output/`:
   - `output/wav/joeDoe_canto1DC.wav` - Sintesi vocale (WAV)
   - `output/mp3/joeDoe_canto1DC.mp3` - Sintesi vocale (MP3)
   - `output/joeDoe_combined_voice.wav` - Audio di riferimento combinato

   **Formato nome**: `{voce}_{testo}.{estensione}`

## Gestione Multiple Voci

### Aggiungere una Nuova Voce

1. Crea una cartella in `input/voice/`:
   ```bash
   mkdir input/voice/nuovaVoce
   ```

2. Aggiungi file audio nella cartella:
   ```
   input/voice/nuovaVoce/
   ├── recording1.wav
   ├── recording2.mp3
   └── recording3.ogg
   ```

3. Verifica che sia stata rilevata:
   ```bash
   python list_voices.py
   ```

4. Selezionala in `config.py`:
   ```python
   SELECTED_VOICE = "nuovaVoce"
   ```

### Cambiare Voce

Modifica semplicemente `SELECTED_VOICE` in `config.py`:

```python
# In config.py
SELECTED_VOICE = "janeDoe"  # Cambia la voce qui
```

Poi riesegui:
```bash
python main.py
```

## Gestione Multiple Testi

### Aggiungere un Nuovo Testo

1. Crea un file `.txt` in `input/textToGenerate/`:
   ```bash
   echo "Il tuo testo qui" > input/textToGenerate/nuovo_testo.txt
   ```

2. Verifica che sia stato rilevato:
   ```bash
   python list_texts.py
   ```

3. Selezionalo in `config.py`:
   ```python
   SELECTED_TEXT_FILE = "nuovo_testo.txt"
   ```

### Cambiare Testo

Modifica `SELECTED_TEXT_FILE` in `config.py`:

```python
# In config.py
SELECTED_TEXT_FILE = "canto1DC.txt"  # Cambia il testo qui
```

Poi riesegui:
```bash
python main.py
```

## Configurazione Avanzata

Modifica il file `config.py` per personalizzare:

```python
# Selezione voce e testo
SELECTED_VOICE = "joeDoe"
SELECTED_TEXT_FILE = "canto1DC.txt"

# Lingua (codici ISO 639-1)
LANGUAGE_ID = "it"  # Italiano

# Qualità audio
SAMPLE_RATE = 24000
MP3_BITRATE = "192k"

# Parametri di generazione
TEMPERATURE = 0.8          # Variabilità (0.0-1.0)
CFG_WEIGHT = 0.5          # Peso del conditioning
EXAGGERATION = 0.5        # Espressività (0.0-1.0)
REPETITION_PENALTY = 2.0  # Penalità ripetizioni
```

## Lingue Supportate

Il modello supporta 23 lingue:

| Codice | Lingua      | Codice | Lingua     |
|--------|-------------|--------|------------|
| `ar`   | Arabo       | `it`   | Italiano   |
| `da`   | Danese      | `ja`   | Giapponese |
| `de`   | Tedesco     | `ko`   | Coreano    |
| `el`   | Greco       | `ms`   | Malese     |
| `en`   | Inglese     | `nl`   | Olandese   |
| `es`   | Spagnolo    | `no`   | Norvegese  |
| `fi`   | Finlandese  | `pl`   | Polacco    |
| `fr`   | Francese    | `pt`   | Portoghese |
| `he`   | Ebraico     | `sv`   | Svedese    |
| `hi`   | Hindi       | `sw`   | Swahili    |
| `tr`   | Turco       | `zh`   | Cinese     |

## Esempi

### Esempio 1: Voce Italiana Espressiva

```python
# config.py
SELECTED_VOICE = "joeDoe"
LANGUAGE_ID = "it"
EXAGGERATION = 0.9  # Più espressività
```

```
# text_to_generate.txt
Wow! Non ci posso credere, è fantastico!
```

### Esempio 2: Voce Calma e Neutra

```python
# config.py
SELECTED_VOICE = "janeDoe"
LANGUAGE_ID = "it"
EXAGGERATION = 0.2  # Meno espressività
TEMPERATURE = 0.6   # Meno variabilità
```

```
# text_to_generate.txt
Questo è un messaggio informativo di servizio.
```

### Esempio 3: Generare Audio per Multiple Voci

```bash
# Voce 1
# Modifica config.py: SELECTED_VOICE = "joeDoe"
python main.py

# Voce 2
# Modifica config.py: SELECTED_VOICE = "janeDoe"
python main.py
```

I file saranno salvati con nomi diversi:
- `output/wav/joeDoe_generated_speech.wav`
- `output/wav/janeDoe_generated_speech.wav`

## Script Utili

### main.py
Genera sintesi vocale per testi brevi/medi (<500 caratteri)

```bash
python main.py
```

### generate_long_text.py
Genera sintesi vocale per testi lunghi (divide automaticamente in chunk)

```bash
python generate_long_text.py
```

Utile per:
- Testi >500 caratteri
- Libri, articoli lunghi
- Quando `main.py` genera errori CUDA

### list_voices.py
Elenca tutte le voci disponibili con dettagli:

```bash
python list_voices.py
```

### list_texts.py
Elenca tutti i file di testo con anteprima:

```bash
python list_texts.py
```

## Risoluzione Problemi

### Errore: "Nessuna voce trovata"

**Soluzione**: Assicurati di aver creato almeno una cartella in `input/voice/` con file audio.

```bash
mkdir input/voice/miaVoce
# Copia file audio in input/voice/miaVoce/
```

### Errore: "Voce non trovata"

**Soluzione**: Verifica che il nome in `SELECTED_VOICE` corrisponda esattamente al nome della cartella:

```bash
python list_voices.py  # Mostra voci disponibili
```

Poi aggiorna `config.py` con il nome corretto.

### Errore: "Nessun file audio trovato"

**Soluzione**: La cartella della voce è vuota. Aggiungi file audio (`.wav`, `.mp3`, `.ogg`, ecc.).

### Errore: "ffmpeg non trovato"

**Soluzione**: L'export MP3 è opzionale. Il file WAV viene comunque generato. Per abilitare MP3:
```bash
winget install ffmpeg  # Windows
```

### Errore: "CUDA error: device-side assert triggered"

**Causa**: Il testo è troppo lungo (>500 caratteri)

**Soluzione**: Usa `generate_long_text.py` invece di `main.py`:
```bash
python generate_long_text.py
```

Questo script:
- Divide automaticamente il testo in chunk
- Genera file separati per ogni chunk
- Combina tutti i chunk in un unico file finale

### La voce generata non somiglia all'audio di riferimento

**Soluzioni**:
- Usa più file audio di riferimento (almeno 3-5)
- Assicurati che gli audio siano puliti e senza rumore
- Aumenta `EXAGGERATION` in `config.py`
- Usa audio della stessa persona/voce

### Out of Memory (GPU)

**Soluzione**: Forza l'uso della CPU modificando `config.py`:
```python
DEVICE = "cpu"
```

## Licenza

Questo progetto è un demo di [Chatterbox by Resemble AI](https://github.com/resemble-ai/chatterbox).

## Crediti

- [Chatterbox](https://github.com/resemble-ai/chatterbox) - Resemble AI
- Modello: Chatterbox Multilingual TTS
