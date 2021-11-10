import requests
from flags import chaos
from flags import true_chaos
from flags import standard
from maths import get_cr
from custom_sprites_portraits import spraypaint
import urllib

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

def get_cr_seed():
    flags = get_cr()[0]
    flagstring = urllib.parse.quote(flags)
    wcurl = 'https://ff6wc.com/flags/' + flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data