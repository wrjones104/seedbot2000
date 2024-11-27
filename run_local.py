import subprocess


async def local_wc(flags, beta, filename):
    if beta in ("dev", "new"):
        rolldir = "WorldsCollide_dev/"
        args = (
            "python3 wc.py -i ../WorldsCollide/ff3.smc -o ../WorldsCollide/seeds/"
            + filename
            + ".smc "
            + flags
        )
    elif beta == "practice":
        rolldir = 'WorldsCollide_practice/'
        args = ("python3 wc.py -i ../WorldsCollide/ff3.smc -o ../WorldsCollide/seeds/" + filename + ".smc " + flags)
    # elif beta == "doors":
    #     rolldir = 'WorldsCollide_Door_Rando/'
    #     args = (f"python3 wc.py -i ../WorldsCollide/ff3.smc -o ../WorldsCollide/seeds/" + filename + ".smc " + flags)
    else:
        rolldir = "WorldsCollide/"
        args = "python3 wc.py -i ff3.smc -o seeds/" + filename + ".smc " + flags
    try:
        localdata = subprocess.check_output(args, cwd=rolldir, shell=True)#.decode(encoding="utf-8").split("Hash")[1].lstrip()
        print(localdata.decode(encoding="utf-8").split("Seed")[1].split("\n")[0].lstrip())
        return localdata
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise
