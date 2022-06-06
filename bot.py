from asyncio import sleep
from time import sleep as s
import sys
from discord import ExtensionError, Intents
from discord.ext import commands
try:
    from lib import time_now, config, check_JSON_files, check_version, setup_change
except ImportError:
    from datetime import datetime
    print(f"{datetime.now().strftime('[%H:%M:%S]')} Lib is missing, consider using 'sdtb-setup.exe' to download the required dependencies")
    s(5)
    sys.exit()


check_version()
setup_change()


if not check_JSON_files():
    print(f"{time_now()} One or multiple JSON files are missing, check the wiki for more info")
    s(5)
    sys.exit()

elif len(config.token) < 30:
    print(f"{time_now()} Your bot token is invalid, check the wiki for more info")
    s(5)
    sys.exit()

elif len(config.prefix.replace(" ", "")) == 0:
    print(f"{time_now()} Your bot prefix is invalid, check the wiki for more info")
    s(5)
    sys.exit()


intents = Intents.default()
intents.members = True  # pylint: disable=E0237
bot = commands.Bot(
    command_prefix = config.prefix,
    case_insensitive = True,
    intents = intents
)


@bot.event
async def on_ready():
    print(f"{time_now()} {bot.user.name} loading...")

    try:
        bot.load_extension("tickets.tickets")
        print(f"{time_now()} Loaded 'tickets'")
    except ExtensionError as exc:
        print(exc)
        await sleep(5)
        sys.exit()

    print(f"{time_now()} {bot.user.name} online")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"{time_now()} {ctx.message.author} tried using '{ctx.message.content}' but the command didn't exist. Maybe add it as an alias in config.json?")

    if isinstance(error, commands.MissingPermissions):
        print(f"{time_now()} {ctx.message.author} tried using '{ctx.message.content}' but they were lacking permissions.")

    if isinstance(error, commands.BotMissingPermissions):
        print(f"{time_now()} I don't have sufficient permissions. Make sure I have administrator!")


print(f"{time_now()} Consider changing to simple discord bot (https://github.com/Voided-Git/simple-discord-bot) from Voided, it is being actively maintained unlike this project.")

bot.run(config.token)
