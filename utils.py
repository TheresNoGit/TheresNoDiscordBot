"""Helper functions for the commands.

Functions/classes here should return text to be sent, rather than
sending directly, unless they handle Discord exceptions.
"""
import io
from typing import Optional, Set, Tuple, Union
import time
import datetime

from discord import File, HTTPException, Message, Embed
from discord.ext.commands import Context

import constants

# Uses typing.Tuple rather than tuple due to <https://github.com/python/mypy/issues/9980>.
AliasDictData = dict[Union[str, Tuple[str, ...]], str]


class AliasDict(dict[str, str]):
    """Create dicts for values that take many aliases (keys).

    When setting a new item, implicitly sets {value: value} as well.
    Will raise a ValueError if the value is already a key.

    Attributes:
      All inherited from `dict`.
    """

    _error_message = "AliasDict values and keys must not overlap."

    def __init__(self,
                 aliases: AliasDictData,
                 value_isnt_alias: Optional[AliasDictData] = None,
                 unaliased: Optional[Set[str]] = None) -> None:
        """Constructs an AliasDict with no uninherited attributes.

        Args:
          aliases:  An AliasDictData of keys and values.  Keys can be
            either strs or tuples thereof.  If a tuple, AliasDict will
            convert this into each member of that tuple having the
            relevant value.  (The tuple itself will not be preserved as
            a key.)  For each value, a {value: value} mapping will also
            be added to the dict.
          value_isnt_alias:  An AliasDictData that is treated the same
            as `aliases`, except that values do not become
            {value: value} mappings.
          unaliased:  A set of strs that will be turned into
            {set item: set item} mappings.

        Raises:
          ValueError if the values and keys overlaps.
        """
        value_isnt_alias = (value_isnt_alias if value_isnt_alias is not None
                            else {})
        unaliased = unaliased if unaliased is not None else set()
        if aliases.keys() & aliases.values() or aliases.keys() & unaliased:
            raise ValueError(self._error_message)
        data = {v: v for v in set(aliases.values()) | unaliased}
        for k, v in aliases.items() | value_isnt_alias.items():
            if isinstance(k, tuple):
                for i in k:
                    data[i] = v
            else:
                data[k] = v
        super().__init__(data)
        # Just here for __repr__ purposes.  Not used otherwise.
        self._aliases = aliases
        self._value_isnt_alias = value_isnt_alias
        self._unaliased = unaliased

    def __repr__(self) -> str:
        return (f"AliasDict({self._aliases!r}, "
                f"value_isnt_alias={self._value_isnt_alias!r}, "
                f"unaliased={self._unaliased!r})")

    def __str__(self) -> str:
        # It makes sense if you (don't) think about it.  -- THK
        return super().__repr__()

    def __setitem__(self, key: str, value: str) -> None:
        if value in self.keys():
            raise ValueError(self._error_message)
        super().__setitem__(key, value)
        super().__setitem__(value, value)


async def safesend(ctx: Context,
                   safe: str,
                   dangerous: str,
                   filename: str,
                   is_json: bool = True) -> None:
    """Send a message that could exceed 2,000 characters.

    Use this on any command that:
      1. Sends variable-length text (e.g. JSON) *or*
      2. Can be called an arbitrary number of times in a single message
         (e.g. `?sock`).

    It will first attempt to send `safe` and `dangerous` together, and,
    if  that results in an HTTPException, will instead send `safe` (if
    non-empty) as message and `unsafe` as a file.

    Will place a newline between `safe` and `dangerous` and will
    automatically format any JSON for display in the message as a code
    block.

    Args:
      ctx:  A Context to send to.
      safe:  A portion of the message that is guaranteed to (or is
        extremely unlikely to) exceed 2,000 characters.  This will be
        sent either way.  Can be empty.
      dangerous:  A portion of the message that will be turned into a
        file if the first attempt to send it fails.
      filename:  A name to assign the file constructed from `unsafe`.
      is_json:  If True, `unsafe` will be formatted in a JSON code block
        in the first attempt at sending; if sent as a file it will be a
        .json file rather than the default .txt.
    """
    safe = safe + "\n"
    fenced = f"```json\n{dangerous}```" if is_json else dangerous
    try:
        await ctx.send(safe + fenced)
    except HTTPException:
        file_ext = 'json' if is_json else 'txt'
        file = File(io.BytesIO(dangerous.encode('utf-8')),
                    filename=f"{filename}.{file_ext}")
        await ctx.send(safe
                       + ("[Rest of o" if safe else "[O")
                       + "utput too long to send as message. Sorry.]",
                       file=file)


async def isDM(message: Message) -> bool:
    """Helper function to see if this message was a DM"""
    return not message.guild


async def isEmbed(message: Message) -> bool:
    """Helper function to see if this message was an Embed"""
    return bool(message.embeds)


async def getUTC() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


async def sendLoggerMessage(ctx: Context, content: str, error: bool) -> None:
    """Helper function to send a DEBUG or ERROR message to the bot commands channel"""
    # Only send if Dev = False
    if not constants.DEV:
        now_utc = await getUTC()
        if error:
            embed = Embed(
                title="[ERROR MESSAGE]",
                description=f"{content}",
                type="rich",
                color=constants.ERROR_COL,
                timestamp=datetime.datetime.utcnow()
            )
        else:
            embed = Embed(
                title="[DEBUG MESSAGE]",
                description=f"{content}",
                type="rich",
                color=constants.DEBUG_COL,
                timestamp=datetime.datetime.utcnow()
            )
        
        await ctx.commands_channel.send(embed=embed)
