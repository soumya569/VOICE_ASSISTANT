import os
from dotenv import load_dotenv

# Load variables from a .env file if available
load_dotenv()

# Assistant Identity
ASSISTANT_NAME = "Soumya"

# Groq API Configuration
# Reads GROQ_API_KEY from environment, with a fallback to GROK_API_KEY for backward compatibility
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Model Definitions
GROQ_LLM_MODEL = "openai/gpt-oss-120b"
GROQ_WHISPER_MODEL = "whisper-large-v3"

# System Prompt to guide the assistant's personality
SYSTEM_PROMPT = f"You are {ASSISTANT_NAME}, a desktop AI voice assistant. Keep your responses short, concise, natural, and conversational (under 3 sentences) so they sound good when spoken aloud."

if not GROQ_API_KEY:
    print(
        "[config] WARNING: Neither GROQ_API_KEY nor GROK_API_KEY environment variables are set. "
        "AI responses and Whisper transcription will fail."
    )