import requests
from maths import get_cr
import flags as fl
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
        i = get_cr(fl.rated())
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
        i = get_cr(fl.chaos())
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


def generate_easy_chaos_seed(paint):
    cr_timeout = 0
    largo = 1000
    largo_flags = ""
    while cr_timeout < 10000:
        i = get_cr(fl.chaos())
        if i[1] < largo:
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


def cr_search(paint, c_rating):
    cr_timeout = 0
    ymin = 10000000
    smin = ""

    # Get initial seed for search
    i = get_cr(fl.rated())  # [flag_str, CR]

    # Search loop
    while cr_timeout < 20000:
        # Select a flag to modify
        this_flag = random.choice(fl.flag_list.keys())

        # Select the modified value
        new_value = random.choice(fl.flag_list[this_flag])

        # Calculate CR with the modification
        new_seed = fl.UpdateFlag(fl.Flagstring2Seed(i[0]), this_flag, new_value)
        i2 = get_cr(fl.Seed2Flagstring[new_seed])

        # Decide whether to take this step, based on whether it is closer to the desired value
        d1 = abs(int(c_rating[0]) - i[1])
        d2 = abs(int(c_rating[0]) - i2[1])

        # if they are equally distant, it should be a coinflip.
        metric = (d2 - d1)  # negative if d2 < d1; positive otherwise
        splitpoint = math.exp(metric)/(math.exp(metric)+1)  # 0.5 if metric = 0; in range (0,1).

        if random.random() > splitpoint:
            i = i2
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