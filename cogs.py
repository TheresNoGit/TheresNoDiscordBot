"""Cogs (categories of bot command)"""
from typing import Tuple
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context, MemberConverter

import constants
import utils


class General(Cog, name="General"):  # type: ignore
    """General commands"""
    @commands.command()
    async def trustme(self, ctx: Context) -> None:
        "Nudges the mods to give you the `trusted` role. Usage: ~trustme"
        channel = Bot.get_channel(ctx.bot, int(ctx.message.channel.id))
        mod_channel = Bot.get_channel(ctx.bot, int(constants.MOD_CHANNEL))
        await mod_channel.send(f"<@{int(constants.BASED_MOD)}> & <@{int(constants.HELPFUL_MOD)}> : <@{ctx.message.author.id}> wants the trusted role in {channel.name} - hopp hopp!")

    @commands.command()
    async def mod(self, ctx: Context, reason: str) -> None:
        "Requests mod attention for a given reason. Usage: ~mod {reason}"
        channel = Bot.get_channel(ctx.bot, int(ctx.message.channel.id))
        mod_channel = Bot.get_channel(ctx.bot, int(constants.MOD_CHANNEL))
        await mod_channel.send(f"<@{int(constants.BASED_MOD)}> & <@{int(constants.HELPFUL_MOD)}> : <@{ctx.message.author.id}> requests mod attention in {channel.name}. Reason: {reason}")

    @commands.command()
    async def urgent(self, ctx: Context, reason: str) -> None:
        "Requests URGENT mod attention for a given reason. Usage: ~urgent {reason}"
        channel = Bot.get_channel(ctx.bot, int(ctx.message.channel.id))
        mod_channel = Bot.get_channel(ctx.bot, int(constants.MOD_CHANNEL))
        await utils.send_email(constants.EMAIL_FROM, [ constants.EMAIL_TO ], f"Urgent mod request from {ctx.message.author.name}", f"{ctx.message.author.name} requests urgent mod attention in {channel.name}. Reason: {reason}")
        #await mod_channel.send(f"<@{int(constants.BASED_MOD)}> & <@{int(constants.HELPFUL_MOD)}> : <@{ctx.message.author.id}> requests urgent mod attention in {channel}. Reason: {reason}")


class Mod(Cog, name="Moderation"):  # type: ignore
    """Mod-only commands"""
    @commands.command()
    @commands.has_any_role('based mod', 'helpful mod')
    async def trust(self, ctx: Context, user_name: str) -> None:
        "Sets a user as trusted. Usage: ~trust {username}"
        user = await MemberConverter().convert(ctx, str(user_name))
        trusted_role = discord.utils.get(user.guild.roles, name="trusted")
        await user.add_roles(trusted_role)
        await ctx.send(f"Setting <@{user.id}> as trusted")

    @commands.command()
    @commands.has_any_role('based mod', 'helpful mod')
    async def spite(self, ctx: Context, user_name: str) -> None:
        "Spite a user. Usage: ~spite {username}"
        user = await MemberConverter().convert(ctx, str(user_name))
        await ctx.send(f"Consider yourself spited, <@{user.id}>")


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
