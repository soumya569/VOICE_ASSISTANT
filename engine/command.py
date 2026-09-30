import os
import time
import platform
import pyttsx3
import speech_recognition as sr
import eel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client using your free API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

def speak(text):
    text = str(text)
    if platform.system() == 'Windows':
        engine = pyttsx3.init('sapi5')
    else:
        engine = pyttsx3.init()
        
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
    
    engine.setProperty('rate', 174)
    
    # Send messages to JavaScript frontend via Eel
    try:
        eel.DisplayMessage(text)
        eel.receiverText(text)
    except Exception as e:
        print("UI update error:", e)

    engine.say(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening....')
        eel.DisplayMessage('Listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)

    try:
        print('Recognizing via Groq Whisper...')
        eel.DisplayMessage('Recognizing....')
        
        # Save temporary audio file for Groq Whisper transcription
        temp_audio_path = "temp_speech.wav"
        with open(temp_audio_path, "wb") as f:
            f.write(audio.get_wav_data())

        # Call Groq's 100% free Whisper API
        with open(temp_audio_path, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(temp_audio_path, file.read()),
                model="whisper-large-v3",
                response_format="json",
                language="en",
            )

        # Cleanup temporary audio file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

        query = transcription.text.strip()
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(1)
        return query.lower()

    except Exception as e:
        print("Transcription Error:", e)
        eel.DisplayMessage("Could not understand audio.")
        return ""


@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        if not query:
            return
        eel.senderText(query)
    else:
        query = str(message).lower()
        eel.senderText(query)

    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        else:
            # Route all general queries to Groq LLM
            from engine.features import grok
            grok(query)
            
    except Exception as e:
        print("Execution Error:", e)
    
    eel.ShowHood()