import asyncio
from main import sequential_download, parallel_download, advanced_download

def get_urls() -> list[str]:
    urls = []
    print("Enter URLs (empty line to finish):")
    while True:
        url = input("URL: ").strip()
        if not url:
            break
        urls.append(url)
    return urls

def get_choice() -> str:
    print("\nChoose download mode:")
    print("1 - Sequential")
    print("2 - Parallel")
    print("3 - Advanced (multiple connections per file)")
    return input("Your choice: ").strip()

def get_connections() -> int:
    while True:
        try:
            conn = int(input("Number of connections per file (1-16): "))
            if 1 <= conn <= 16:
                return conn
            else:
                print("Please enter a number between 1 and 16.")
        except ValueError:
            print("Invalid input, please enter a number.")

async def main():
    urls = get_urls()
    if not urls:
        print("No URLs provided. Exiting.")
        return

    choice = get_choice()

    if choice == "1":
        await sequential_download(urls)
    elif choice == "2":
        await parallel_download(urls)
    elif choice == "3":
        connections = get_connections()
        await advanced_download(urls, connections)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    asyncio.run(main())
