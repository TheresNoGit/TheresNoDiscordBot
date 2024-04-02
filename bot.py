"""Good cabal bot."""
import random
import typing
import datetime
import asyncio
import discord
from discord import Guild, Message, Embed, Member
from discord.ext.commands import (Bot, Context, CommandError, CommandNotFound,
                                  UserInputError, MissingAnyRole)

import cogs
import constants
import wikilink
import utils

__version__ = constants.VERSION

bot = Bot(command_prefix='~',
          description=("Based TheresNoBot\nCurrently just converting wikilinks"
                       " for cabal goodness, but who knows what comes next"),
          intents=discord.Intents.all(),
          case_insensitive=True)


async def checkMessage(message: Message) -> bool:
    """Check a message against the regexes"""
    if await utils.isDM(message):
        # Message is a DM
        await message.channel.send("Not yet implemented, sorry...")
        # TODO: Probably another function to deal with any DM commands
        return True
    else:
        if await utils.isEmbed(message):
            return False # TODO: No longer have any embed actions, refactor/remove?
        else:
            # Message is not a DM nor an embed
            links = wikilink.extract(message.content)
            if links:
                await message.channel.send("\n".join(links))
                return True
            else:
                return False


@bot.event
async def on_ready() -> None:
    """Things to do when the bot readies."""
    now_utc = await utils.getUTC()
    print(f"{now_utc}\n" + "-" * 18)
    if constants.DEV:
        print("In development mode...\n" + "-" * 18)
    print(f"Logged in as\n{bot.user.name}\n{bot.user.id}\nv{constants.VERSION} ({constants.VERSION_NAME})\n"
          + "-" * 18)
    bot.guild = typing.cast(Guild, bot.get_guild(constants.GUILD))
    bot.mod_channel = bot.get_channel(constants.MOD_CHANNEL)
    bot.spam_channel = bot.get_channel(constants.BOT_SPAM_CHANNEL)
    bot.commands_channel = bot.get_channel(constants.COMMANDS_CHANNEL)
    bot.all_mod_channel = bot.get_channel(constants.ALL_MOD_CHANNEL)
    bot.welcome_channel = bot.get_channel(constants.WELCOME_CHANNEL)
    bot.mod_pings = (f"{bot.guild.get_role(constants.MOD_PLUS_PLUS).mention} & "
                     f"{bot.guild.get_role(constants.MOD).mention} & "
                     f"{bot.guild.get_role(constants.HALF_MOD).mention}")
    bot.custom_activity = constants.BOT_ACTIVITY
    await utils.sendLoggerMessage(bot, f"Restarted OK (v{__version__})", False)
    await bot.change_presence(activity=discord.Game(name=f"{bot.custom_activity}"))


@bot.event
async def on_member_join(member: Member) -> None:
    """Things to do when a new member joins"""
    embed = Embed(
        title="A new member just joined..",
        description=(f"🎉 Everyone please welcome {member.mention}! 🎉\n\n"
                    f"This server is run by <@{constants.USER_OWNER}>, and has a bit of everything - we're really glad you're here 🙂\n\n"
                    "**Hold up!**\n"
                    f"You're currently <@&{constants.NEW}>, and need the <@&{constants.TRUSTED}> role before you can start joining channels.\n"
                    "Normally a mod will give it to you pretty quick, but if you've been waiting for a little while, "
                    "please type **`~trustme`** and I'll give them a nudge! 😜\n\n"
                    f"Once you have the role, you'll then be able to go into the <#{constants.META_CHANNEL}> "
                    "channel and grab some more *interesting* roles, "
                    "which will open the server up a bit more.\n\n"
                    "Lastly, just so we know which invites are getting used, could you *react* to answer the below? 😅\n\n"
                    "**Where did you find the invite?**\n"
                    " - If you found it on Twitter, click the 🐦\n"
                    " - If you were invited directly by someone, click on the 🗣️\n"
                    " - Or maybe you found it somewhere else? That's a *bit sus*, but its okay.. click on the 👀\n"),
        type="rich",
        color=constants.DEBUG_COL,
        timestamp=datetime.datetime.utcnow()
    )
    reacts = ['🐦', '🗣️', '👀']

    # We assume that because its a new member join, that they'll be in the "welcome channel"
    message = await bot.welcome_channel.send(embed=embed)

    # Add reacts
    for react in reacts:
        await message.add_reaction(react)
    
    # Notify mods
    await cogs.BotInternal.notifyModsOfNewMember(bot, member)


@bot.event
async def on_message(message: Message) -> None:
    """Run on every message."""
    if message.author.discriminator != "0000":  # Ignore webhooks.
        if not message.is_system() and message.author.id != bot.user.id: # Ignore self.
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
        await utils.sendLoggerMessage(bot, f"Got an unknown error in `on_command_error`", True)
        await ctx.send("Unknown error.  Scream (at Tamzin cos this code is mostly "
                       f"{random.choice(['hers', 'theirs', 'xyrs'])}).")

async def setup():
    for cog in (cogs.BotInternal, cogs.Mod, cogs.General):
        await bot.add_cog(cog(bot))

asyncio.run(setup())

bot.run(constants.DISCORD_KEY)
