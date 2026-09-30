# This is now a simplified, macOS-only voice assistant

No face login, no phone/ADB automation, no hotword listener, no WhatsApp
contact-messaging automation. What's left:

- **Ask a question, get a spoken answer** — anything you say that isn't an
  "open" or "play ... on youtube" command is sent to the AI (x.ai's Grok)
  and spoken back to you.
- **"open chrome" / "open whatsapp"** — opens the app directly.
- **"open youtube" / "open google"** — opens the website.
- **"play <song/video> on youtube"** — searches and plays it on YouTube.
- A Settings panel (already built into the web UI) lets you add more
  app/website shortcuts without touching code.

## What changed from the previous version

- **`main.py`** — removed the face-authentication step and the device/ADB
  setup call entirely. On startup it now goes straight from the loading
  animation to "ready".
- **`run.py`** — removed the background hotword-listener process (it used
  to launch two processes: the app, and a "jarvis"/"alexa" wake-word
  listener). Now it just runs the app directly. You trigger listening by
  clicking the mic in the UI.
- **`engine/command.py`** — removed the "send message" / "phone call" /
  "video call" routing branch. Only "open", "... on youtube", and
  everything else (→ Q&A) remain.
- **`engine/features.py`** — removed `findContact`, `whatsApp` (contact
  messaging automation), `makeCall`, `sendMessage`, `chatBot` (an unused
  hugchat integration that was dead code even before), and the
  `hotword()` listener. Kept `openCommand`, `PlayYoutube`, `grok` (the
  Q&A function), and the Settings-panel CRUD functions the web UI uses.
- **`engine/auth/`** — deleted entirely (face recognition code, trained
  model, sample images).
- **`device.bat`** — deleted (was for setting up a wireless ADB
  connection to an Android phone; no longer needed).
- **`engine/db.py`** — this was previously *entirely commented-out
  scratch code*, meaning `jarvis.db` shipped with **zero tables** — "open
  chrome" etc. would have failed even before any of today's changes. It
  now actually creates the needed tables on first run and seeds default
  entries so `chrome` and `whatsapp` work immediately:
  - `chrome` / `google chrome` → `/Applications/Google Chrome.app`
  - `whatsapp` → `/Applications/WhatsApp.app`
  - `youtube` (website) → `https://www.youtube.com`
  - `google` (website) → `https://www.google.com`

  If your Chrome or WhatsApp isn't installed at the default path above,
  either move it there, or open the app's Settings panel and update the
  shortcut's path yourself (no code changes needed).
- **`requirements.txt`** — trimmed to only what's actually imported now:
  `beautifulsoup4`, `Eel`, `markdown2`, `openai`, `playsound3`,
  `PyAudio`, `pywhatkit`, `SpeechRecognition`. Dropped `opencv-python`,
  `numpy`, `pyautogui`, `pvporcupine`, `hugchat`, and the Windows-only
  packages from before — none of them are needed anymore.

## Setup on macOS

1. **Delete your old `.venv`** if you have one from before (the
   dependency list changed a lot):
   ```bash
   rm -rf .venv
   ```

2. **Create a fresh virtual environment with Python 3.11** (recommended —
   Python 3.13 can have build issues with some of these packages):
   ```bash
   brew install python@3.11   # if you don't already have it
   python3.11 -m venv .venv
   source .venv/bin/activate
   python --version            # should print 3.11.x
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   If `PyAudio` fails to build:
   ```bash
   brew install portaudio
   pip install pyaudio
   ```

4. **Set your API key** — don't put it in `config.py`. Add to
   `~/.zshrc`:
   ```bash
   export GROK_API_KEY="your-real-x.ai-key-here"
   ```
   Then `source ~/.zshrc` (or open a new terminal tab).

5. **Run it:**
   ```bash
   python run.py
   ```
   This opens `http://localhost:8000` and plays a startup sound. Click
   the mic icon and speak — the app will listen, show what it heard, and
   either open something or answer your question out loud.

6. **In VS Code**: press `Cmd+Shift+P` → "Python: Select Interpreter" →
   pick the one ending in `.venv/bin/python`, so the built-in terminal
   and any "Run" button use the right environment.

The first time you run it, macOS will prompt for **microphone access** —
approve it, or voice commands won't work.

If anything errors, paste the exact output here.
