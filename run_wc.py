import os
import subprocess


def local_wc(flags):
    home = os.getcwd()
    args = ("python3 wc.py -i ff3.smc -o seedbot.smc " + flags)
    os.chdir('../worldscollide')
    try:
        subprocess.check_call(args, shell=True)
        os.chdir(home)
    except subprocess.CalledProcessError:
        os.chdir(home)
        raise
