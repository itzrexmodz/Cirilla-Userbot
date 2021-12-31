import glob
import importlib
import logging
import sys
from pathlib import Path

from telethon import events

from ciri import CMD_HANDLERS, FULL_SUDO, OWNER_ID, SUDO, ub


def ciri_cmd(**args):
    args["pattern"] = "^[" + CMD_HANDLERS + "](?i)" + args["pattern"]
    if args.get("allow_sudo"):
        FROM_USERS = SUDO
        FROM_USERS.append(OWNER_ID)
        args["from_users"] = FROM_USERS
        del args["allow_sudo"]
    elif args.get("full_sudo"):
        FROM_USERS = FULL_SUDO
        FROM_USERS.append(OWNER_ID)
        args["from_users"] = FROM_USERS
        del args["full_sudo"]
    else:
        args["from_users"] = OWNER_ID

    def decorator(func):
        async def wrapper(ev):
            try:
                await func(ev)
            except Exception as exception:
                logging.info(exception)

        ub.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator

async def eor(e, msg, parse_mode="md", link_preview=False):
 if e.sender_id == OWNER_ID:
    await e.edit(msg, parse_mode=parse_mode, link_preview=link_preview)
 else:
    await e.reply(msg, parse_mode=parse_mode, link_preview=link_preview)

def load_modules():
    print("Loading Modules...")
    for x in glob.glob("ciri/modules/*.py"):
        with open(x) as f:
            name = Path(f.name).stem.replace(".py", "")
            spec = importlib.util.spec_from_file_location(
                "ciri.modules.{}".format(name), Path("ciri/modules/{}.py".format(name))
            )
            mod = importlib.util.module_from_spec(spec)
            mod.bot = ub
            spec.loader.exec_module(mod)
            sys.modules["ciri.modules." + name] = mod
            print("sucessfully imported " + name)
    print("Sucessfully Loaded All Modules.")
