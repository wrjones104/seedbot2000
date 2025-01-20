import subprocess
import os
import signal

class RollException(Exception):
    def __init__(self, msg, filename, sperror):
        self.msg=msg
        self.sperror=sperror
        self.filename=filename

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
    elif beta == "ws":
        rolldir = "WorldsCollide_shuffle_by_world/"
    else:
        rolldir = "WorldsCollide/"
    try:
        localdata = subprocess.Popen(args, cwd=rolldir, shell=True, start_new_session=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        localdata.wait(timeout=10)
        out = localdata.communicate()
        if out[1]:
            raise RollException("There was an issue with this subprocess", filename, out[1].decode("utf-8"))
        else:
            return out[0]
    except subprocess.TimeoutExpired as e:
        os.killpg(os.getpgid(localdata.pid), signal.SIGTERM)
        raise e
    except Exception as e:
        raise e
