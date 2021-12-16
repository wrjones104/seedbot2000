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

    verbose = False  # set to True to say every step

    # Set which flags may be searched
    search_flags = list(fl.flag_list.keys())  # search all flags
    search_flags.remove('ktcr') # currently CR calc requires -kter, -ktcr, -stcr, -ster = TRUE
    search_flags.remove('kter') #
    search_flags.remove('stcr')  #
    search_flags.remove('ster')  #

    # Get initial seed for search
    i = get_cr(fl.rated())  # [flag_str, CR]
    if verbose:
        print('Starting CR: ', i[0])

    seed = fl.Flagstring2Seed(i[0])

    # Search loop
    while cr_timeout < 10000:
        # Select a flag to modify
        this_flag = random.choice(search_flags)

        # Select the modified value
        options = [k for k in fl.flag_list[this_flag]]
        if verbose:
            print(this_flag, options, seed[this_flag])
        if seed[this_flag] in options:
            options.remove(seed[this_flag]) # don't make no change
        else:
            print(type(options[0]), type(seed[this_flag]))
            #break
        new_value = random.choice(options)

        if verbose:
            print('Step ', cr_timeout, ': ', this_flag, seed[this_flag], ' --> ', new_value)

        # Calculate CR with the modification
        new_seed = fl.UpdateFlag(seed, this_flag, new_value)
        new_str = fl.Seed2Flagstring(new_seed)
        if verbose:
            print(new_str)
        i2 = get_cr(new_str)

        # Decide whether to take this step, based on whether it is closer to the desired value
        d1 = abs(int(c_rating[0]) - i[1])
        d2 = abs(int(c_rating[0]) - i2[1])

        # if they are equally distant, it should be a coinflip.
        metric = (d2 - d1)  # negative if d2 < d1; positive otherwise
        splitpoint = math.exp(metric) / (math.exp(metric) + 1)  # 0.5 if metric = 0; in range (0,1).

        if verbose:
            print('   CR: ', i[1], ' --> ', i2[1],'. Metric = ', metric,', split @ ', splitpoint)

        if random.random() > splitpoint:
            seed = new_seed
            i = i2
            smin = i[0]
            cmin = i[1]
            ymin = d2
        if ymin < 1:
            break
        cr_timeout += 1

        #if verbose:
        #    time.sleep(0.1)


    flags = smin
    fs = ''.join([flags, paint])
    flagstring = urllib.parse.quote(fs)
    wcurl = 'https://ff6wc.com/flags/' + flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data, cmin