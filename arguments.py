

from argparse import ArgumentParser
from typing import Any, Iterable
import sys

class Arguments:
    def __init__(self, flags):
        import importlib
        self.groups = [
            "settings",
            "objectives",
            "starting_party", "characters", "swdtechs", "blitzes", "lores", "rages", "dances", "steal", "commands",
            "xpmpgp", "scaling", "bosses", "encounters", "boss_ai",
            "espers", "natural_magic",
            "starting_gold_items", "items", "shops", "chests",
            "graphics",
            "coliseum", "auction_house", "challenges", "bug_fixes", "misc",
        ]
        self.group_modules = {}
        for group in self.groups:
            self.group_modules[group] = importlib.import_module("WorldsCollide.args." + group)

        self.parser = ArgumentParser()
        flags = flags if isinstance(flags, list) else flags.split(' ')
        self.parser.add_argument("-i", dest = "input_file", required = True, help = "FFIII US v1.0 rom file")
        self.parser.add_argument("-o", dest = "output_file", required = False, help = "Modified FFIII US v1.0 rom file")
        self.parser.add_argument("-sid", dest = "seed_id", required = False, help = "Seed unique id (website)")
        self.parser.add_argument("-debug", dest = "debug", action = "store_true", help = "Debug mode")

        self.parser.add_argument("-nro", dest = "no_rom_output", action = "store_true", help = "Do not output a modified rom file")
        self.parser.add_argument("-slog", dest = "stdout_log", action = "store_true", help = "Write log to stdout instead of file")
        for group in self.group_modules.values():
            group.parse(self.parser)

        for meg in self.parser._mutually_exclusive_groups:
            latest_action = meg._group_actions[0]
            latest_idx = 0
            for action in meg._group_actions:
                for os in action.option_strings:
                    if os in flags:
                        rev = flags[-1::-1].index(os)
                        this_idx = len(flags) - 1 if rev == 0 else (len(flags) - rev - 1)
                        latest_action = latest_action if this_idx <= latest_idx else action
                        latest_idx = latest_idx if this_idx <= latest_idx else this_idx

            for action in [act for act in meg._group_actions if act != latest_action]:
                for os in action.option_strings:
                    # if any aliases are in the args string, remove it and all subsequent args
                    while os in flags:
                        idx = flags.index(os)
                        flags.pop(idx)
                        # remove excess args
                        while (len(flags) > idx and flags[idx][0] != '-'):
                            flags.pop(idx)

        self.flags = flags
        self.final_flags = ' '.join(flags)

if __name__ == "__main__":
    import os, sys

    # add Worlds Collide as an import context path
    sys.path.append(os.path.join(sys.path[0], 'WorldsCollide'))

    args = Arguments(sys.argv)
    print(args.flags)
