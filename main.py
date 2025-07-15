import os
import aiohttp
import httpx
import asyncio
from tqdm import tqdm
from utils import DOWNLOAD_DIR, get_filename_from_url
from typing import List

MAX_RETRIES = 3

async def download_single_httpx(url: str, filename: str) -> None:
    """
    Fallback download method using httpx in case aiohttp fails.

    Args:
        url (str): The download URL.
        filename (str): Path to save the downloaded file.
    """
    async with httpx.AsyncClient() as client:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = await client.get(url, timeout=20)
                response.raise_for_status()
                with open(filename, 'wb') as f:
                    f.write(response.content)
                return
            except Exception as e:
                print(f"HTTPX attempt {attempt} failed for {url}: {e}")
                if attempt == MAX_RETRIES:
                    print(f"HTTPX fallback also failed after {MAX_RETRIES} attempts.")


async def download_single_aiohttp(session: aiohttp.ClientSession, url: str, filename: str) -> None:
    """
    Download a file using aiohttp in a single connection.
    Falls back to httpx if aiohttp fails.

    Args:
        session (aiohttp.ClientSession): The aiohttp session.
        url (str): The download URL.
        filename (str): The filename to save the download.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            async with session.get(url, timeout=20) as response:
                if response.status == 200:
                    with open(filename, 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                    return
                else:
                    raise aiohttp.ClientError(f"Non-200 response: {response.status}")
        except Exception as e:
            print(f"[ERROR] aiohttp attempt {attempt} failed for {url}: {e}")
            if attempt == MAX_RETRIES:
                print("[INFO] Trying httpx fallback...")
                await download_single_httpx(url, filename)


async def sequential_download(urls: List[str]) -> None:
    """Download files one by one (sequentially)."""
    async with aiohttp.ClientSession() as session:
        for i, url in enumerate(urls, 1):
            filename = os.path.join(DOWNLOAD_DIR, get_filename_from_url(url, i))
            print(f"Downloading (sequential): {url}")
            await download_single_aiohttp(session, url, filename)
            print(f"Saved as {filename}")


async def parallel_download(urls: List[str]) -> None:
    """Download multiple files in parallel using aiohttp."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(urls, 1):
            filename = os.path.join(DOWNLOAD_DIR, get_filename_from_url(url, i))
            tasks.append(download_single_aiohttp(session, url, filename))
        await asyncio.gather(*tasks)


async def download_chunk(client: httpx.AsyncClient, url: str, start: int, end: int, part_filename: str) -> None:
    """Download a specific byte range (chunk) of a file."""
    headers = {'Range': f'bytes={start}-{end}'}
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = await client.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            with open(part_filename, 'wb') as f:
                f.write(response.content)
            return
        except Exception as e:
            print(f"[ERROR] Chunk attempt {attempt} failed for {url} range {start}-{end}: {e}")
            if attempt == MAX_RETRIES:
                print(f"[FAILURE] Abandoning chunk {start}-{end} for {url} after {MAX_RETRIES} attempts.")


async def download_with_multiple_connections(url: str, filename: str, connections: int) -> None:
    """Download a file using multiple connections (byte range splitting)."""
    try:
        async with httpx.AsyncClient() as client:
            head = await client.head(url, timeout=20)
            head.raise_for_status()
            file_size = int(head.headers['Content-Length'])
            part_size = file_size // connections
            tasks = []
            part_filenames = []

            for i in range(connections):
                start = i * part_size
                end = file_size - 1 if i == connections - 1 else (i + 1) * part_size - 1
                part_filename = f"{filename}.part{i}"
                part_filenames.append(part_filename)
                tasks.append(download_chunk(client, url, start, end, part_filename))

            await asyncio.gather(*tasks)

            with open(filename, 'wb') as f:
                for part_file in part_filenames:
                    with open(part_file, 'rb') as pf:
                        f.write(pf.read())
                    os.remove(part_file)
    except Exception as e:
        print(f"[ERROR] Multi-connection download failed for {url}: {e}")
        print("[INFO] Falling back to single connection download...")
        await download_single_httpx(url, filename)


async def advanced_download(urls: List[str], conn_count: int) -> None:
    """Download multiple files using multiple connections per file."""
    tasks = []
    for i, url in enumerate(urls, 1):
        filename = os.path.join(DOWNLOAD_DIR, get_filename_from_url(url, i))
        tasks.append(download_with_multiple_connections(url, filename, conn_count))
    await asyncio.gather(*tasks)
