import subprocess
import functools
import typing
import asyncio


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


def local_wc(flags, beta):
    if beta in ("dev", "new"):
        rolldir = 'WorldsCollide_dev/'
    elif beta == "doors":
        rolldir = 'WorldsCollide_Door_Rando/'
    else:
        rolldir = 'WorldsCollide/'
    args = (f"python3 wc.py -i ff3.smc -o seedbot.smc " + flags)
    try:
        subprocess.check_call(args, cwd=rolldir, shell=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise


@to_thread
def local_jdm():
    args = "python3 johnnydmad.py"
    try:
        subprocess.check_call(args, cwd='johnnydmad/', shell=True)
    except subprocess.CalledProcessError:
        raise


@to_thread
def local_jdc():
    args = "python3 johnnydchaos.py"
    try:
        subprocess.check_call(args, cwd='johnnydmad/', shell=True)
    except subprocess.CalledProcessError:
        raise


@to_thread
def local_jdsilent():
    args = "python3 johnnydsilent.py"
    try:
        subprocess.check_call(args, cwd='johnnydmad/', shell=True)
    except subprocess.CalledProcessError:
        raise
