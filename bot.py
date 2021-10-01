"""Good cabal bot."""
import random
import re
import typing

import discord
from discord import Guild, Message
from discord.ext.commands import (Bot, Context, CommandError, CommandNotFound,
                                  UserInputError, MissingAnyRole)

import cogs
import constants
import wikilink

__version__ = constants.VERSION

bot = Bot(command_prefix='~',
          description=("Based TheresNoBot\nCurrently just converting wikilinks"
                       " for cabal goodness, but who knows what comes next"),
          intents=discord.Intents.default(),
          case_insensitive=True)

funfact_regex = re.compile(r'^fun fact', re.IGNORECASE)
devon_regex = re.compile(r'.*devon', re.IGNORECASE)
sock_regex = re.compile(r'.*sock(puppet)?', re.IGNORECASE)


async def checkMessage(message: Message) -> bool:
    """Check a message against the regexes"""
    links = wikilink.extract(message.content)
    if links:
        await message.channel.send("\n".join(links))
        return True
    elif funfact_regex.match(message.content):
        await message.reply("Is it *really* a fun fact though...?")
        return True
    elif devon_regex.match(message.content):
        await message.reply("*That* had better have been an insult about Devon.")
        return True
    elif sock_regex.match(message.content):
        await message.add_reaction("🧦")
        return True
    else:
        return False


@bot.event
async def on_ready() -> None:
    """Things to do when the bot readies."""
    print(f"Logged in as\n{bot.user.name}\n{bot.user.id}\nv{__version__}\n"
          + "-" * 18)
    bot.guild = typing.cast(Guild, bot.get_guild(865055891345506334))
    bot.mod_channel = bot.get_channel(constants.MOD_CHANNEL)
    bot.all_mod_channel = bot.get_channel(constants.ALL_MOD_CHANNEL)
    bot.mod_pings = (f"{bot.guild.get_role(constants.MOD_PLUS_PLUS).mention} & "
                     f"{bot.guild.get_role(constants.MOD).mention} & "
                     f"{bot.guild.get_role(constants.HALF_MOD).mention}")


@bot.event
async def on_message(message: Message) -> None:
    """Run on every message."""
    if message.author.discriminator != "0000":  # Ignore webhooks.
        if message.author.id != constants.BOT_ID: # Ignore self.
            if await checkMessage(message) == False:
                await bot.process_commands(message)
            

@bot.event
async def on_command_error(ctx: Context,
                           error: CommandError) -> None:
    """Notify a user that they have not provided an argument."""
    if ctx.message.content.startswith("~~"):
        return
    print(error)
    replies = {
        UserInputError: ("*You need to use the correct syntax...* "
                         f"Type `~help {ctx.command}` for more information."),
        CommandNotFound: ("*You need to use a valid command...* "
                          "Type `~help` for a list of commands."),
        MissingAnyRole: ("You don't appear to have the correct role for this command. lel.")
    }
    for k, v in replies.items():
        if isinstance(error, k):
            await ctx.send(v)
            break
    else:
        await ctx.send("Unknown error.  Scream (at Tamzin cos this code is mostly "
                       f"{random.choice(['hers', 'theirs', 'xyrs'])}).")


for cog in (cogs.BotInternal, cogs.Mod, cogs.General):
    bot.add_cog(cog(bot))


bot.run(constants.DISCORD_KEY)
