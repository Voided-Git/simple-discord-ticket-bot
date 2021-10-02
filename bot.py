import discord  # noqa
from discord.ext import commands
from lib import time_now, config, check_JSON_files, check_version
from asyncio import sleep
from time import sleep as s
from sys import exit


check_version()


if not check_JSON_files():
    print(f"{time_now()} One or multiple JSON files are missing, check the wiki for more info")
    s(5)
    exit()

elif len(config.token) != 59:
    print(f"{time_now()} Your bot token is invalid, check the wiki for more info")
    s(5)
    exit()

elif len(config.prefix.replace(" ", "")) == 0:
    print(f"{time_now()} Your bot prefix is invalid, check the wiki for more info")
    s(5)
    exit()


intents = discord.Intents.default()
intents.members = True
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
    except Exception as exc:
        print(exc)
        await sleep(5)
        exit()

    print(f"{time_now()} {bot.user.name} online")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"{time_now()} {ctx.message.author} tried using '{ctx.message.content}' but the command didn't exist. Maybe add it as an alias in config.json?")

    if isinstance(error, commands.MissingPermissions):
        print(f"{time_now()} {ctx.message.author} tried using '{ctx.message.content}' but they were lacking permissions.")

    if isinstance(error, commands.BotMissingPermissions):
        print(f"{time_now()} I don't have sufficient permissions. Make sure I have administrator!")


bot.run(config.token)
