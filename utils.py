import os
from urllib.parse import urlparse

# Directory where downloaded files will be saved
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_filename_from_url(url: str, index: int) -> str:
    """
    Generate a filename from the given URL. If the URL doesn't contain a valid filename,
    use a fallback name with .bin extension.

    Args:
        url (str): The download URL.
        index (int): Index of the URL in the list (used for naming uniqueness).

    Returns:
        str: The generated filename.
    """
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)
    if name and '.' in name:
        return f"{index}_{name}"
    else:
        return f"file_{index}.bin"