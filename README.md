# Simple Discord Ticket Bot **(SDTB)** #
A simple ticket bot for your Discord server's needs, written in Python using the Discord API wrapper. A lot of ticket bots for Discord exist all over the web, this one might not be the best one, but give it a try, it's quite simple, and if you ever need help, you can join the official [Discord server](https://discord.gg/DQMgmn6keK "GitHub/RRyan2447") for support from the community or the developers themselves.
- - - -
### **Setup using the source code** ###
If you're planning to use the source code instead of the .exe, run `setup.py` and let it generate the essential JSON files required for operation. You can edit `config.json` to suit your needs and preferences, however you shouldn't directly edit `tickets.json` as you can configure it within Discord.
- - - -
### **Setup using the release** ###
If you're planning to use the release version, run the `setup.exe` and let it generate the essential files required for operation. You can edit `config.json` to suit your needs and preferences, however you shouldn't directly edit `tickets.json` as you can configure it within Discord.
- - - -
### **Running the bot** ###
Make sure to install [Python](https://python.org "Python") and the following packages using `pip install`:
* [Discord.py](https://discordpy.readthedocs.io/en/stable/ "Discord.py docs") (`pip install discord`)

After you've installed Python and all the dependencies, you can run the bot by running `bot.py`.
- - - -
### **Tickets Configuration** ###
To configure the ticket system, you need to enable developer mode on Discord, go to `User Settings → Advanced → Developer Mode → enable developer mode`. Afer enabling developer mode, add the bot to your server, run the bot (using `bot.exe` or `bot.py`), type `+setup` (<kbd>+</kbd> is the default prefix, you may have changed the bot's prefix within the `config.json` file) and type the responses to configure the ticket system accordingly.
- - - -
### **Features included within the bot:** ###
* Customisable prefix
* Customisable aliases for `open` and `close` commands
* Customisable messages
* Understandable error handling
* Highly customisable in general
* Quick issue responses
* Community suggestions for improving the code and releases
* Hosting available by the developer (contact them using their [Discord server](https://discord.gg/DQMgmn6keK "GitHub/RRyan2447"))
* Update version checker