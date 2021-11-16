import requests
from flags import chaos
from flags import true_chaos
from flags import standard
from maths import get_cr
from maths import get_chaos_cr
from custom_sprites_portraits import spraypaint
import urllib


def generate_random_seed(stype, paint):
    flags = stype
    rp = paint
    fs = ''.join([flags, rp])
    flagstring = urllib.parse.quote(fs)
    wcurl = 'https://ff6wc.com/flags/' + flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data


def generate_cr_seed(paint, c_rating):
    rp = paint
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
    fs = ''.join([flags, rp])
    flagstring = urllib.parse.quote(fs)
    wcurl = 'https://ff6wc.com/flags/' + flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data, cmin


def get_test():
    chaos_flags = chaos()
    flagstring = urllib.parse.quote(chaos_flags)
    wcurl = 'https://ff6wc.com/flags/'+flagstring
    return wcurl


def get_standard_test():
    standard_flags = standard()
    flagstring = urllib.parse.quote(standard_flags)
    wcurl = 'https://ff6wc.com/flags/'+flagstring
    return wcurl


def get_chaos_test():
    chaos_flags = chaos()
    flagstring = urllib.parse.quote(chaos_flags)
    wcurl = 'https://ff6wc.com/flags/'+flagstring
    return wcurl


def get_chaos():
    chaos_flags = chaos()
    flagstring = urllib.parse.quote(chaos_flags)
    wcurl = 'https://ff6wc.com/flags/'+flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data


def get_truechaos():
    chaos_flags = true_chaos()
    flagstring = urllib.parse.quote(chaos_flags)
    wcurl = 'https://ff6wc.com/flags/'+flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data


def get_standard():
    flags = standard()
    flagstring = urllib.parse.quote(flags)
    wcurl = 'https://ff6wc.com/flags/' + flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data


def get_chaos_paint():
    chaos_flags = chaos()
    flagstring = urllib.parse.quote(chaos_flags)
    wcurl = 'https://ff6wc.com/flags/'+flagstring+spraypaint()
    r = requests.get(wcurl)
    data = r.json()
    return data


def get_truechaos_paint():
    chaos_flags = true_chaos()
    flagstring = urllib.parse.quote(chaos_flags)
    wcurl = 'https://ff6wc.com/flags/'+flagstring+spraypaint()
    r = requests.get(wcurl)
    data = r.json()
    return data


def get_standard_paint():
    flags = standard()
    flagstring = urllib.parse.quote(flags)
    wcurl = 'https://ff6wc.com/flags/' + flagstring+spraypaint()
    r = requests.get(wcurl)
    data = r.json()
    return data


def get_cr_seed(arg):
    cr_timeout = 0
    ymin = 10000000
    smin = ""
    while cr_timeout < 10000:
        i = get_cr()
        iget = abs(arg - i[1])
        if iget < ymin:
            smin = i[0]
            cmin = i[1]
            ymin = iget
            iteration = cr_timeout
        if ymin < 1:
            break
        cr_timeout += 1
    flags = smin
    flagstring = urllib.parse.quote(flags)
    wcurl = 'https://ff6wc.com/flags/' + flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data, cmin, iteration


def get_cr_chaos_seed():
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
    flagstring = urllib.parse.quote(flags)
    wcurl = 'https://ff6wc.com/flags/' + flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data, largo, largo_flags