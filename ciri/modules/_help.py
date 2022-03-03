from .. import bot

cmds = ["Alive", "Autodp", "Eval", "Spotdl"]
from telethon import events, functions

from ..utils import ciri_cmd, eor


@bot.on(events.InlineQuery(pattern="help"))
async def help_menu(e):
    await eor(e, "Hi")


@ciri_cmd(pattern="dc")
async def _(e):
    if e.fwd_from:
        return
    result = await e.client(functions.help.GetNearestDcRequest())
    res = "**DC Lookup**\n**Current DC:** {}\n**Nearest DC:** {}\n**Country:** {}".format(result.this_dc, result.nearest_dc, result.country)
    await eor(e, res)