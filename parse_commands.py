import flags
import functions


async def parse_command(message):
    command = message.content.lstrip("!")
    print(command)
    roll_commands = {
        "jones_special": flags.flag_presets["jones_special"], "jones": flags.flag_presets["jones_special"],
        "chaos": flags.v1_chaos(), "true": flags.v1_true_chaos(), "rando": "next", "randomseed": "next",
        "true_chaos": flags.v1_true_chaos(), "standard": flags.v1_standard(),
        "rollseed": command.split()[1:]
    }
    try:
        if command.split()[0] in roll_commands.keys():
            rc = roll_commands[command.split()[0]]
            print(rc)
            if rc == "next":
                rc = roll_commands[command.split()[1]]
                print(f"rc: {rc}")
        else:
            rc = roll_commands["standard"]
            print(f"rc: {rc}")
    except (IndexError, KeyError):
        rc = roll_commands["standard"]
        print(f"rc: {rc}")
    if command.split()[0] == "rollseed":
        await functions.rollseed(message, rc)
    else:
        await functions.make_seed(message, rc)

