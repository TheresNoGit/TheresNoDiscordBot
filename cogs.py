"""Cogs (categories of bot command)"""
import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context, MemberConverter

import constants


class Mod(Cog, name="Moderation"):  # type: ignore
    """Mod-only commands"""
    @commands.command()
    @commands.has_any_role('based mod', 'helpful mod')
    async def trust(self, ctx: Context, user_name: str) -> None:
        "Sets a user as trusted. Usage: !trust {username}"
        user = await MemberConverter().convert(ctx, str(user_name))
        trusted_role = discord.utils.get(user.guild.roles, name="trusted")
        await user.add_roles(trusted_role)
        await ctx.send(f"Setting <@{user.id}> as trusted")

    @commands.command()
    @commands.has_any_role('based mod', 'helpful mod')
    async def spite(self, ctx: Context, user_name: str) -> None:
        "Spite a user. Usage: !spite {username}"
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
