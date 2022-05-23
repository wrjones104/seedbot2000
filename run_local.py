import os
import subprocess


def local_wc(flags, beta):
    home = os.getcwd()
    args = ("python3 wc.py -i ../worldscollide/ff3.smc -o ../worldscollide/seedbot.smc " + flags)
    if beta:
        os.chdir('../worldscollide-beta')
    else:
        os.chdir('../worldscollide')
    try:
        subprocess.check_call(args, shell=True)
        os.chdir(home)
    except subprocess.CalledProcessError:
        os.chdir(home)
        raise


def local_jdm():
    home = os.getcwd()
    args = "python3 johnnydmad.py"
    os.chdir('../johnnydmad')
    try:
        subprocess.check_call(args, shell=True)
        os.chdir(home)
    except subprocess.CalledProcessError:
        os.chdir(home)
        raise


def local_jdc():
    home = os.getcwd()
    args = "python3 johnnydchaos.py"
    os.chdir('../johnnydmad')
    try:
        subprocess.check_call(args, shell=True)
        os.chdir(home)
    except subprocess.CalledProcessError:
        os.chdir(home)
        raise

def local_jdsilent():
    home = os.getcwd()
    args = "python3 johnnydsilent.py"
    os.chdir('../johnnydmad')
    try:
        subprocess.check_call(args, shell=True)
        os.chdir(home)
    except subprocess.CalledProcessError:
        os.chdir(home)
        raise