# Chatterbox TTS Studio

Studio professionale di sintesi vocale utilizzando [Chatterbox](https://github.com/resemble-ai/chatterbox) con **interfaccia web Gradio** e gestione completa di voci e testi.

## Caratteristiche

- 🌐 **Interfaccia Web Gradio** - Interfaccia grafica moderna e professionale
- ✨ **Sintesi vocale multilingue** - Supporto per 23 lingue
- 🎙️ **Gestione voci** - Crea, modifica ed elimina voci direttamente dall'interfaccia
- 📝 **Gestione testi** - Upload, modifica ed elimina file di testo
- ⚡ **Batch processing** - Genera audio per più testi contemporaneamente
- 📊 **Cronologia e statistiche** - Traccia tutte le generazioni con statistiche dettagliate
- 📜 **Scripts per registrazione** - Guide complete per clonazione vocale
- 📁 **Riferimenti audio multipli** - Concatena automaticamente più file audio per voce
- 🎵 **Export multiplo** - Output in formato WAV e MP3
- ⚙️ **Configurazione centralizzata** - Tutte le impostazioni in un unico file
- 🎛️ **Preset audio** - Configurazioni predefinite (Espressivo, Neutro, Conservativo)

## Struttura del Progetto

```
chatterbox_demo/
├── main-web.py                          # 🌐 Interfaccia Web Gradio (NUOVO!)
├── start_web.bat                        # 🚀 Avvio rapido interfaccia web
├── main.py                              # Script da riga di comando
├── config.py                            # Configurazioni
├── utils/
│   ├── web_handlers.py                  # Handler logica web
│   ├── web_ui.py                        # Costruzione UI Gradio
│   ├── gradio_helpers.py                # Helper per Gradio
│   ├── audio_generator.py               # Generazione audio
│   ├── audio_utils.py                   # Utility audio
│   ├── text_utils.py                    # Utility testo
│   ├── text_splitter.py                 # Divisione testi lunghi
│   ├── voice_manager.py                 # Gestione voci
│   ├── output_manager.py                # Gestione output
│   ├── history_manager.py               # Cronologia generazioni
│   └── setup_utils.py                   # Setup e configurazione
├── input/
│   ├── voice/                           # Cartelle delle voci
│   │   ├── voce1/                       # Voce esempio 1
│   │   │   ├── sample1.wav
│   │   │   └── sample2.wav
│   │   └── voce2/                       # Voce esempio 2
│   │       ├── sample1.ogg
│   │       └── sample2.ogg
│   └── textToGenerate/                  # File di testo
│       ├── text1.txt
│       └── text2.txt
├── output/                              # File generati
│   ├── wav/                             # Audio WAV
│   ├── mp3/                             # Audio MP3
│   └── history/                         # Cronologia generazioni
├── script_clonazione_vocale.md          # Script registrazione (100 frasi)
├── script_medio_clonazione_vocale.md    # Script medio (50 frasi)
└── script_base_clonazione_vocale.md     # Script base (25 frasi)
```

## Quick Start - 5 Minuti

Vuoi iniziare subito? Segui questi passi:

### 1. Installazione Veloce

```bash
# Clona o scarica il progetto
cd chatterbox_demo

# Crea ambiente virtuale
python -m venv venv

# Attiva ambiente
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Installa dipendenze
pip install -r requirements.txt
pip install -e ./chatterbox
```

### 2. Prepara una Voce di Test

```bash
# Crea cartella voce
mkdir input/voice/test

# Copia 3-5 file audio (WAV, MP3, OGG) nella cartella
# Oppure registra clip audio di 5-10 secondi della tua voce
```

### 3. Avvia l'Interfaccia Web

```bash
# Windows
start_web.bat

# Linux/Mac
python main-web.py
```

Apri il browser su: **http://localhost:7860**

### 4. Genera il Primo Audio!

1. Tab **🎬 Generate**
2. Seleziona voce "test"
3. Scrivi un testo o selezionane uno esistente
4. Click **Generate**
5. Ascolta il risultato!

---

## Installazione Completa

### Requisiti

- **Python 3.8 - 3.11** (⚠️ Python 3.13 non è ancora supportato)
- PyTorch con supporto CUDA (per GPU) o CPU
- 4GB RAM minimo (8GB+ consigliati)
- 3GB spazio disco per modelli
- ffmpeg (opzionale, per export MP3)

### Setup Dettagliato

1. **Clona o scarica il progetto**
   ```bash
   git clone <repository-url>
   cd chatterbox_demo
   ```

2. **Crea un ambiente virtuale**
   ```bash
   # Python 3.11 consigliato
   python -m venv venv

   # Attiva ambiente
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Installa PyTorch con CUDA** (per GPU NVIDIA)
   ```bash
   # Per CUDA 12.4
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

   # Oppure solo CPU
   pip install torch torchvision torchaudio
   ```

4. **Installa le altre dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

5. **Installa Chatterbox**
   ```bash
   pip install -e ./chatterbox
   ```

6. **Installa ffmpeg (opzionale, per export MP3)**
   ```bash
   # Windows
   winget install ffmpeg

   # Mac
   brew install ffmpeg

   # Linux
   sudo apt install ffmpeg
   ```

7. **Verifica installazione**
   ```bash
   python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
   ```

## Utilizzo

### 🌐 INTERFACCIA WEB (Consigliato)

L'interfaccia web Gradio è il modo **più semplice e completo** per usare Chatterbox TTS Studio!

#### Avvio Rapido

**Windows:**
```bash
# Doppio click su:
start_web.bat
```

**Linux/Mac:**
```bash
python main-web.py
```

Apri il browser su: **http://localhost:7860**

#### Funzionalità Interfaccia Web

L'interfaccia web include 6 tab principali:

##### 🎬 Tab 1: Generate (Genera Audio)
- Seleziona voce e testo dai dropdown
- Configura parametri di generazione (temperatura, esagerazione, ecc.)
- Usa preset predefiniti: Espressivo, Neutro, Conservativo
- Genera audio WAV e MP3 con un click
- Ascolta e scarica direttamente dall'interfaccia

##### 🎤 Tab 2: Voices (Gestione Voci)
- **Visualizza** tutte le voci disponibili con dettagli
- **Crea** nuove voci caricando file audio
- **Aggiungi** file audio a voci esistenti
- **Elimina** voci non più necessarie
- Vedi numero di file audio per ogni voce

##### 📝 Tab 3: Texts (Gestione Testi)
- **Visualizza** tutti i file di testo disponibili
- **Scrivi** nuovi testi direttamente nell'editor
- **Upload** file .txt dal computer
- **Elimina** testi non più necessari
- Contatore caratteri in tempo reale

##### ⚡ Tab 4: Batch (Generazione Massiva)
- Genera audio per **più testi contemporaneamente**
- Seleziona una voce e più file di testo
- Configura parametri una volta sola
- Genera tutto con un singolo click
- Perfetto per automatizzare la produzione

##### 📊 Tab 5: History (Cronologia)
- Vedi tutte le **generazioni precedenti**
- Statistiche: totale generazioni, durata, dimensione file
- Voci e testi più usati
- Cancella cronologia quando necessario

##### 📜 Tab 6: Scripts (Guide Registrazione)
- Accedi agli **script per clonazione vocale**
- 3 livelli: Base (25 frasi), Medio (50 frasi), Completo (100 frasi)
- Script con frasi foneticamente bilanciate
- Checklist tecnica per registrazione professionale
- Leggi e copia direttamente dall'interfaccia

---

### 💻 Riga di Comando (Avanzato)

Se preferisci usare gli script da terminale:

#### Quick Start

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

## Clonazione Vocale

Per ottenere i migliori risultati nella clonazione vocale, segui gli script di registrazione professionali!

### 📜 Script di Registrazione Disponibili

Il progetto include 3 script per registrare campioni vocali di alta qualità:

1. **script_base_clonazione_vocale.md** - 25 frasi (5-7 minuti)
   - Ideale per test rapidi
   - Copre i fonemi principali

2. **script_medio_clonazione_vocale.md** - 50 frasi (10-12 minuti)
   - Bilanciamento fonemi migliorato
   - Buona qualità generale

3. **script_clonazione_vocale.md** - 100 frasi (15-20 minuti) ⭐ **CONSIGLIATO**
   - Copertura completa di tutti i fonemi italiani
   - Include: domande, esclamazioni, numeri, emozioni
   - Checklist tecnica dettagliata
   - Risultati professionali

### 🎙️ Come Usare gli Script

**Con Interfaccia Web** (Più Facile):
1. Avvia l'interfaccia: `start_web.bat`
2. Vai al tab **📜 Scripts**
3. Seleziona lo script desiderato dal dropdown
4. Leggi e registra le frasi seguendo le istruzioni
5. Salva i file nella cartella della voce

**Da File**:
1. Apri uno degli script `.md` con un editor
2. Segui le istruzioni di registrazione
3. Salva ogni frase come `frase_001.wav`, `frase_002.wav`, ecc.
4. Copia tutti i file in `input/voice/tuaVoce/`

### ✅ Checklist Rapida Registrazione

- ✅ **Ambiente silenzioso** (nessun rumore di fondo)
- ✅ **Microfono di qualità** (condensatore USB consigliato)
- ✅ **Distanza costante**: 15-20cm dalla bocca
- ✅ **Formato**: WAV, 44.1kHz, 16-bit, mono
- ✅ **Durata**: Almeno 3-5 secondi per file
- ✅ **Quantità**: Minimo 20 file, consigliati 50-100
- ✅ **Idratazione**: Bevi acqua, voce pulita
- ✅ **Lettura naturale**: Conversazionale, non robotica

---

## Configurazione Avanzata

### Parametri di Generazione

**Con Interfaccia Web**:
- Vai al tab **🎬 Generate**
- Usa i **Preset**: Espressivo, Neutro, Conservativo
- Oppure regola manualmente i parametri

**Da Riga di Comando** - Modifica `config.py`:

```python
# Selezione voce e testo
SELECTED_VOICE = "miaVoce"
SELECTED_TEXT_FILE = "mio_testo.txt"

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
MIN_P = 0.05              # Probabilità minima token
TOP_P = 1.0               # Top-p sampling
```

### Spiegazione Parametri

| Parametro | Intervallo | Descrizione | Quando Usarlo |
|-----------|-----------|-------------|---------------|
| **TEMPERATURE** | 0.0-1.0 | Variabilità della sintesi | Basso (0.5-0.7) per voce stabile, Alto (0.8-1.0) per variabilità |
| **CFG_WEIGHT** | 0.0-1.0 | Fedeltà all'audio di riferimento | Alto (0.5-0.8) per somiglianza, Basso (0.2-0.4) per creatività |
| **EXAGGERATION** | 0.0-1.0 | Espressività emotiva | Basso (0.2-0.4) per voce neutra, Alto (0.7-0.9) per narrazione espressiva |
| **REPETITION_PENALTY** | 1.0-3.0 | Evita ripetizioni | Standard: 2.0, Aumenta se noti parole ripetute |
| **MIN_P** | 0.0-1.0 | Filtra token improbabili | Standard: 0.05 |
| **TOP_P** | 0.0-1.0 | Nucleus sampling | Standard: 1.0, Riduci (0.7-0.9) per più coerenza |

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

## Esempi d'Uso

### 🌐 Esempio 1: Workflow Completo con Interfaccia Web

**Scenario**: Creare un audiolibro con la tua voce

1. **Registra campioni vocali**
   - Vai al tab **📜 Scripts**
   - Seleziona "Script Completo Clonazione Vocale"
   - Registra le 100 frasi seguendo le indicazioni
   - Salva come `frase_001.wav`, `frase_002.wav`, etc.

2. **Crea la voce**
   - Vai al tab **🎤 Voices**
   - Inserisci nome: "La_Mia_Voce"
   - Carica tutti i file audio registrati
   - Click su "Create Voice"

3. **Prepara i testi**
   - Vai al tab **📝 Texts**
   - Scrivi o carica i capitoli del libro
   - Salva come: `capitolo_1.txt`, `capitolo_2.txt`, etc.

4. **Genera l'audiolibro (Batch)**
   - Vai al tab **⚡ Batch**
   - Seleziona voce: "La_Mia_Voce"
   - Seleziona tutti i capitoli
   - Usa preset "Espressivo"
   - Click "Generate All"

5. **Verifica risultati**
   - Vai al tab **📊 History**
   - Vedi tutte le generazioni
   - Scarica i file WAV/MP3
   - Controlla statistiche

---

### 💻 Esempio 2: Voce Italiana Espressiva (Riga di Comando)

```python
# config.py
SELECTED_VOICE = "narrator"
SELECTED_TEXT_FILE = "racconto.txt"
LANGUAGE_ID = "it"
EXAGGERATION = 0.9       # Voce molto espressiva
TEMPERATURE = 0.8        # Buona variabilità
CFG_WEIGHT = 0.6         # Fedele all'audio di riferimento
```

```bash
# Testo in input/textToGenerate/racconto.txt
Wow! Non ci posso credere, è fantastico!
Il mio cuore batteva forte mentre aprivo la porta...
```

```bash
python main.py
```

**Output**: `output/wav/narrator_racconto.wav`

---

### 💻 Esempio 3: Voce Neutra per Assistente Virtuale

```python
# config.py
SELECTED_VOICE = "assistant"
SELECTED_TEXT_FILE = "messaggi_sistema.txt"
LANGUAGE_ID = "it"
EXAGGERATION = 0.2       # Voce neutra
TEMPERATURE = 0.6        # Stabile e ripetibile
CFG_WEIGHT = 0.7         # Molto fedele
```

```bash
# Testo
Benvenuto nel sistema. Seleziona un'opzione dal menu.
```

---

### 🌐 Esempio 4: Generazione Batch Multilingue

**Interfaccia Web - Tab Batch**:
- Voce: "polyglot"
- Testi:
  - `welcome_it.txt` (italiano)
  - `welcome_en.txt` (inglese)
  - `welcome_fr.txt` (francese)

**Nota**: Cambia `LANGUAGE_ID` in `config.py` prima di ogni generazione, oppure usa più sessioni batch separate.

## Script Utili

### main-web.py (CONSIGLIATO)
**Interfaccia web completa con Gradio**

```bash
# Windows
start_web.bat

# Linux/Mac
python main-web.py
```

Funzionalità:
- Gestione completa voci e testi
- Generazione batch
- Cronologia e statistiche
- Scripts per clonazione vocale
- Interfaccia user-friendly

---

### main.py
**Script da riga di comando** - Genera sintesi vocale per testi brevi/medi e lunghi

```bash
python main.py
```

Caratteristiche:
- Auto-detect lunghezza testo (<500 caratteri: single-pass, >500 caratteri: chunked)
- Concatena automaticamente più file audio di riferimento
- Output WAV e MP3
- Nomi file intelligenti: `{voce}_{testo}.wav`

Configurazione in `config.py`:
```python
SELECTED_VOICE = "miaVoce"
SELECTED_TEXT_FILE = "mio_testo.txt"
```

## Risoluzione Problemi

### 🌐 Problemi Interfaccia Web

#### L'interfaccia web non si avvia

**Soluzione**:
1. Verifica che tutte le dipendenze siano installate:
```bash
pip install -r requirements.txt
pip install -e ./chatterbox
```

2. Verifica che la porta 7860 sia libera:
```bash
# Windows
netstat -ano | findstr :7860

# Linux/Mac
lsof -i :7860
```

3. Prova a cambiare porta in `main-web.py` (linea 376-380)

#### Errore durante il caricamento del modello

**Soluzione**: Il modello viene caricato all'avvio. Attendi 30-60 secondi. Se persiste:
- Verifica connessione internet (download modello da Hugging Face)
- Controlla spazio su disco (modello ~2GB)
- Verifica memoria GPU/RAM disponibile

---

### 💻 Problemi Script da Riga di Comando

### Errore: "Nessuna voce trovata"

**Soluzione**: Assicurati di aver creato almeno una cartella in `input/voice/` con file audio.

```bash
mkdir input/voice/miaVoce
# Copia file audio in input/voice/miaVoce/
```

Oppure usa l'interfaccia web (Tab **Voices**) per creare voci facilmente!

### Errore: "Voce non trovata"

**Soluzione**: Verifica che il nome in `SELECTED_VOICE` corrisponda esattamente al nome della cartella.

**Con interfaccia web**: Vai al tab **Generate** e seleziona la voce dal dropdown.

**Da riga di comando**: Aggiorna `config.py` con il nome corretto della cartella.

### Errore: "Nessun file audio trovato"

**Soluzione**: La cartella della voce è vuota. Aggiungi file audio (`.wav`, `.mp3`, `.ogg`, `.flac`, `.m4a`, `.opus`).

**Con interfaccia web**: Usa il tab **Voices** > **Add Audio Files** per aggiungere file.

### Errore: "ffmpeg non trovato"

**Soluzione**: L'export MP3 è opzionale. Il file WAV viene comunque generato. Per abilitare MP3:
```bash
# Windows
winget install ffmpeg

# Linux
sudo apt install ffmpeg

# Mac
brew install ffmpeg
```

### La voce generata non somiglia all'audio di riferimento

**Soluzioni**:
- **Usa più file audio di riferimento** (almeno 3-5 file da 5-10 secondi)
- Assicurati che gli audio siano **puliti e senza rumore di fondo**
- Aumenta il parametro **EXAGGERATION** (0.7-0.9 per voci più espressive)
- Usa audio della **stessa persona/voce**
- Registra seguendo gli **script di clonazione vocale** (tab Scripts nell'interfaccia web)

**Nell'interfaccia web**:
- Vai al tab **Generate**
- Usa il preset **"Espressivo"** per voci più caratterizzate
- Regola il parametro **Exaggeration** manualmente

### Out of Memory (GPU)

**Soluzione**: Forza l'uso della CPU modificando `config.py`:
```python
DEVICE = "cpu"
```

**Nota**: La generazione sarà più lenta ma funzionerà anche senza GPU.

### Testo troppo lungo / Errore CUDA

**Causa**: Il testo supera i 500 caratteri e la GPU va in errore.

**Soluzione**: Lo script `main.py` ora gestisce **automaticamente** i testi lunghi dividendoli in chunk!

Se usi l'**interfaccia web**, la gestione è automatica in tutti i tab.

## Tips & Best Practices

### 🎙️ Per Audio di Alta Qualità

1. **Qualità dei Campioni Vocali**
   - Usa microfono condensatore (es. Blue Yeti, Audio-Technica AT2020)
   - Ambiente silenzioso con poco riverbero
   - Nessun rumore di fondo (ventole, traffico, ecc.)
   - Distanza costante dal microfono (15-20cm)

2. **Quantità Campioni**
   - Minimo: 20 file (test rapidi)
   - Raccomandato: 50-100 file (qualità professionale)
   - Usa gli script di clonazione vocale forniti

3. **Formato Audio**
   - Formato: WAV (non MP3 compresso)
   - Sample rate: 44.1kHz o 48kHz
   - Bit depth: 16-bit o 24-bit
   - Canali: Mono (non stereo)

4. **Contenuto Vocale**
   - Variabilità: domande, esclamazioni, affermazioni
   - Copertura fonetica completa (usa gli script!)
   - Emozioni diverse (neutro, felice, serio)
   - Evita: tosse, schiocchi di labbra, respiri pesanti

### ⚙️ Ottimizzazione Parametri

**Per Narrazione/Audiolibri:**
```python
EXAGGERATION = 0.7-0.9
TEMPERATURE = 0.7-0.8
CFG_WEIGHT = 0.5-0.6
```

**Per Assistente Virtuale/Sistema:**
```python
EXAGGERATION = 0.2-0.3
TEMPERATURE = 0.6
CFG_WEIGHT = 0.7
```

**Per Podcast/Interviste:**
```python
EXAGGERATION = 0.5-0.6
TEMPERATURE = 0.7
CFG_WEIGHT = 0.6
```

### 🚀 Performance

- **GPU NVIDIA**: 5-10x più veloce della CPU
- **Testi lunghi**: Usa chunking automatico (già implementato)
- **Batch processing**: Usa tab Batch nell'interfaccia web
- **Memoria**: Se OOM su GPU, usa `DEVICE = "cpu"` in config.py

### 📁 Organizzazione File

```
input/voice/
├── personaggio_1/        # Voce protagonista
├── personaggio_2/        # Voce antagonista
├── narratore/           # Voce neutrale
└── backup_registrazioni/  # Backup originali

input/textToGenerate/
├── progetto_A/
│   ├── capitolo_1.txt
│   └── capitolo_2.txt
└── progetto_B/
    └── script.txt
```

---

## FAQ - Domande Frequenti

**Q: Quanti file audio servono per clonare una voce?**
A: Minimo 20, ma 50-100 file danno risultati molto migliori. Usa gli script di registrazione forniti.

**Q: Quanto tempo serve per generare 1 minuto di audio?**
A: Con GPU: 10-30 secondi. Con CPU: 1-3 minuti. Dipende dalla lunghezza del testo.

**Q: Posso usare file MP3 come campioni vocali?**
A: Sì, ma WAV non compresso è fortemente raccomandato per migliore qualità.

**Q: Supporta lingue italiane/dialetti?**
A: Il modello è addestrato su italiano standard. Dialetti funzionano se presenti nei campioni audio.

**Q: Posso commercializzare audio generati?**
A: Verifica la licenza di Chatterbox. Assicurati di avere i diritti sulla voce clonata.

**Q: Come miglioro la somiglianza alla voce originale?**
A: 1) Più campioni audio (50+), 2) Audio di alta qualità, 3) Aumenta CFG_WEIGHT, 4) Usa script di registrazione.

**Q: L'interfaccia web funziona su tablet/smartphone?**
A: Sì, ma le prestazioni dipendono dall'hardware. Raccomandato PC/laptop con GPU.

---

## Changelog Recenti

### v2.0.0 - Interfaccia Web Gradio
- ✨ **NUOVO**: Interfaccia web completa con 6 tab
- ✨ **NUOVO**: Gestione voci e testi dall'interfaccia
- ✨ **NUOVO**: Batch processing per più testi
- ✨ **NUOVO**: Cronologia e statistiche generazioni
- ✨ **NUOVO**: Scripts di clonazione vocale integrati
- ✨ **NUOVO**: Preset audio (Espressivo, Neutro, Conservativo)
- 🔧 Migliorato: Gestione automatica testi lunghi
- 🔧 Migliorato: Nomenclatura file output intelligente
- 📚 Documentazione completamente riscritta

---

## Licenza

Questo progetto è un demo di [Chatterbox by Resemble AI](https://github.com/resemble-ai/chatterbox).

Verifica i termini di licenza di Chatterbox per uso commerciale.

## Crediti

- [Chatterbox](https://github.com/resemble-ai/chatterbox) - Resemble AI
- Modello: Chatterbox Multilingual TTS
- Interfaccia: Gradio
- Sviluppato con Python, PyTorch, librosa

---

## Supporto

Per problemi, domande o suggerimenti:

1. Consulta la sezione **Risoluzione Problemi** sopra
2. Controlla le **FAQ**
3. Verifica la [documentazione Chatterbox](https://github.com/resemble-ai/chatterbox)

---

**Buona sintesi vocale! 🎙️✨**
