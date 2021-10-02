from datetime import datetime
from json import load, dump
from requests import get


def time_now():
    """Returns the time at the time of call."""
    return datetime.now().strftime("[%H:%M:%S]")


def load_JSON(filename):
    """Loads the specified JSON file."""
    with open(filename, "r") as f:
        return load(f)


def check_integer(string):
    """Checks if the input is a valid integer."""
    try:
        int(string)
        return True

    except Exception:
        return False


def check_JSON_files():
    """Checks whether the correct JSON files exist."""
    failed = False

    try:
        load_JSON(r"config.json")
    except FileNotFoundError:
        failed = True
        print(f"{time_now()} config.json file not found")
        with open(r"config.json", "w+") as f:
            dump(
                {
                    "token": "BOT_TOKEN_HERE",
                    "prefix": "+",
                    "open-aliases": [],
                    "close-aliases": [],
                    "messages":
                    {
                        "open.existing_ticket": "You already have an ongoing ticket at {}",
                        "close.no_ticket": "You don't have an ongoing ticket yet, try using {}"
                    }
                },
                f, indent = 4
            )

    try:
        load_JSON(r"tickets/tickets.json")
    except FileNotFoundError:
        failed = True
        print(f"{time_now()} tickets.json file not found")
        with open(r"tickets/tickets.json", "w+") as f:
            dump(
                {
                    "category": 111111111111111111,
                    "support-role": 111111111111111111,
                    "ticket-number": 0,
                    "ticket-users": {}
                },
                f, indent = 4
            )

    if failed:
        return False

    else:
        return True


def check_version():
    """Checks the current version against the newest version."""
    version = float(str(get("https://rryan2448.000webhostapp.com/simple-discord-ticket-bot/version").content).replace("b", "").replace("'", ""))

    if config.version != version:
        print(f"{time_now()} Your version is outdated '{config.version}' the newest version is '{version}'")


class config:
    """Loads the config.json file as an object."""
    config = load_JSON(r"config.json")

    version = config["version"]
    token = config["token"]
    prefix = config["prefix"]
    open_aliases = config["open-aliases"]
    close_aliases = config["close-aliases"]
    _open_existing_ticket = config["messages"]["open.existing-ticket"]
    _open_open_ticket = config["messages"]["open.open-ticket"]
    _open_ticket = config["messages"]["open.ticket"]
    _close_no_ticket = config["messages"]["close.no-ticket"]
    _close_not_ticket_channel = config["messages"]["close.not-ticket-channel"]
    _close_close_ticket = config["messages"]["close.close-ticket"]
