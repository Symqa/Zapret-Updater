# Zapret Updater by Symqa
from filedialpy import openDir
from config import JsonTools
from time import sleep
from req import download_latest_version
import sys
import zipfile
import os
from zapretCut import stop_zapret

def select_folder(isExit=False) -> None:
    folder = openDir("Упрости работу РКН (Папка zapret'a)")
    if folder:
        with JsonTools() as settings:
            settings["directory"] = folder
        version = get_version_by_bat()
        with JsonTools() as settings:
            settings["version"] = version
            print("Updated path:", folder, "\n",
                "Current version of zapret-discord:", version, "\n"
            )   
        return
    
    print(f"Exception: selected item '{folder}' is not folder\n")
    sleep(0.5)
    print("Choose (0-1):\n")
    print("1. Try again")
    print("0. Back")
    command = int(input("Enter a command: ")) 
    match command:
        case 1:
            select_folder()
        case 0:
            if isExit: sys.exit()
            pass
        case _:
            pass


def get_directory(isPrint: bool = True) -> None:
    with JsonTools() as settings:
        if isPrint:
            print("Current path to directory of zapret-discord:", settings["directory"], "\n")
        return settings["directory"]


def delete_zip(zip_abs_path: str) -> bool:
    if os.path.exists(zip_abs_path):
        os.remove(zip_abs_path)
        print("Downloaded zip file successfully deleted")
    else:
        print("Failed to delete zip archive")
        return False


def get_version_by_bat() -> str:
    with JsonTools() as settings:
        dir = settings["directory"]
        service_bat_path = os.path.join(dir, "service.bat")
        version = "0.0"
        if os.path.exists(service_bat_path):
            with open(service_bat_path, "r", encoding="UTF-8") as file:
                version = file.readlines()[1].split("=")[1].split('"')[0]
        return version



def update_zapret(directory: str, version: str):
    file_abs_path = download_latest_version(directory, version)
    if file_abs_path:
        print("\nUnpack downloaded zip file?")
        get_directory()
        print("All files will be replaced!")
        command = input("Enter (y/n): ")
        print('\n')
        if (command == "y"):
            stop_zapret()
            with zipfile.ZipFile(file_abs_path, 'r') as zip_ref:
                zip_ref.extractall(directory)
                print(f"New version of zapret discord successfully extracted into:\n", directory)
        else:
            print("Update canceled")
        delete_zip(file_abs_path)



# -------------------------------------------------------------------------
print("\n===== Zapret Updater v1.0 =====\n")

isExists = True
with JsonTools() as settings:
    if not settings:
        isExists = False
    elif not os.path.exists(settings["directory"]):
        isExists = False

if not isExists:
    print("Welcome! To start work, please, select folder of zapret-discord to update")
    sleep(3)
    select_folder(True)
# -------------------------------------------------------------------------
while True:
    current_zapret_version = get_version_by_bat()
    with JsonTools() as settings:
        settings["version"] = current_zapret_version
    print("Choose command (0-3):\n")
    print(f"--------------Zapret version v{current_zapret_version}---------------")
    print("1. Update zapret-discord version")
    print("2. Update path to zapret-discord")
    print("3. Get path to zapret-discord")
    print("0. Exit")
    print("--------------------------------------------------")
    
    command = int(input("Enter a command: "))
    match command:
        case 1:
            with JsonTools() as settings: 
                update_zapret(settings["directory"], settings["version"])
        case 2:
            select_folder()
        case 3:
            get_directory()
        case 0:
            print("\nExit")
            break
        case _:
            print("Wrong command, use (0-3)\n")
    
    sleep(1)

