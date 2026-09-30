import re

def extract_yt_term(command):
    """
    Extracts the search term from a YouTube voice command.
    Handles 'play [song] on youtube' as well as 'play [song]'.
    """
    command = command.lower().strip()
    
    # Match: "play <term> on youtube"
    pattern1 = r'play\s+(.*?)\s+on\s+youtube'
    match1 = re.search(pattern1, command, re.IGNORECASE)
    if match1:
        return match1.group(1).strip()
        
    # Fallback match: "play <term>"
    pattern2 = r'play\s+(.*)'
    match2 = re.search(pattern2, command, re.IGNORECASE)
    if match2:
        term = match2.group(1).replace("on youtube", "").strip()
        return term if term else command

    return command


def markdown_to_text(md):
    """
    Strips Markdown symbols (bold, italics, links, code blocks) 
    so the pyttsx3 text-to-speech engine reads clean plain text.
    """
    if not md:
        return ""

    # Remove code blocks
    text = re.sub(r'```[^\n]*\n(.*?)\n```', r'\1', md, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Remove headers (# Title)
    text = re.sub(r'#+\s+', '', text)
    # Remove bold/italics (*text* or **text**)
    text = re.sub(r'\*+([^*]+)\*+', r'\1', text)
    text = re.sub(r'_+([^_]+)_+', r'\1', text)
    # Remove Markdown links [text](url) -> keep only text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove bullet list markers (* or -)
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)

    return text.strip()