import ctypes

import requests
from maths import get_cr
import flags as fl
import urllib
import random
import math
import numpy as np


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


def cr_search_v1(paint, c_rating):
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


def cr_search(paint, c_rating, fixed_flags, range_flags = ''):
    # Search for a seed with a particular challenge rating (c_rating).
    # Version 2 of searcher.  Make the search more powerful by:
    #   - at each step, calculate the CR if changed to every possibility (or at least 10, if there are many)
    #   - use the quantity abs(CR-goal) as the weight for selecting one of them, so closer seeds are more likely.
    #   - make flags that have been picked recently be less likely to be picked next time.
    #       - if flags have only two values and you are already on the best one, make it much less likely to be picked (?)
    #
    # V2a: This version also introduces the ability to require certain flag values in the search.
    # Include a partial flagstring as a second (optional) argument to require those values in the final flagstring.
    #   Example:  cr_search(175, '-as -ktcr 3 5' will find a flag with CR = 175, autosprint on, and KT character requirements 3-5.
    # NOTE: You can force a binary flag to be "off" by including the argument 'off' or 'false' after it.
    #   Example:  '-brl off', '-as off', '-nil false', '-nxppd false'
    # You can force a flag group to have the original value by including the argument 'off', 'original', or 'false':
    #   Example:  '-bb original'  forces original boss battles
    #             '-loremp original' forces original lore mp values
    #             '-ascale original' forces original boss ability scaling.
    #             '-ebonus original' forces original esper bonuses.
    # Groups are listed in flag_groups.keys().
    #
    # V2b: This version introduces the ability to alter the range of flags in the search.
    # Include a partial flagstring as a third (optional) argument to change the range of the search.
    #   Example:  cr_search(175, '', '-xpm 1 15 -ktcr 1 5 10 15' will allow the search to look only within the ranges
    #       xp multiplier = [1, 15], kt character requirement lower bound [1, 5], and upper bound [10, 15].
    # This will only work with numerically defined values:
    #   ktcr, kter, ktdr, stcr, ster, stdr, slr, lmprp, lmprv, srr, sdr, csrp, rec1, rec2, rec3, rec4, rec5, xpm, gpm,
    #   mpm, lsp, lsa, lsh, lst, hmp, hma, hmh, hmt, xgp, xga, xgh, xgt, asr, ase, msl, eel, rer, fer, escr, esr, ebr,
    #   emprp, emprv, eer, eebr, gp, smc, sws, sfd, sto, ier, iebr, ieor, iesr, ierr, ierbr, ieror, iersr, csb, sisr,
    #   sprv, sprp, sdm, ccsr, crvr

    ### CONTROLS ###-
    cr_timeout = 10000       # Maximum number of loops
    max_options = 100        # maximum number of options to assess on each loop
    it_scalar = [0.5, 0.05]  # [light, heavy] weight penalty for re-assessing a flag
    verbose = False          # set to True to say every step

    # Get initial seed for search
    i = get_cr(fl.rated())  # [flag_str, CR]
    seed = fl.Flagstring2Seed(i[0])

    # Grab the default list of flags and ranges
    range_list = {}
    for f in fl.flag_list.keys():
        range_list[f] = fl.flag_list[f]

    # Set which flags may be searched
    search_flags = [k for k in range_list.keys()]  # search all flags
    search_flags.remove('ktcr')  # currently CR calc requires -kter, -ktcr, -stcr, -ster
    search_flags.remove('kter')  #
    search_flags.remove('stcr')  #
    search_flags.remove('ster')  #

    # Parse range_flags
    if range_flags[-1] != ' ':
        range_flags += ' '

    if len(range_flags) > 0:
        # We need a new parser for this.
        while range_flags.find('-') >= 0:
            # Split out flag
            temp = range_flags[range_flags.find('-'):].split(' ',1) # get flag
            this_flag = temp[0][range_flags.find('-')+1:]
            range_flags = temp[1]
            if verbose:
                print(this_flag, ': ', range_flags)
            # Figure out how many numbers there should be
            if this_flag in range_list.keys():
                if range_list[this_flag] == [True, False]:
                    # This is a binary flag.  Look for subflags.
                    k = 0
                    while this_flag + '_' + str(k+1) in range_list.keys():
                        k += 1
                        [temp2a, temp2b, range_flags] = range_flags.split(' ', 2)
                        range_list[this_flag+'_'+str(k)] = [j for j in range_list[this_flag+'_'+str(k)] if float(j) >= float(temp2a) and float(j) <= float(temp2b)]
                        if verbose:
                            print('[',float(temp2a),', ',float(temp2b),']: ', fl.flag_list[this_flag+'_'+str(k)], '-->', range_list[this_flag+'_'+str(k)])
                else:
                    # Not a binary flag. Just adjust the ranges.  Non-binary flags can only have one value.
                    [temp2a, temp2b, range_flags] = range_flags.split(' ', 2)
                    range_list[this_flag] = [j for j in range_list[this_flag] if float(j) >= float(temp2a) and float(j) <= float(temp2b)]
                    if verbose:
                        print(fl.flag_list[this_flag], '-->', range_list[this_flag])

        # Make sure that all starting values are in the new ranges
        for f in seed.keys():
            if seed[f] not in range_list[f]:
                seed[f] = random.choices(range_list[f])[0]

        #for f in range_list.keys():
        #    if len(range_list[f]) > 10:
        #        print(f,': ', range_list[f][:10])
        #    else:
        #        print(f,': ', range_list[f])


    # Parse fixed_flags (fixed should take precedence over ranges)
    if len(fixed_flags) > 0:
        seedlet = fl.Flagstring2Seedlet(fixed_flags)

        for f in seedlet.keys():
            # Update the starting seed appropriately
            seed[f] = seedlet[f]

            # remove keys from search_flags
            if f in fl.flag_group_lookup.keys():
                # If f is in a flag group, remove the group from randomization
                search_flags.remove(fl.flag_group_lookup[f])
            else:
                # Remove the flag from randomization
                if f in search_flags:
                    search_flags.remove(f)


    # Initialize flag weighting for the search
    weight_flags = [1 for i in range(len(search_flags))]  # start with equal weight on all flags

    if verbose:
        print('Starting CR:  ', i[0])

    # Search loop
    counter = 0
    ymin = 10000000
    smin = ""
    while counter < cr_timeout:
        # Select a flag to modify
        this_flag = random.choices(search_flags, weight_flags)[0]

        # Get acceptable values
        options = [k for k in fl.flag_list[this_flag]]
        if verbose:
            print(' ')
            print('Selected flag: ', this_flag, '. Available options: ', options, '. Current value: ', seed[this_flag])
        if seed[this_flag] in options:
            options.remove(seed[this_flag])  # don't make no change
        else:
            # troubleshoot
            print('There was an error!')
            print('Selected flag: ', this_flag, '. Available options: ', options, '. Current value: ', seed[this_flag])
            print(type(options[0]), type(seed[this_flag]))
            break

        # If there are more than the maximum number of options, limit how many are used
        if len(options) > max_options:
            options = random.sample(options, max_options)

        # Calculate the CR for each value
        op_CR = []  # previously: new_value = random.choice(options)
        for op in options:
            temp_seed = fl.CopySeed(seed)
            fl.UpdateFlag(temp_seed, this_flag, op)
            temp = get_cr(fl.Seed2Flagstring(temp_seed))
            op_CR.append(temp[1])
        options.append(seed[this_flag])  # value if no change
        op_CR.append(i[1])  # for calculating weights

        # Calculate the weight for each option based on CR
        c_rating_int = int(c_rating[0])
        dist = [abs(CR - c_rating_int) for CR in op_CR]
        sigma = np.max([0.75, np.std(dist)])  # width of gaussian - should this depend on something?
        target = np.min(dist)
        op_weight = np.exp([-((d - target) / sigma) ** 2 for d in dist])

        # Select a value using this weighting
        new_value = random.choices(options, op_weight)[0]

        if verbose:
            # print('Step ', counter, ': ', this_flag, ' current value = ', seed[this_flag])
            for jjj in range(len(op_weight)):
                print('     ', options[jjj], ': d=', round(dist[jjj], 3), ', CR = ', round(op_CR[jjj], 2), ', weight =',
                      round(op_weight[jjj], 5))
            # print('     selected: ', new_value)

        if new_value != seed[this_flag]:
            # Calculate CR with the modification
            new_seed = fl.UpdateFlag(seed, this_flag, new_value)
            new_str = fl.Seed2Flagstring(new_seed)
            if verbose:
                print(new_str)
            i2 = get_cr(new_str)

            # Update the best seed
            seed = new_seed
            i = i2
            smin = i[0]
            cmin = i[1]
            ymin = abs(i[1] - c_rating_int)
        if ymin < 1:
            break

        # If this is a binary flag and we are already at the value with smallest difference, discount heavily; otherwise, discount normally
        this_flag_ind = search_flags.index(this_flag)
        this_weight = weight_flags[search_flags.index(this_flag)]
        if fl.flag_list[this_flag] == [True, False] and ymin == np.min(dist):
            # Harsh adjustment
            weight_flags[this_flag_ind] = this_weight * it_scalar[1]

        else:
            # Standard adjustment
            weight_flags[this_flag_ind] = this_weight * it_scalar[0]

        if verbose:
            print('Flag ', this_flag, ' weight changed: ', this_weight, '-->', weight_flags[this_flag_ind])

        # Iterate the loop
        counter += 1

        # if verbose:
        #    time.sleep(0.1)

    flags = smin
    fs = ''.join([flags, paint])
    flagstring = urllib.parse.quote(fs)
    wcurl = 'https://ff6wc.com/flags/' + flagstring
    r = requests.get(wcurl)
    data = r.json()
    return data, cmin