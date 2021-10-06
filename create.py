import requests
import random
from flags import chaos
from flags import true_chaos
from flags import rollseed
import urllib

def get_test():
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

def get_rollseed():
    flags = rollseed()
    flagstring = urllib.parse.quote(flags)
    wcurl = 'https://ff6wc.com/flags/' + flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data

#Print the results
#print(data)
#print('---')
#print(data["share_url"])