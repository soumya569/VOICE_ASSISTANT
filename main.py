import os
import webbrowser
import eel

# Import feature functions and voice commands
from engine.features import *
from engine.command import *
from engine.config import ASSISTANT_NAME


def start():
    # 1. Initialize Eel with web root directory 'www'
    eel.init("www")

    # 2. Play startup sound chime
    playAssistantSound()

    @eel.expose
    def init():
        """
        Triggered when index.html finishes loading.
        Bypasses face auth screens and boots directly to main dashboard.
        """
        try:
            # Transition directly to active assistant screen
            eel.hideStart()
            
            # Greeting
            greeting = f"Hello, I am {ASSISTANT_NAME}. How can I help you today?"
            speak(greeting)
            
        except Exception as e:
            print("Initialization transition error:", e)

    # 3. Open browser and start local Eel server on port 8000
    print(f"[*] Starting {ASSISTANT_NAME} AI Desktop Assistant...")
    webbrowser.open("http://localhost:8000/index.html")
    
    eel.start('index.html', mode=None, host='localhost', port=8000, block=True)


if __name__ == "__main__":
    start()