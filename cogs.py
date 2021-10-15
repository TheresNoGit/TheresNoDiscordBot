"""Cogs (categories of bot command)"""
import datetime
import random
from zoneinfo import ZoneInfo

import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context

import constants


class General(Cog, name="General"):  # type: ignore
    """General commands"""
    _COUNTDOWN_TZ = ZoneInfo("Europe/London")
    _COUNTDOWN_ARRIVAL = datetime.datetime(2021, 11, 9, 12,
                                           tzinfo=_COUNTDOWN_TZ)
    _COUNTDOWN_DISAGREEMENT_PREFACE = ("get into a fight with someone in the next seat about ")
    _COUNTDOWN_DISAGREEMENT_OPTIONS = [
        'whether that tune is "God Save the Queen" or "My Country, \'Tis of Thee"',
        "whether it's fries or crisps",
        "whether it's Shakespeare or Loadegunne",
        "whether it's William Shakespeare or Wouldiwas Shookespeared",
        "whether the Redcoats *let* the Revolutionaries win",
        "whether it's Union *Flag* or Union *Jack*",
        "the Irish Republican Army",
        "J. K. Rowling",
        "whether tea is a kind of soda",
        'the concept of "sweet tea"',
        "the French",
        "whether the UK would have won either world war without the U.S.",
        "Lady Diana Spencer",
        "monarchism",
        "whether it's baseball or cricket",
        "whether it's cricket or grasshopper"
    ]
    _COUNTDOWN_LINES = [
        "head off to retake the colonies",
        "forsake her beloved queen",
        'avoid the temptation to shout "bomb" in an airport',
        "spend eight hours in an aluminum tube six miles above the Atlantic Ocean",
        "try to get some Vyvanse past Customs",
        ("try to convince Customs that she *definitely* hasn't been "
         "lured here for organ harvesting"),
        "drunkenly try to convince the pilot to let her land the plane",
        "inevitably realize all the things she forgot as soon as she gets in the air",
        "realize she's actually been booked for New York, __Lincolnshire__,",
        "do the most exciting thing you can do in the United Kindgom: Leave...",
        "become the most insufferable tourist possible"
    ]
    _GENDERS = [
        "female", "male", "demigirl", "demiguy", "agender", "demigender",
        "genderfluid", "genderflux", "fluidflux", "xenogender", "cat",
        "dog", "NaN", "no thanks", "404 not found", "gayyyyy",
        "currently being discussed at Articles for deletion", "villain",
        "French", "ruled safe at third, but play currently under review"
    ]

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def countdown(self, ctx: Context) -> None:
        """How long till Sam visits Tamzin? Usage: ~countdown"""
        disagreement = (self._COUNTDOWN_DISAGREEMENT_PREFACE
                        + random.choice(self._COUNTDOWN_DISAGREEMENT_OPTIONS))
        weights = ([1] * len(self._COUNTDOWN_LINES)
                   + [len(self._COUNTDOWN_DISAGREEMENT_OPTIONS)])
        line = random.choices([*self._COUNTDOWN_LINES, disagreement],
                              weights)[0]
        time_till = (self._COUNTDOWN_ARRIVAL
                     - datetime.datetime.now().astimezone(self._COUNTDOWN_TZ))
        if time_till < datetime.timedelta():
            await ctx.send("She's already left, silly!")
            return
        if time_till > datetime.timedelta(days=14):
            time_message = f"in {time_till.days} days!"
        elif time_till > datetime.timedelta(hours=12):
            time_message = (
                ("in ***JUST*** "
                 if time_till < datetime.timedelta(days=7)
                 else "in")
                + (f"{time_till.days} days, "
                   if time_till > datetime.timedelta(days=1)
                   else "")
                + (f"{time_till.seconds // 3600} hours, "
                   f"{time_till.seconds // 60 % 60} minutes, and "
                   f"{time_till.seconds % 60} seconds!")
            )
        else:
            time_message = (
                "***LITERALLY FUCKING TODAY!*** ... "
                f"{time_till.seconds // 3600}:"
                f"{time_till.seconds // 60 % 60:02}:"
                f"{time_till.seconds % 60:02}")

        await ctx.send(f":airplane_departure: Sam will {line} "
                       f"{time_message} :airplane_arriving:")

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

    @commands.command(aliases=['gender'])
    async def whatsmygender(self, ctx: Context) -> None:
        """Because sometimes figuring out your own gender is too hard."""
        await ctx.send(
            f"Looks like your gender is {random.choice(self._GENDERS)}.\n"
            "Does that not sound right? It's possible that it's changed "
            "already! Feel free to ask again."
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

    async def notifyModsOfNewMember(self, member: Member) -> None:
        "Send a notification to the mod channel of a new member"
        if not constants.DEV:
            await self.bot.all_mod_channel.send(f"{member.mention} has just joined in <#{constants.WELCOME_CHANNEL}>")

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
