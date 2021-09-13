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

wikilink_regex = re.compile(r'\[\[(?P<wikilink>.*?)\]\]')


@bot.event
async def on_ready() -> None:
    """Things to do when the bot readies."""
    print(f"Logged in as\n{bot.user.name}\n{bot.user.id}\nv{__version__}\n"
          + "-" * 18)
    bot.guild = typing.cast(Guild, bot.get_guild(865055891345506334))
    bot.mod_channel = bot.get_channel(constants.MOD_CHANNEL)
    bot.mod_pings = (f"{bot.guild.get_role(constants.BASED_MOD).mention} & "
                     f"{bot.guild.get_role(constants.HELPFUL_MOD).mention}")


@bot.event
async def on_message(message: Message) -> None:
    """Run on every message."""
    if message.author.discriminator != "0000":  # Ignore webhooks.
        links = wikilink.extract(message.content)
        if links:
            try:
                await message.channel.send("\n".join(wikilink.parse(i)
                                                     for i in links))
            except UserInputError:
                pass
        else:
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
