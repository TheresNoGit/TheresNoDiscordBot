"""Good cabal bot"""
import discord
import re
from discord.ext.commands import (Bot, Context, CommandError, CommandNotFound,
                                  UserInputError, MissingAnyRole)

import cogs
import constants

__version__ = constants.VERSION

bot = Bot(command_prefix='!',
          description="Based TheresNoBot\nCurrently just converting wikilinks for cabal goodness, but who knows what comes next",
          intents=discord.Intents.default(),
          case_insensitive=True)

wikilink_regex = re.compile('\[\[(?P<wikilink>.*?)\]\]')


@bot.event
async def on_ready() -> None:
    """Things to do when the bot readies."""
    print(f"Logged in as\n{bot.user.name}\n{bot.user.id}\nv{__version__}\n"
          + "-" * 18)


@bot.event
async def on_message(message):
    user = message.author
    channel = message.channel
    content = message.content
    wikilink_match = wikilink_regex.match(content)

    if wikilink_match:
        msg = f"{constants.ENWIKI_URL}{wikilink_match.group('wikilink')}"
        await channel.send(msg)

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx: Context,
                           error: CommandError) -> None:
    """Notify a user that they have not provided an argument."""
    print(error)
    replies = {
        UserInputError: ("*You need to use the correct syntax...* "
                         f"Type `!help {ctx.command}` for more information."),
        CommandNotFound: ("*You need to use a valid command...* "
                          "Type `!help` for a list of commands."),
        MissingAnyRole: ("You don't appear to have the correct role for this command. lel.")
    }
    for k, v in replies.items():
        if isinstance(error, k):
            await ctx.send(v)
            break
    else:
        await ctx.send("Unknown error.  Scream (at Tamzin cos this code is mostly hers).")


for cog in (cogs.BotInternal, cogs.Mod):
    bot.add_cog(cog(bot))


bot.run(constants.DISCORD_KEY)
