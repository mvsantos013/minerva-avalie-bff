import re
import unicodedata

def slugify(text):
    """Converts a string to a URL-friendly slug."""

    # Convert to lowercase
    text = text.lower()

    # Remove accents and diacritics
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('ascii')

    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)

    # Remove leading/trailing hyphens
    text = text.strip('-')

    # Handle consecutive hyphens
    text = re.sub(r'-{2,}', '-', text)

    return text