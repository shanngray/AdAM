import re

def sanitize_name(name):
    """Sanitize the name to comply with OpenAI's API requirements."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)