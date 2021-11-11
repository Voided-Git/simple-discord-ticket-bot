from json import load
from requests import get
from sys import exit
from os import mkdir, rename
from datetime import datetime


def time_now():
    return datetime.now().strftime("[%H:%M:%S]")


def load_JSON(filename):
    with open(filename, "r") as f:
        return load(f)


def check_version(config):
    version = float(str(get("https://rryan2448.000webhostapp.com/simple-discord-ticket-bot/version").content).replace("b", "").replace("'", ""))

    if config["version"] != version:
        print(f"{time_now()} Your version is outdated '{config['version']}' the newest version is '{version}'")


def generate_JSON(args = None):
    try:
        mkdir(r"sdtb")
        print(f"{time_now()} Created 'sdtb' directory")
    except FileExistsError:
        pass

    try:
        mkdir(r"sdtb/tickets")
        print(f"{time_now()} Created 'sdtb/tickets' directory")
    except FileExistsError:
        pass

    if not args:
        get_JSON()

    elif args.upper() == "FORCE":
        try:
            rename(r"sdtb/config.json", r"sdtb/config.json.old")
        except FileNotFoundError:
            pass

        try:
            rename(r"sdtb/tickets/tickets.json", r"sdtb/tickets/tickets.json.old")
        except FileNotFoundError:
            pass

        get_JSON()


def get_JSON():
    try:
        config = load_JSON(r"sdtb/config.json")
        check_version(config)
    except FileNotFoundError:
        print(f"{time_now()} Downloading 'config.json'")
        with open(r"sdtb/config.json", "wb") as f:
            f.write(get("https://rryan2448.000webhostapp.com/simple-discord-ticket-bot/config.json").content)
        print(f"{time_now()} Downloaded 'config.json'")

    try:
        load_JSON(r"sdtb/tickets/tickets.json")
    except FileNotFoundError:
        print(f"{time_now()} Downloading 'tickets.json'")
        with open(r"sdtb/tickets/tickets.json", "wb") as f:
            f.write(get("https://rryan2448.000webhostapp.com/simple-discord-ticket-bot/tickets.json").content)
        print(f"{time_now()} Downloaded 'tickets.json'")


def get_lib():
    try:
        mkdir(r"sdtb/lib")
    except FileExistsError:
        pass

    print(f"{time_now()} Downloading 'lib'...")
    with open(r"sdtb/lib/__init__.py", "wb") as f:
        f.write(get("https://rryan2448.000webhostapp.com/simple-discord-ticket-bot/lib/__init__.py").content)
    with open(r"sdtb/lib/lib.py", "wb") as f:
        f.write(get("https://rryan2448.000webhostapp.com/simple-discord-ticket-bot/lib/lib.py").content)
    print(f"{time_now()} Downloaded 'lib'")


def get_files():
    print(f"{time_now()} Downloading 'bot.py'...")
    with open(r"sdtb/bot.py", "wb") as f:
        f.write(get("https://rryan2448.000webhostapp.com/simple-discord-ticket-bot/bot.py").content)
    print(f"{time_now()} Downloaded 'bot.py'")

    print(f"{time_now()} Downloading 'tickets.py'...")
    with open(r"sdtb/tickets/tickets.py", "wb") as f:
        f.write(get("https://rryan2448.000webhostapp.com/simple-discord-ticket-bot/tickets.py").content)
    print(f"{time_now()} Downloaded 'tickets.py'")


while True:
    cont = input("Are you sure you want to continue with the setup, this will delete any existing files related to the simple Discord ticket bot (Y/n)?")
    if cont.lower() in ("n", "no"):
        exit()

    elif cont.upper() in ("Y", "YES"):
        break

while True:
    full = input("Would you like a full setup, just the default / updated JSON files, just the default / updated bot files or lib (F/j/fi/l)?")
    if full.lower() in ("j", "json"):
        generate_JSON("FORCE")
        exit()

    elif full.lower() in ("l", "lib"):
        get_lib()
        exit()

    elif full.lower() in ("fi", "files"):
        get_files()
        exit()

    elif full.upper() in ("F", "FULL"):
        break


generate_JSON()
get_files()
get_lib()
