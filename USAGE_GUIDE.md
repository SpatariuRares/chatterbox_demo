# Guida Rapida all'Uso - Chatterbox TTS Demo

## 📋 Panoramica

Questo sistema permette di generare sintesi vocale con:
- **Multiple voci** - Gestisci diverse voci (persone)
- **Multiple testi** - Gestisci diversi file di testo

## 🗂️ Struttura File

```
input/
├── voice/              # Voci disponibili
│   ├── marcoMartini/
│   └── valentinaBini/
└── textToGenerate/     # Testi da sintetizzare
    ├── text_to_generate.txt
    └── canto1DC.txt

output/
├── wav/                # File WAV generati
│   ├── marcoMartini_text_to_generate.wav
│   └── marcoMartini_canto1DC.wav
└── mp3/                # File MP3 generati
    └── marcoMartini_text_to_generate.mp3
```

## 🚀 Quick Start

### 1. Vedi Voci Disponibili

```bash
python list_voices.py
```

Output:
```
🎤 [SELEZIONATA] marcoMartini
     Percorso: input/voice/marcoMartini
     File audio: 5

   valentinaBini
     Percorso: input/voice/valentinaBini
     File audio: 0
```

### 2. Vedi Testi Disponibili

```bash
python list_texts.py
```

Output:
```
📄 [SELEZIONATO] text_to_generate.txt
     Caratteri: 58
     Anteprima: Ciao, sono la copia di Marco Martini e voto COMUNISTA.

   canto1DC.txt
     Caratteri: 1234
     Anteprima: Nel mezzo del cammin di nostra vita...
```

### 3. Configura in config.py

```python
# Seleziona voce e testo
SELECTED_VOICE = "marcoMartini"
SELECTED_TEXT_FILE = "canto1DC.txt"

# Parametri (opzionale)
LANGUAGE_ID = "it"
EXAGGERATION = 0.5
```

### 4. Genera Audio

```bash
python main.py
```

### 5. Risultato

File generato:
```
output/wav/marcoMartini_canto1DC.wav
output/mp3/marcoMartini_canto1DC.mp3
```

## 📝 Esempi Pratici

### Esempio 1: Generare Più Testi con la Stessa Voce

```python
# config.py - Prima esecuzione
SELECTED_VOICE = "marcoMartini"
SELECTED_TEXT_FILE = "introduzione.txt"
```
```bash
python main.py  # → marcoMartini_introduzione.wav
```

```python
# config.py - Seconda esecuzione
SELECTED_VOICE = "marcoMartini"
SELECTED_TEXT_FILE = "capitolo1.txt"
```
```bash
python main.py  # → marcoMartini_capitolo1.wav
```

### Esempio 2: Stesso Testo con Voci Diverse

```python
# config.py - Prima esecuzione
SELECTED_VOICE = "marcoMartini"
SELECTED_TEXT_FILE = "annuncio.txt"
```
```bash
python main.py  # → marcoMartini_annuncio.wav
```

```python
# config.py - Seconda esecuzione
SELECTED_VOICE = "valentinaBini"
SELECTED_TEXT_FILE = "annuncio.txt"
```
```bash
python main.py  # → valentinaBini_annuncio.wav
```

### Esempio 3: Aggiungere Nuova Voce

```bash
# 1. Crea cartella
mkdir input/voice/lucaRossi

# 2. Aggiungi file audio
# Copia i tuoi file .wav/.mp3 in input/voice/lucaRossi/

# 3. Verifica
python list_voices.py

# 4. Configura
# config.py: SELECTED_VOICE = "lucaRossi"

# 5. Genera
python main.py
```

### Esempio 4: Aggiungere Nuovo Testo

```bash
# 1. Crea file
echo "Testo da sintetizzare" > input/textToGenerate/nuovo_testo.txt

# 2. Verifica
python list_texts.py

# 3. Configura
# config.py: SELECTED_TEXT_FILE = "nuovo_testo.txt"

# 4. Genera
python main.py
```

## ⚙️ Configurazione Parametri

### Parametri Voce

```python
# Espressività
EXAGGERATION = 0.5  # 0.0 = monotono, 1.0 = molto espressivo

# Variabilità
TEMPERATURE = 0.8   # 0.0 = ripetitivo, 1.0 = variegato

# Qualità
CFG_WEIGHT = 0.5    # Peso conditioning (0.0-1.0)
```

### Esempi di Configurazione

**Voce Neutra (Annunci, Notizie)**
```python
EXAGGERATION = 0.2
TEMPERATURE = 0.6
```

**Voce Espressiva (Narrazione, Audio-libri)**
```python
EXAGGERATION = 0.7
TEMPERATURE = 0.8
```

**Voce Drammatica (Teatro, Performance)**
```python
EXAGGERATION = 0.9
TEMPERATURE = 0.9
```

## 📊 Nomenclatura File Output

I file generati seguono questo schema:

```
{VOCE}_{TESTO}.{FORMATO}
```

Esempi:
- `marcoMartini_introduzione.wav`
- `valentinaBini_capitolo1.mp3`
- `lucaRossi_annuncio.wav`

## 🔧 Script Utili

### list_voices.py
Lista tutte le voci disponibili con statistiche

### list_texts.py
Lista tutti i file di testo con anteprima

### main.py
Genera la sintesi vocale

## ❓ FAQ

**Q: Come cambio voce?**
A: Modifica `SELECTED_VOICE` in `config.py`

**Q: Come cambio testo?**
A: Modifica `SELECTED_TEXT_FILE` in `config.py`

**Q: I file hanno nomi strani, posso rinominarli?**
A: Sì, vengono rinominati automaticamente come `{voce}_{testo}.wav`

**Q: Posso generare batch di file?**
A: Attualmente no, ma puoi eseguire `main.py` più volte cambiando la config

**Q: Dove trovo i file generati?**
A: In `output/wav/` (WAV) e `output/mp3/` (MP3)

## 💡 Tips

1. **Più campioni audio = voce migliore**
   Usa almeno 5 file audio da 3-10 secondi per voce

2. **Audio puliti**
   Rimuovi rumori di fondo per risultati migliori

3. **Testi ben formattati**
   Usa punteggiatura corretta per pause naturali

4. **Sperimenta parametri**
   Prova diverse combinazioni di `EXAGGERATION` e `TEMPERATURE`

5. **Nomenclatura chiara**
   Usa nomi descrittivi per voci e testi
   - ✅ `marcoMartini`, `introduzione.txt`
   - ❌ `voce1`, `test.txt`
