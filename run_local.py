import subprocess


async def local_wc(flags, beta, filename):
    if beta in ("dev", "new"):
        rolldir = 'WorldsCollide_dev/'
    elif beta == "doors":
        rolldir = 'WorldsCollide_Door_Rando/'
    else:
        rolldir = 'WorldsCollide/'
    args = (f"python3 wc.py -i ff3.smc -o seeds/" + filename + ".smc " + flags)
    try:
        subprocess.check_call(args, cwd=rolldir, shell=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise
