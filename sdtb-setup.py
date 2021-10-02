from json import dump
from requests import get
from sys import exit
from os import mkdir
from datetime import datetime


def time_now():
    return datetime.now().strftime("[%H:%M:%S]")


def generate_JSON():
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

    with open(r"sdtb/tickets/tickets.json", "w+") as f:
        dump(
            {
                "category": 111111111111111111,
                "support-role": 111111111111111111,
                "ticket-number": 0,
                "ticket-users": {}
            },
            f, indent = 4
        )
    print(f"{time_now()} Created 'tickets.json'")

    with open(r"sdtb/config.json", "w+") as f:
        dump(
            {
                "version": 1.0,
                "token": "BOT_TOKEN_HERE",
                "prefix": "+",
                "open-aliases": [],
                "close-aliases": [],
                "messages":
                {
                    "open.existing-ticket": "You already have an ongoing ticket.",
                    "open.open-ticket": "Ticket created at {}.",
                    "open.ticket": "Please describe your issue in as much detail as possible so the support team can respond to you as quickly as possible.\n\nIf you do not receive a response shortly, please be patient as the support team may be busy with other tickets or not currently available.",
                    "close.no-ticket": "You don't have an ongoing ticket yet, try using {}.",
                    "close.not-ticket-channel": "You can only execute {} in a ticket channel.",
                    "close.close-ticket": "Deleting ticket in 5 seconds."
                }
            },
            f, indent = 4
        )
    print(f"{time_now()} Created 'config.json'")


while True:
    cont = input("Are you sure you want to continue with the setup, this will delete any existing files related to the simple Discord ticket bot (Y/n)?")
    if cont.lower() in ("n", "no"):
        exit()

    elif cont.upper() in ("Y", "YES"):
        break

while True:
    full = input("Would you like a full setup or just the default JSON files (F/j)?")
    if full.lower() in ("j", "json"):
        generate_JSON()
        exit()

    elif full.upper() in ("F", "FULL"):
        break


generate_JSON()

print(f"{time_now()} Downloading 'bot.py'...")
with open(r"sdtb/bot.py", "wb") as f:
    f.write(get("https://rryan2448.000webhostapp.com/simple-discord-ticket-bot/bot.py").content)
print(f"{time_now()} Downloaded 'bot.py'")

print(f"{time_now()} Downloading 'tickets.py'...")
with open(r"sdtb/tickets/tickets.py", "wb") as f:
    f.write(get("https://rryan2448.000webhostapp.com/simple-discord-ticket-bot/tickets.py").content)
print(f"{time_now()} Downloaded 'tickets.py'")

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
