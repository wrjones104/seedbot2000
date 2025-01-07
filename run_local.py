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
    elif beta == "doors":
        rolldir = 'WorldsCollide_Door_Rando/'
        args = ("python3 wc.py -i ../WorldsCollide/ff3.smc -o ../WorldsCollide/seeds/" + filename + ".smc " + flags)
    elif beta == "lg1" or beta == "lg2":
        rolldir = 'WorldsCollide_location_gating1/'
        args = ("python3 wc.py -i ../WorldsCollide/ff3.smc -o ../WorldsCollide/seeds/" + filename + ".smc " + flags)
    else:
        rolldir = "WorldsCollide/"
        args = "python3 wc.py -i ff3.smc -o seeds/" + filename + ".smc " + flags
    try:
        localdata = subprocess.Popen(args, cwd=rolldir, start_new_session=True, stdout=subprocess.PIPE)
        localdata.wait(timeout=10)
        out = localdata.communicate()
        return out
    except subprocess.TimeoutExpired as e:
        localdata.terminate()
        raise e
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise e
