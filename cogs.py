"""Cogs (categories of bot command)"""
from discord import Member
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context

import constants
import utils


class General(Cog, name="General"):  # type: ignore
    """General commands"""
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def trustme(self, ctx: Context) -> None:
        """Nudges the mods to give you the `trusted` role. Usage: ~trustme"""
        await self.bot.mod_channel.send(
            f"{self.bot.mod_pings}: {ctx.message.author.mention} wants the "
            f"*trusted* role in {ctx.message.channel.mention} – hopp hopp!"
        )

    @commands.command(aliases=['mods'])
    async def mod(self, ctx: Context, *, reason: str) -> None:
        """Requests mod attention for a given reason. Usage: ~mod {reason}"""
        await self.bot.mod_channel.send(
            f"{self.bot.mod_pings}: {ctx.message.author.mention} requests mod "
            f"attention in {ctx.channel.mention}. Reason: {reason}"
        )

    @commands.command()
    async def urgent(self, ctx: Context, *, reason: str) -> None:
        """Requests URGENT mod attention for a given reason. Usage: ~urgent {reason}"""
        await self.mod(ctx, reason=reason)
        utils.send_email(
            subject=f"Urgent mod request from {ctx.message.author.name}",
            text=(f"{ctx.message.author.name} requests urgent mod attention in"
                  f" {ctx.message.channel.name}. Reason: {reason}")
        )


class Mod(Cog, name="Moderation"):  # type: ignore
    """Mod-only commands"""
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.has_any_role('based mod', 'helpful mod')
    async def trust(self, ctx: Context, *, member: Member) -> None:
        "Sets a user as trusted. Usage: ~trust {username}"
        await member.add_roles(self.bot.guild.get_role(885647339207946280))
        await ctx.send(f"Setting {member.mention} as trusted")

    @commands.command()
    @commands.has_any_role('based mod', 'helpful mod')
    async def spite(self, ctx: Context, *, member: Member) -> None:
        "Spite a user. Usage: ~spite {username}"
        await ctx.send(f"Consider yourself spited, {member.mention}")


class BotInternal(Cog, name="Bot Internal", command_attrs={'hidden': True}):  # type: ignore
    """Commands that relate to the bot itself."""
    @commands.command()
    async def version(self, ctx: Context) -> None:
        "Gets the bots current version number"
        await ctx.send(f"I'm currently running version {constants.VERSION}")

    @commands.command()
    async def python(self, ctx: Context) -> None:
        "Ew"
        await ctx.send('Python would be *dangerous* if it was a **real** programming language.')

    @commands.command()
    async def php(self, ctx: Context) -> None:
        "Ew."
        await ctx.send("https://www.youtube.com/watch?v=6otW6OXjR8c&t=281")
