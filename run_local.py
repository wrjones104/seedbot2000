import subprocess
import os
import signal

async def local_wc(flags, beta, filename):
    args = ("python3 wc.py -i ../WorldsCollide/ff3.smc -o ../WorldsCollide/seeds/" + filename + ".smc " + flags)

    if beta in ("dev", "new"):
        rolldir = "WorldsCollide_dev/"
    elif beta == "practice":
        rolldir = 'WorldsCollide_practice/'
    elif beta == "doors":
        rolldir = 'WorldsCollide_Door_Rando/'
    elif beta == "lg1" or beta == "lg2":
        rolldir = 'WorldsCollide_location_gating1/'
    else:
        rolldir = "WorldsCollide/"
    try:
        localdata = subprocess.Popen(args, cwd=rolldir, shell=True, start_new_session=True, stdout=subprocess.PIPE)
        localdata.wait(timeout=10)
        out = localdata.communicate()
        print(f'out={out[0]}')
        return out[0]
    except subprocess.TimeoutExpired as e:
        os.killpg(os.getpgid(localdata.pid), signal.SIGTERM)
        raise e
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise e
