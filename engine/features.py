import json
import os
import platform
import sqlite3
import subprocess
import webbrowser
from playsound3 import playsound
import eel
from engine.command import speak
from engine.config import ASSISTANT_NAME, GROQ_API_KEY, GROQ_LLM_MODEL
import pywhatkit as kit
from openai import OpenAI

from engine.helper import extract_yt_term, markdown_to_text
from engine.db import init_db

# Ensure database tables exist
init_db()

con = sqlite3.connect("jarvis.db", check_same_thread=False)
cursor = con.cursor()


def _open_path(path):
    """Cross-platform app launcher."""
    system = platform.system()
    if system == 'Windows':
        os.startfile(path)
    elif system == 'Darwin':
        subprocess.call(['open', path])
    else:
        subprocess.call(['xdg-open', path])


@eel.expose
def playAssistantSound():
    music_dir = "www/assets/audio/start_sound.mp3"
    try:
        playsound(music_dir)
    except Exception as e:
        print("Sound play error:", e)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    app_name = query.strip().lower()

    if app_name != "":
        try:
            # 1. Search in local app shortcuts
            cursor.execute('SELECT path FROM sys_command WHERE LOWER(name) = ?', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + app_name)
                _open_path(results[0][0])
                return

            # 2. Search in web shortcuts
            cursor.execute('SELECT url FROM web_command WHERE LOWER(name) = ?', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + app_name)
                webbrowser.open(results[0][0])
                return

            # 3. Fallback OS execution
            speak("Opening " + app_name)
            if platform.system() == 'Darwin':
                subprocess.call(['open', '-a', app_name])
            elif platform.system() == 'Windows':
                os.system('start ' + app_name)
            else:
                subprocess.call(['xdg-open', app_name])

        except Exception as e:
            print("openCommand error:", e)
            speak("Something went wrong while opening " + app_name)


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)


# Initialize Groq client using OpenAI SDK compatibility layer
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def grok(query):
    try:
        query = query.replace(ASSISTANT_NAME, "")
        query = query.replace("search", "").strip()

        if not query:
            return

        # Request response from Groq using Llama 3.3
        response = client.chat.completions.create(
            model=GROQ_LLM_MODEL,
            messages=[
                {
                    "role": "system", 
                    "content": f"You are {ASSISTANT_NAME}, a desktop voice assistant. Keep answers brief (under 3 sentences) and natural."
                },
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=150
        )

        raw_text = response.choices[0].message.content
        filter_text = markdown_to_text(raw_text)

        speak(filter_text)

    except Exception as e:
        print("Groq API Error:", e)
        speak("I am having trouble connecting to my brain right now.")


# ---------------------------------------------------------------------
# Settings panel support (Eel-exposed functions called from HTML/JS)
# ---------------------------------------------------------------------

@eel.expose
def assistantName():
    return ASSISTANT_NAME


@eel.expose
def personalInfo():
    try:
        cursor.execute("SELECT * FROM info")
        results = cursor.fetchall()
        if results:
            jsonArr = json.dumps(results[0])
            eel.getData(jsonArr)
        return 1
    except Exception as e:
        print("no data", e)


@eel.expose
def updatePersonalInfo(name, designation, mobileno, email, city):
    cursor.execute("SELECT COUNT(*) FROM info")
    count = cursor.fetchone()[0]

    if count > 0:
        cursor.execute(
            '''UPDATE info 
               SET name=?, designation=?, mobileno=?, email=?, city=?''',
            (name, designation, mobileno, email, city)
        )
    else:
        cursor.execute(
            '''INSERT INTO info (name, designation, mobileno, email, city) 
               VALUES (?, ?, ?, ?, ?)''',
            (name, designation, mobileno, email, city)
        )

    con.commit()
    personalInfo()
    return 1


@eel.expose
def displaySysCommand():
    cursor.execute("SELECT * FROM sys_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displaySysCommand(jsonArr)
    return 1


@eel.expose
def deleteSysCommand(id):
    cursor.execute("DELETE FROM sys_command WHERE id = ?", (id,))
    con.commit()


@eel.expose
def addSysCommand(key, value):
    cursor.execute(
        '''INSERT INTO sys_command (name, path) VALUES (?, ?)''', (key, value))
    con.commit()


@eel.expose
def displayWebCommand():
    cursor.execute("SELECT * FROM web_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayWebCommand(jsonArr)
    return 1


@eel.expose
def addWebCommand(key, value):
    cursor.execute(
        '''INSERT INTO web_command (name, url) VALUES (?, ?)''', (key, value))
    con.commit()


@eel.expose
def deleteWebCommand(id):
    cursor.execute("DELETE FROM web_command WHERE id = ?", (id,))
    con.commit()


@eel.expose
def displayPhoneBookCommand():
    cursor.execute("SELECT * FROM contacts")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayPhoneBookCommand(jsonArr)
    return 1


@eel.expose
def deletePhoneBookCommand(id):
    cursor.execute("DELETE FROM contacts WHERE id = ?", (id,))
    con.commit()


@eel.expose
def InsertContacts(Name, MobileNo, Email, City):
    cursor.execute(
        '''INSERT INTO contacts (name, mobile_no, email, city) VALUES (?, ?, ?, ?)''',
        (Name, MobileNo, Email, City))
    con.commit()