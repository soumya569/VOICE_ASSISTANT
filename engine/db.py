"""
Sets up jarvis.db on first run with OS-aware application paths.
"""

import sqlite3
import platform

def init_db():
    con = sqlite3.connect("jarvis.db")
    cursor = con.cursor()

    # Create required tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS sys_command
                       (id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS web_command
                       (id INTEGER PRIMARY KEY, name VARCHAR(100), url VARCHAR(1000))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                       (id INTEGER PRIMARY KEY, name VARCHAR(200), mobile_no VARCHAR(255),
                        email VARCHAR(255), city VARCHAR(255))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS info
                       (name VARCHAR(100), designation VARCHAR(50), mobileno VARCHAR(40),
                        email VARCHAR(200), city VARCHAR(300))''')
    con.commit()

    # Detect Operating System to set correct default application paths
    is_windows = platform.system() == "Windows"

    cursor.execute("SELECT COUNT(*) FROM sys_command")
    if cursor.fetchone()[0] == 0:
        if is_windows:
            default_apps = [
                ("chrome", "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"),
                ("google chrome", "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"),
                ("notepad", "notepad.exe"),
                ("calculator", "calc.exe"),
            ]
        else:  # macOS / Linux
            default_apps = [
                ("chrome", "/Applications/Google Chrome.app"),
                ("google chrome", "/Applications/Google Chrome.app"),
                ("whatsapp", "/Applications/WhatsApp.app"),
            ]

        cursor.executemany(
            "INSERT INTO sys_command (name, path) VALUES (?, ?)", default_apps
        )
        con.commit()

    # Seed web commands (identical across all OS platforms)
    cursor.execute("SELECT COUNT(*) FROM web_command")
    if cursor.fetchone()[0] == 0:
        default_sites = [
            ("youtube", "https://www.youtube.com"),
            ("whatsapp web", "https://web.whatsapp.com"),
            ("google", "https://www.google.com"),
        ]
        cursor.executemany(
            "INSERT INTO web_command (name, url) VALUES (?, ?)", default_sites
        )
        con.commit()

    con.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")