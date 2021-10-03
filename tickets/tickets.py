import discord
from discord.ext import commands
from lib import config, load_JSON, check_integer, time_now
from asyncio import sleep, TimeoutError
from json import dump
from discord.utils import get


class tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator = True)
    @commands.bot_has_permissions(administrator = True)
    async def setup(self, ctx):
        main = discord.Embed(
            color = discord.Color.random(),
            title = "Ticket Setup",
            description = "*Type your answers as question come up.*"
        )
        message = await ctx.send(embed = main)

        try:
            header = await ctx.send("What is the ticket category ID (example: `000000000000000000`)?")
            category = await self.bot.wait_for(
                "message",
                check = lambda m: m.author.id == ctx.message.author.id and m.channel.id == ctx.message.channel.id,
                timeout = 30.0
            )
        except TimeoutError:
            main.color = discord.Color.random()
            main.description += "\n\n⏲ Timed out."
            return await message.edit(embed = main)

        await header.delete()
        await category.delete()

        if not check_integer(category.content) and len(category.content) != 18:
            main.color = discord.Color.random()
            main.description += f"\n\n❌ `{category.content}` isn't valid. A category ID should look something like `000000000000000000`."
            return await message.edit(embed = main)

        main.color = discord.Color.random()
        main.add_field(
            name = "Ticket Category",
            value = f"<#{category.content}>"
        )
        await message.edit(embed = main)

        try:
            header = await ctx.send("What is the support role ID (example: `000000000000000000`)?")
            support = await self.bot.wait_for(
                "message",
                check = lambda m: m.author.id == ctx.message.author.id and m.channel.id == ctx.message.channel.id,
                timeout = 30.0
            )
        except TimeoutError:
            main.color = discord.Color.random(),
            main.description += "\n\n⏲ Timed out."
            return await message.edit(embed = main)

        await header.delete()
        await support.delete()

        if not check_integer(support.content) and len(support.content) != 18:
            main.color = discord.Color.random()
            main.description += f"\n\n❌ `{support.content}` isn't valid. A valid support role ID should look something like `000000000000000000`."
            return await message.edit(embed = main)

        main.color = discord.Color.random()
        main.add_field(
            name = "Support Role",
            value = f"<@&{support.content}>"
        )
        await message.edit(embed = main)

        tickets = load_JSON(r"tickets/tickets.json")
        tickets["category"] = int(category.content)
        tickets["support-role"] = int(support.content)

        with open(r"tickets/tickets.json", "w") as f:
            dump(tickets, f, indent = 4)

        main.color = discord.Color.random()
        main.description += "\n\n✔ Setup complete!"
        await message.edit(embed = main)

    @commands.command(
        name = "open",
        aliases = config.open_aliases
    )
    @commands.bot_has_permissions(administrator = True)
    async def _open(self, ctx):
        tickets = load_JSON(r"tickets/tickets.json")

        if str(ctx.message.author.id) not in tickets["ticket-users"]:
            tickets["ticket-number"] += 1

            if len(str(tickets["ticket-number"])) == 1:
                ticket_number = f"000{tickets['ticket-number']}"
            elif len(str(tickets["ticket-number"])) == 2:
                ticket_number = f"00{tickets['ticket-number']}"
            elif len(str(tickets["ticket-number"])) == 3:
                ticket_number = f"0{tickets['ticket-number']}"
            else:
                ticket_number = tickets["ticket-number"]

            role = get(
                ctx.message.guild.roles,
                id = tickets["support-role"]
            )
            category = get(
                ctx.message.guild.categories,
                id = tickets["category"]
            )

            if not role:
                return print(f"{time_now()} The support role ID is invalid, try reconfiguring the ID using '{config.prefix}setup'")
            elif not category:
                return print(f"{time_now()} The category ID is invalid, try reconfiguring the ID using '{config.prefix}setup'")

            channel = await ctx.message.guild.create_text_channel(
                f"ticket-{ticket_number}",
                category = category
            )

            tickets["ticket-users"][str(ctx.message.author.id)] = channel.name

            with open(r"tickets/tickets.json", "w") as f:
                dump(tickets, f, indent = 4)

            await channel.set_permissions(
                role,
                read_messages = True,
                send_messages = True,
                read_message_history = True
            )
            await channel.set_permissions(
                ctx.message.author,
                read_messages = True,
                send_messages = True,
                read_message_history = True
            )

            await ctx.send(embed = discord.Embed(
                color = discord.Color.random(),
                description = f"🎫 {config._open_open_ticket.replace('{}', channel.mention)}"
            ))
            embed = discord.Embed(
                color = discord.Color.random(),
                title = channel.name.capitalize(),
                description = config._open_ticket
            )
            embed.set_footer(
                text = ctx.message.author,
                icon_url = ctx.message.author.avatar_url
            )
            await channel.send(embed = embed)

        else:

            await ctx.send(embed = discord.Embed(
                color = discord.Color.random(),
                description = f"⚠ {config._open_existing_ticket}"
            ))

    @commands.command(
        name = "close",
        aliases = config.close_aliases
    )
    @commands.bot_has_permissions(administrator = True)
    async def _close(self, ctx):
        tickets = load_JSON(r"tickets/tickets.json")

        if "ticket-" not in ctx.channel.name:
            await ctx.send(embed = discord.Embed(
                color = discord.Color.random(),
                description = f"⚠ {config._close_not_ticket_channel.replace('{}', f'{config.prefix}close')}"
            ))

        if str(ctx.message.author.id) in tickets["ticket-users"]:
            await ctx.send(embed = discord.Embed(
                color = discord.Color.random(),
                description = f"⚠ {config._close_close_ticket}"
            ))
            await sleep(5)
            await ctx.channel.delete()

            tickets["ticket-users"].pop(str(ctx.message.author.id))

            with open(r"tickets/tickets.json", "w") as f:
                dump(tickets, f, indent = 4)

        elif get(ctx.message.guild.roles, id = tickets["support-role"]) in ctx.message.author.roles:
            for i in tickets["ticket-users"]:
                if tickets["ticket-users"][i] == ctx.message.channel.name:
                    await ctx.send(embed = discord.Embed(
                        color = discord.Color.random(),
                        description = f"⚠ {config._close_close_ticket}"
                    ))
                    await sleep(5)
                    await ctx.channel.delete()

                    tickets["ticket-users"].pop(i)

                    with open(r"tickets/tickets.json", "w") as f:
                        dump(tickets, f, indent = 4)

                    return

        else:
            await ctx.send(embed = discord.Embed(
                color = discord.Color.random(),
                description = f"⚠ {config._close_no_ticket.replace('{}', f'`{config.prefix}open`')}"
            ))


def setup(bot):
    bot.add_cog(tickets(bot))
