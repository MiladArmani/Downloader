🚀 Python Download Manager

A lightweight yet powerful Download Manager written in Python 3, supporting different download strategies using aiohttp and httpx.

📌 Features
.✅ Sequential downloads (one by one)
.✅ Parallel downloads (multiple files at once)
.✅ Multi-connection downloads (split into chunks for faster speed)
.✅ Automatic retry system on failure
.✅ Saves all files into a downloads folder
.✅ Fallback from aiohttp to httpx if one fails

📂 Project Structure
download-manager/
│── main.py        # Core download logic
│── utils.py       # Helper functions and path management
│── requirements.txt
│── README.md
│── downloads/     # Downloaded files are stored here

⚙️ Installation

1. Clone the repository
git clone https://github.com/USERNAME/download-manager.git
cd download-manager

2. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

▶️ Usage Example
import asyncio
from main import sequential_download, parallel_download, advanced_download

urls = [
    "https://example.com/file1.zip",
    "https://example.com/file2.mp4",
]

# Sequential download
asyncio.run(sequential_download(urls))

# Parallel download
# asyncio.run(parallel_download(urls))

# Multi-connection download (faster)
# asyncio.run(advanced_download(urls, conn_count=4))

📦 Dependencies
.aiohttp
.httpx
.tqdm
