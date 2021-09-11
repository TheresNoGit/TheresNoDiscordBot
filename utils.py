"""Helper functions for the commands.

Functions/classes here should return text to be sent, rather than
sending directly, unless they handle Discord exceptions.
"""
import io

from discord import File, HTTPException
from discord.ext.commands import Context


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
