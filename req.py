import requests
from bs4 import BeautifulSoup
import os
import sys

def download_latest_version(directory: str, current_version: str) -> str:
    version = get_latest_version()
    if not version:
        print("Exception: can't search last version from github")
    print("Version to download:", version)
    print("Current version on device:", current_version)
    if version == current_version:
        print("Exception: current version of zapret-discord is latest")
        return
    filename = f"zapret-discord-youtube-{version}.zip"
    download_url = f"https://github.com/Flowseal/zapret-discord-youtube/releases/download/{version}/{filename}"
    print("Request files from github...")
    try:
        responce = requests.get(download_url, stream=True, timeout=(10, 30))
    except:
        print("Exception: github doesn't responce, please try on VPN")
        return
    total_size = int(responce.headers.get('content-length', 0))
    downloaded = 0
    chunk_size = 8192

    file_abs_path = os.path.join(directory, filename)

    if responce.status_code == 200:
        with open(file_abs_path, "wb") as file:
            for chunk in responce.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    downloaded+=len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        sys.stdout.write(f"\r\033[KDownloaded: {percent:.1f}%")
                    else:
                        sys.stdout.write(f"\r\033[KDownloaded: {downloaded} bytes")
                    sys.stdout.flush()
        print("\nZip file of zapret-discord has successfully downloaded")
        return file_abs_path

    else:
        print("Exception: cannot connect to github, status code:", responce.status_code)



def get_latest_version() -> str:
    responce = requests.get("https://github.com/Flowseal/zapret-discord-youtube/releases")
    if responce.status_code == 200:
        soup = BeautifulSoup(responce.text, 'html.parser')
        version = soup.find_all("section")[0].find("h2").get_text()
    else:
        return
    
    return version



