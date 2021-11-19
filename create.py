import requests
from maths import get_cr
from maths import get_chaos_cr
import urllib


def generate_random_seed(stype, paint):
    flags = stype
    fs = ''.join([flags, paint])
    flagstring = urllib.parse.quote(fs)
    wcurl = 'https://ff6wc.com/flags/' + flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data


def generate_cr_seed(paint, c_rating):
    cr_timeout = 0
    ymin = 10000000
    smin = ""
    while cr_timeout < 20000:
        i = get_cr()
        iget = abs(int(c_rating[0]) - i[1])
        if iget < ymin:
            smin = i[0]
            cmin = i[1]
            ymin = iget
        if ymin < 1:
            break
        cr_timeout += 1
    flags = smin
    fs = ''.join([flags, paint])
    flagstring = urllib.parse.quote(fs)
    wcurl = 'https://ff6wc.com/flags/' + flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data, cmin


def generate_hard_chaos_seed(paint):
    cr_timeout = 0
    largo = 0
    largo_flags = ""
    while cr_timeout < 10000:
        i = get_chaos_cr()
        if i[1] > largo:
            largo = i[1]
            largo_flags = i[0]
        cr_timeout += 1
    flags = largo_flags
    fs = ''.join([flags, paint])
    flagstring = urllib.parse.quote(fs)
    wcurl = 'https://ff6wc.com/flags/' + flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data, largo
