"""Cogs (categories of bot command)"""
import random
import discord
import datetime

from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context

import constants

class General(Cog, name="General"):  # type: ignore
    """General commands"""
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self._genders = [
            "female", "male", "demigirl", "demiguy", "agender", "demigender",
            "genderfluid", "genderflux", "fluidflux", "xenogender", "cat",
            "dog", "NaN", "no thanks", "404 not found", "gayyyyy",
            "currently being discussed at Articles for deletion", "villain",
            "French", "ruled safe at third, but play currently under review"
        ]

    @commands.command(aliases=['gender'])
    async def whatsmygender(self, ctx: Context) -> None:
        """Because sometimes figuring out your own gender is too hard."""
        await ctx.send(
            f"Looks like your gender is {random.choice(self._genders)}.\n"
            "Does that not sound right? It's possible that it's changed "
            "already! Feel free to ask again."
        )

    @commands.command(aliases=['mods'])
    async def mod(self, ctx: Context, *, reason: str) -> None:
        """Requests mod attention for a given reason. Usage: ~mod {reason}"""
        await self.bot.all_mod_channel.send(
            f"{self.bot.mod_pings}: {ctx.message.author.mention} requests mod "
            f"attention in {ctx.channel.mention}. Reason: {reason}"
        )

    @commands.command()
    async def trustme(self, ctx: Context) -> None:
        """Nudges the mods to give you the `trusted` role. Usage: ~trustme"""
        await self.bot.all_mod_channel.send(
            f"{self.bot.mod_pings}: {ctx.message.author.mention} wants the "
            f"*trusted* role in {ctx.message.channel.mention} – hopp hopp!"
        )


class Mod(Cog, name="Moderation"):  # type: ignore
    """Mod-only commands"""
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.has_any_role('mod', 'half mod')
    async def trust(self, ctx: Context, *, member: Member) -> None:
        "Sets a user as trusted. Usage: ~trust {username}"
        await member.add_roles(self.bot.guild.get_role(constants.TRUSTED))
        await ctx.send(f"Setting {member.mention} as trusted")

    @commands.command()
    @commands.has_any_role('mod', 'half mod')
    async def untrust(self, ctx: Context, *, member: Member) -> None:
        "Sets a user as no longer trusted. Usage: ~untrust {username}"
        await member.remove_roles(self.bot.guild.get_role(constants.TRUSTED))
        await ctx.send(f"Setting {member.mention} as no longer trusted")

    @commands.command()
    @commands.has_any_role('mod', 'half mod')
    async def spite(self, ctx: Context, *, member: Member) -> None:
        "Spite a user. Usage: ~spite {username}"
        await ctx.send(f"Consider yourself spited, {member.mention}")


class BotInternal(Cog, name="Bot Internal", command_attrs={'hidden': True}):  # type: ignore
    """Commands that relate to the bot itself."""
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def notifyModsOfNewMember(bot: Bot, member: Member) -> None:
        "Send a notification to the mod channel of a new member"
        if not constants.DEV:
            await bot.all_mod_channel.send(f"{member.mention} has just joined in <#{constants.WELCOME_CHANNEL}>")
    
    @commands.command()
    async def version(self, ctx: Context) -> None:
        "Gets the bots current version number"
        embed = Embed(
            title=f"TheresNoBot v{constants.VERSION}",
            description=f"I'm currently running version {constants.VERSION}",
            type="rich",
            url="https://github.com/TheresNoGit/TheresNoDiscordBot",
            color=constants.DEBUG_COL,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text=f"Codename: {constants.VERSION_NAME}")
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_any_role('mod', 'half mod')
    async def activity(self, ctx: Context, *, activity: str) -> None:
        "Change the bot activity (until restart). Usage: ~activity {new activity}"
        await self.bot.change_presence(activity=discord.Game(name=f"{activity}"))
        await ctx.send(f"Changed bot activity to {activity}")

    @commands.command()
    async def python(self, ctx: Context) -> None:
        "Ew"
        await ctx.send('Python would be *dangerous* if it was a **real** programming language.')

    @commands.command()
    async def php(self, ctx: Context) -> None:
        "Ew."
        await ctx.send("https://www.youtube.com/watch?v=6otW6OXjR8c&t=281")
