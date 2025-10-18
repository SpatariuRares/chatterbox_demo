# Come Usare Questo Programma
**Guida Semplicissima per Principianti**

## Cosa fa questo programma?

Questo programma trasforma un testo scritto in un audio parlato, usando una voce che tu fornisci come esempio.

---

## PASSO 0: Scaricare il Programma sul Tuo Computer

Prima di tutto, devi copiare questo programma sul tuo computer. Ci sono due modi per farlo:

### Metodo A: Download Diretto (PIÙ FACILE)

1. **Vai alla pagina del progetto** su internet (il link ti sarà stato dato da chi ti ha condiviso questo programma)

2. **Cerca il pulsante verde** che dice "Code" o "<> Code"

3. **Clicca** su quel pulsante

4. **Clicca** su "Download ZIP"

5. **Salva il file ZIP** sul tuo computer (es: nel Desktop)

6. **Trova il file ZIP** che hai scaricato

7. **Fai click destro** sul file ZIP

8. **Scegli** "Estrai tutto..." o "Extract all..."

9. **Clicca** su "Estrai" o "Extract"

10. **Ora hai una cartella** con tutti i file del programma!

### Metodo B: Usando Git (per chi vuole imparare)

**Cos'è Git?** È un programma che scarica codice da internet. Non è difficile, ma serve installarlo prima.

#### 1. Installare Git

1. **Vai su** https://git-scm.com/download/win

2. **Scarica** Git per Windows (si scarica automaticamente)

3. **Fai doppio click** sul file scaricato per installarlo

4. **Clicca sempre "Next"** durante l'installazione (le impostazioni predefinite vanno bene)

5. **Clicca "Finish"** alla fine

#### 2. Scaricare il Progetto con Git

1. **Apri il menu Start** di Windows

2. **Cerca** "Git Bash" e aprilo (vedrà una finestra nera)

3. **Decidi dove salvare il progetto**. Per salvarlo sul Desktop, scrivi:
   ```bash
   cd Desktop
   ```
   Poi premi Invio

4. **Copia il progetto** scrivendo questo comando:
   ```bash
   git clone https://github.com/TUO_LINK_QUI
   ```
   (Sostituisci `TUO_LINK_QUI` con il link che ti è stato dato)

   Poi premi Invio

5. **Aspetta** che finisca di scaricare (vedrai scritte che scorrono)

6. **Chiudi** la finestra Git Bash

7. **Ora sul Desktop** troverai una nuova cartella con il programma!

---

## PASSO 0-BIS: Installare ffmpeg (OPZIONALE)

**Cos'è ffmpeg?** È un programmino che permette di convertire audio in formato MP3. Se non lo installi, il programma funzionerà comunque, ma creerà solo file WAV (che sono più grandi ma funzionano ugualmente bene).

### Come Installare ffmpeg

#### Metodo 1: Installazione Automatica (Windows 10/11)

1. **Apri il menu Start** di Windows

2. **Cerca** "Prompt dei comandi" o "CMD"

3. **Fai click destro** su "Prompt dei comandi"

4. **Scegli** "Esegui come amministratore"

5. **Scrivi** questo comando:
   ```
   winget install ffmpeg
   ```

6. **Premi Invio**

7. **Aspetta** che finisca (ci vorranno 1-2 minuti)

8. **Chiudi** la finestra

9. **Adesso devi dire a Windows dove si trova ffmpeg** (aggiungere alle variabili d'ambiente):

   a. **Apri il menu Start** e cerca "variabili d'ambiente"

   b. **Clicca** su "Modifica le variabili d'ambiente di sistema"

   c. Si apre una finestra. **Clicca** sul pulsante "Variabili d'ambiente..." (in basso)

   d. Nella sezione in BASSO chiamata "Variabili di sistema", **cerca** la voce "Path"

   e. **Clicca** su "Path" per selezionarla (diventerà blu)

   f. **Clicca** sul pulsante "Modifica..."

   g. Si apre un'altra finestra con una lista di percorsi

   h. **Clicca** sul pulsante "Nuovo"

   i. **Scrivi** questo percorso (dove winget installa ffmpeg):
      ```
      C:\Program Files\ffmpeg\bin
      ```
      oppure cerca dove winget l'ha installato (di solito in `C:\Users\TUO_NOME\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_...`)

   j. **Clicca** "OK" su tutte le finestre aperte (3 volte)

   k. **RIAVVIA il computer** (importante! Altrimenti Windows non riconosce ffmpeg)

10. **Verifica che funzioni**:
    - Apri di nuovo il "Prompt dei comandi"
    - Scrivi: `ffmpeg -version`
    - Premi Invio
    - Se vedi informazioni su ffmpeg, funziona! ✅
    - Se vedi "comando non riconosciuto", controlla di aver riavviato il computer

#### Metodo 2: Download Manuale

1. **Vai su** https://www.gyan.dev/ffmpeg/builds/

2. **Cerca** la sezione "release builds"

3. **Clicca** su "ffmpeg-release-essentials.zip"

4. **Salva** il file ZIP

5. **Estrai** il contenuto del ZIP (come hai fatto per il progetto)

6. **Ora la parte un po' più complicata** - devi aggiungere ffmpeg al "PATH":
   - Apri la cartella estratta
   - Entra nella cartella "bin"
   - Copia l'indirizzo completo della cartella (es: `C:\ffmpeg\bin`)
   - Cerca "variabili d'ambiente" nel menu Start
   - Clicca su "Modifica le variabili d'ambiente di sistema"
   - Clicca su "Variabili d'ambiente"
   - Cerca "Path" nella sezione "Variabili di sistema"
   - Clicca "Modifica"
   - Clicca "Nuovo"
   - Incolla l'indirizzo che hai copiato
   - Clicca "OK" su tutte le finestre

**Se ti sembra troppo complicato, salta questa parte!** Il programma funziona anche senza MP3.

---

## Prima di iniziare

### Cosa ti serve:
- Un computer con Windows
- File audio della voce che vuoi clonare (registrazioni vocali)
- Il testo che vuoi far "leggere" alla voce
- Python installato (chiedi a qualcuno se non sai come fare)

### Cosa NON ti serve:
- Conoscenza di programmazione
- Esperienza con comandi tecnici
- Account o software complicati

---

## Passo 1: Preparare le tue registrazioni vocali

1. **Trova o registra** degli audio della voce che vuoi clonare
   - Vanno bene file `.wav`, `.mp3`, `.ogg`
   - Meglio se sono almeno 3-5 file diversi
   - Ogni file dovrebbe durare almeno 5 secondi
   - Importante: gli audio devono essere puliti, senza musica di fondo

2. **Crea una cartella** per la tua voce:
   - Vai nella cartella `input/voice/`
   - Crea una nuova cartella con un nome semplice (es: `marioRossi`)
   - **Importante**: il nome NON deve avere spazi! Usa invece `_` (underscore)
     - ✅ Giusto: `marioRossi`, `voce_marco`, `laura2024`
     - ❌ Sbagliato: `mario rossi`, `voce di marco`

3. **Metti i file audio** dentro questa cartella

**Esempio di come dovrebbe apparire:**
```
input/voice/marioRossi/
├── registrazione1.wav
├── registrazione2.mp3
└── registrazione3.wav
```

---

## Passo 2: Preparare il testo

1. **Apri il Blocco Note** di Windows (cerca "Blocco Note" nel menu Start)

2. **Scrivi o incolla** il testo che vuoi far leggere

3. **Salva il file**:
   - Vai su File → Salva con nome
   - Naviga fino alla cartella `input/textToGenerate/`
   - Dai un nome semplice al file (es: `mio_testo.txt`)
   - **Importante**: assicurati che finisca con `.txt`
   - Clicca Salva

**Esempio:**
```
File salvato come: input/textToGenerate/mio_testo.txt
```

---

## Passo 3: Scegliere voce e testo

1. **Apri il file `config.py`** (puoi usare il Blocco Note)

2. **Cerca queste due righe** (sono all'inizio del file):
   ```python
   SELECTED_VOICE = "joeDoe"
   SELECTED_TEXT_FILE = "text_to_generate.txt"
   ```

3. **Cambia i nomi** con i tuoi:
   ```python
   SELECTED_VOICE = "marioRossi"
   SELECTED_TEXT_FILE = "mio_testo.txt"
   ```
   - Scrivi esattamente i nomi delle cartelle/file che hai creato
   - Lascia le virgolette `"` com'è

4. **Salva il file** e chiudilo

---

## Passo 4: Avviare il programma

### Metodo 1: Doppio Click (più semplice)

1. **Trova il file** `main.py` nella cartella principale
2. **Fai doppio click** su `main.py`
3. Si aprirà una finestra nera con scritte che scorrono
4. **Aspetta** che finisca (può volerci qualche minuto)
5. La finestra si chiuderà da sola quando ha finito

### Metodo 2: Prompt dei Comandi

1. **Apri il Prompt dei Comandi**:
   - Premi i tasti `Windows + R`
   - Scrivi `cmd` e premi Invio

2. **Vai nella cartella del progetto**:
   - Scrivi: `cd C:\Users\spata\Desktop\progetti\AI\chatterbox_demo`
   - Premi Invio

3. **Avvia il programma**:
   - Scrivi: `python main.py`
   - Premi Invio

4. **Aspetta** che finisca (vedrai scritte che scorrono)

---

## Passo 5: Trovare il file audio generato

1. **Apri la cartella** `output`

2. **Troverai due cartelle**:
   - `wav/` - contiene il file audio in formato WAV
   - `mp3/` - contiene il file audio in formato MP3 (se installato ffmpeg)

3. **Il nome del file** sarà composto così:
   - `{tuaVoce}_{tuoTesto}.wav`
   - Esempio: `marioRossi_mio_testo.wav`

4. **Apri il file** e ascoltalo!

---

## Cambiare voce o testo

Vuoi generare un altro audio con una voce o testo diverso?

1. **Apri di nuovo** il file `config.py`
2. **Cambia** i nomi in `SELECTED_VOICE` e/o `SELECTED_TEXT_FILE`
3. **Salva** il file
4. **Avvia di nuovo** il programma (Passo 4)

Il nuovo file audio verrà creato con un nome diverso, quindi non sovrascriverà quello precedente!

---

## Controllare quali voci e testi hai

### Vedere tutte le voci disponibili:

1. Fai doppio click su `list_voices.py`
2. Si aprirà una finestra che mostra tutte le voci trovate
3. La voce con 🎤 è quella attualmente selezionata

### Vedere tutti i testi disponibili:

1. Fai doppio click su `list_texts.py`
2. Si aprirà una finestra che mostra tutti i file di testo trovati
3. Il testo con 📄 è quello attualmente selezionato

---

## Problemi Comuni

### "La finestra si apre e si chiude subito"

**Soluzione**: Probabilmente manca Python. Devi installarlo:
1. Cerca "Python" nel menu Start
2. Se non lo trovi, chiedi a qualcuno di installarlo per te

### "Non trovo il file audio generato"

**Soluzione**: Controlla dentro le cartelle `output/wav/` e `output/mp3/`

### "La voce non somiglia all'originale"

**Soluzioni**:
- Usa più file audio di riferimento (almeno 3-5)
- Assicurati che gli audio siano puliti e senza rumori
- Prova con audio più lunghi (almeno 10 secondi ciascuno)

### "Il programma non parte"

**Soluzione**: Controlla che in `config.py` tu abbia scritto:
- Il nome della cartella voce esattamente come l'hai chiamata
- Il nome del file testo con `.txt` alla fine
- Tutto fra virgolette `"così"`

---

## Ricapitolando

1. Metti i file audio in `input/voice/NOME_VOCE/`
2. Metti il file di testo in `input/textToGenerate/`
3. Apri `config.py` e scrivi i nomi giusti
4. Fai doppio click su `main.py`
5. Trova il file generato in `output/wav/` o `output/mp3/`

---

## Serve Aiuto?

Se qualcosa non funziona:
1. Rileggi questa guida passo-passo
2. Controlla di aver seguito tutti i passaggi
3. Chiedi aiuto a qualcuno che conosce il computer

**Buona sintesi vocale!** 🎙️
