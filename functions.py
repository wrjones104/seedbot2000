import datetime
import sqlite3
import discord
import components.views as views
from core.database import save_buttons


async def gen_reroll_buttons(ctx, presets, flags, args, mtype):
    viewid = datetime.datetime.now().strftime("%d%m%y%H%M%S%f")
    viewids = [viewid, viewid]
    names = ["Reroll", "Reroll with Extras"]
    if presets:
        ids = [
            f"{viewid}_Reroll_{presets[0]}",
            f"{viewid}_Reroll with Extras_{presets[0]}",
        ]
    else:
        ids = [f"{viewid}_Reroll_{mtype}", f"{viewid}_Reroll with Extras_{mtype}"]
    flags = [flags, flags]
    mtypes = [mtype, mtype]
    if args:
        bargs = ["".join(args), "".join(args)]
    else:
        bargs = (None, None)
    if presets:
        ispreset = [True, True]
    else:
        ispreset = [False, False]
    names_and_ids = list(zip(viewids, names, ids, flags, bargs, ispreset, mtypes))
    await save_buttons(names_and_ids)
    view = views.ButtonView(names_and_ids)
    return view
