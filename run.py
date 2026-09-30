"""
Entry point for the Soumya AI Voice Assistant.
Executes database initialization and boots the main Eel desktop interface.
"""

from engine.db import init_db
from main import start

if __name__ == '__main__':
    # Guarantee local SQLite tables exist on first run
    init_db()
    
    # Boot Eel desktop server
    start()