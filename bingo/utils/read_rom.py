# from common.constants import *
# from common.monster import Monster
# from common.battlegroup import Battlegroup
# import copy


# Dullahan at TunnelArmr
# In vanilla TA data is mentioned at 517829
# In WC TA data is mentioned at 421739

# TA Battle Formation is 436?
# DL Battle Formation is 252?
# Battle Data starts at 0xF6200 - Size is 15 bytes

def format_hex(bstring: bytes, line_length: int) -> str:
    """Converts a byte string to space-delimted two-character hex values with line breaks at an interval
       of ``line_length``. As an example \x80\x81\x82\x83 with ``line_length`` of 2 would yield:

       80 81
       82 83

    Parameters
    ----------
    bstring : bytes
        The byte string to be formatted. Can be int if it is only one character.
    line_length : int
        The number 2-digit hex values per line in the output

    Returns
    -------
    str
        A formatted string representation of the input bytes
    """
    error = ""
    if not isinstance(bstring, (bytes, int)):
        error += "Input bstring must be bytes or int. Found type %s\n" % (type(bstring))
    elif isinstance(bstring, int) and not 0 <= bstring <= 255:
        error += "If input bstring is int, it must be between 0 and 255 inclusive. Found value %s\n" % (bstring)

    if error != "":
        raise Exception(error)

    output = ['']
    counter = 0
    if isinstance(bstring, int):
        bstring = bstring.to_bytes(1, 'little')
    for b in bstring:
        h = str(hex(b))[2:]
        if len(h) < 2:
            h = "0" + h
        output.append(h)
        counter += 1
        if counter % line_length == 0:
            output.append("\n")
            counter = 0

    return (' ').join(output).strip().replace(' \n ', '\n')


filenamef = "../roms/FinalFantasy3e.smc"
filenamew = "../roms/wc.smc"
filenamex = "../roms/wc2.smc"
filenamee = "../roms/edited.smc"
with open(filenamef, 'rb') as f:
    fdata = f.read()

with open(filenamew, 'rb') as f:
    wdata = f.read()

# with open(filenamee, 'rb') as f:
#    edata = f.read()

with open(filenamex, 'rb') as f:
    xdata = f.read()

mode = 0x0
if filenamef == "FinalFantasy3e.smc":
    mode = 0x200

print(len(fdata) % 0x400)

p = 0xFFC0 + 0x200
p = 0x200 + 0xFF00

fhx = format_hex(fdata[p: p + 8], 40)
whx = format_hex(wdata[:0x200], 40)

print(fhx)
# print (hashlib.md5(fdata[:0x200]).hexdigest())
exit()

# Remove header
fdata = fdata[0x200:]
edata = edata[0x200:]

# 3c0f is in a spot in F0000 + offsets in WC TunnelArmr spot where it is 14 05 in FF6 spot 9-10
# 9006 is in a spot in F0000 + offsets in WC TunnelArmr spot where it is 00 00 in FF6 spot 13-14
# TA at CA/769C? MAP
# Dull at CA/435D? MAP
# Map events 40342 vanilla

# ghosttrain
enemy_id = 262
enemy_id = 358
tunnelarmr = 260
dullahan = 284
tunnel_loc = 73

size_data = 0x20
size_name = 10
size_loca = 33

name_location = 0xFC050
data_location = 0xF0000
loca_location = 0x2D8F00

wtdatat = data_location + (tunnelarmr * size_data)
ftdatat = data_location + (tunnelarmr * size_data) + 0x200

wtdatad = data_location + (dullahan * size_data)
ftdatad = data_location + (dullahan * size_data) + 0x200

wtdatat = i2hbytes(wtdatat)
ftdatat = i2hbytes(ftdatat)

wtdatad = i2hbytes(wtdatad)
ftdatad = i2hbytes(ftdatad)
# print(wdata.find(wtdatat))
# print(fdata.find(ftdatat))
# print(wdata.find(wtdatad))
# print(fdata.find(ftdatad))


# exit()

if False:
    npointer = name_location + (enemy_id * size_name) + mode
    dpointer = data_location + (enemy_id * size_data) + mode

    # tunnelarmr
    tnpointer = name_location + (tunnelarmr * size_name) + mode
    tdpointer = data_location + (tunnelarmr * size_data) + mode
    tlpointer = loca_location + (tunnel_loc * size_loca) + mode

    # dullahan
    dnpointer = name_location + (dullahan * size_name) + mode
    ddpointer = data_location + (dullahan * size_data) + mode

    dullahan_data = data[ddpointer:ddpointer + size_data]
    tunnelarmr_data = data[tdpointer:tdpointer + size_data]
    tloc_data = data[tlpointer:tlpointer + size_loca]

    print(filename)
    print("-" * 40)
    print("    TunnelArmr:")
    print(tunnelarmr_data)
    h = '0' + hex(tdpointer)[2:]
    lc = bytes.fromhex(h)
    print(lc)
    print(data.find(lc))
    print("        Location:")
    print(tloc_data)

    z = data[tlpointer: tlpointer + 1000]

# Starting at F8602, ff3usme changes a bunch of stuff

# Check for diffs
if False:
    sz = 0x20
    counter = 0xF0000
    mx = counter + sz * 5
    while counter < 0xFFFFF:
        fbyte = fdata[counter]
        ebyte = edata[counter]

        if fbyte != ebyte and counter < 0xfffff and not 0xF8600 <= counter <= 0xFF050:
            print(hex(counter))
            print("FF6: %s" % print_hex(fdata[counter: counter + sz], sz))
            print("EDT: %s" % print_hex(edata[counter: counter + sz], sz))
            counter += sz
        else:
            counter += 1

# Check for diffs in WC
if False:
    sz = 0x20
    counter = 0xF0000
    mx = counter + sz * 5
    while counter < mx:
        fbyte = fdata[counter]
        wbyte = wdata[counter]

        if counter == 0xF0000 or (fbyte != wbyte and counter < mx and not 0xF8600 <= counter <= 0xFF050):
            print(hex(counter))
            if counter == 0xF0000:
                print("Monster Data Base for Reference")
            f = "FF6: %s" % print_hex(fdata[counter: counter + sz], sz)
            e = "EDT: %s" % print_hex(edata[counter: counter + sz], sz)
            w = "WC : %s" % print_hex(wdata[counter: counter + sz], sz)
            print(f.strip())
            print(e.strip())
            print(w.strip())
            print()

            counter += sz
        else:
            counter += 1

# Compare monsters
if False:
    monster = 0
    sz = 0x20
    count = 384
    counter = 0xF0000

    wc_monst = []
    ff_monst = []
    # while counter < (counter + count * sz):
    while counter < 0xF3000:
        f = print_hex(fdata[counter: counter + sz], sz)
        e = print_hex(edata[counter: counter + sz], sz)
        w = print_hex(wdata[counter: counter + sz], sz)
        fmonst = Monster(ENEMIES[monster], fdata[counter: counter + sz])
        wmonst = Monster(ENEMIES[monster], wdata[counter: counter + sz])

        # if counter == 0xF0000 or f != w:
        if counter == 0xF0000 or f != w:
            # print (hex(counter))
            if counter == 0xF0000:
                print("Monster Data Base for Reference")
            ff = "FF6: %s" % f
            ee = "EDT: %s" % e
            ww = "WC : %s" % w
            print(fmonst.compare(wmonst))
            # print (ff.strip())
            # print (ee.strip())
            # print (ww.strip())
            # print()

        wc_monst.append(copy.deepcopy(wmonst))
        ff_monst.append(copy.deepcopy(fmonst))
        counter += sz
        monster += 1
    exit()

# Compare Battlegroups
if False:
    count = 0
    sz = 0x8
    base = 0xF4800
    mx = 0xF5000
    counter = base

    wc_monst = []
    ff_monst = []

    while counter < mx:
        f = print_hex(fdata[counter: counter + sz], sz)
        e = print_hex(edata[counter: counter + sz], sz)
        w = print_hex(wdata[counter: counter + sz], sz)

        fbg = Battlegroup(fdata[counter: counter + sz])
        wbg = Battlegroup(wdata[counter: counter + sz])

        if counter == base or f != w:
            print(hex(counter))
            if counter == base:
                print("Base for Reference")
            ff = "FF6: %s" % f
            ee = "EDT: %s" % e
            ww = "WC : %s" % w
            # print (ff.strip())
            # print (ee.strip())
            # print (ww.strip())
            # print()
            print(fbg.compare(wbg))

        counter += sz
        count += 1
    exit()

# Event Battlegroups
# These are all the same in WC as FF
if False:
    count = 0
    sz = EVENT_BATTLE_GROUP_SIZE
    base = EVENT_BATTLE_GROUP_LOC
    mx = base + sz * EVENT_BATTLE_GROUP_COUNT
    counter = base

    wc_monst = []
    ff_monst = []

    while counter < mx:
        f = print_hex(fdata[counter: counter + sz], sz)
        e = print_hex(edata[counter: counter + sz], sz)
        w = print_hex(wdata[counter: counter + sz], sz)

        # fbg = Battlegroup(fdata[counter : counter + sz])
        # wbg = Battlegroup(wdata[counter : counter + sz])

        if counter == base or f != w or counter == mx - sz:
            print(hex(counter))
            if counter == base:
                print("Base for Reference")
            elif counter == mx - sz:
                print("Last for Reference")
            ff = "FF6: %s" % f
            ee = "EDT: %s" % e
            ww = "WC : %s" % w
            print(ff.strip())
            print(ee.strip())
            print(ww.strip())
            print()
            # print(fbg.compare(wbg))

        counter += sz
        count += 1
    exit()

# WOB Battle Groups
# These are all the same in WC as FF
if False:
    count = 0
    sz = 0x04
    base = 0xF5400
    mx = base + sz * 64
    counter = base

    wc_monst = []
    ff_monst = []

    while counter < mx:
        f = print_hex(fdata[counter: counter + sz], sz)
        e = print_hex(edata[counter: counter + sz], sz)
        w = print_hex(wdata[counter: counter + sz], sz)

        # fbg = Battlegroup(fdata[counter : counter + sz])
        # wbg = Battlegroup(wdata[counter : counter + sz])

        if counter == base or f != w or counter == mx - sz:
            print(hex(counter))
            if counter == base:
                print("Base for Reference")
            elif counter == mx - sz:
                print("Last for Reference")
            ff = "FF6: %s" % f
            ee = "EDT: %s" % e
            ww = "WC : %s" % w
            print(ff.strip())
            print(ee.strip())
            print(ww.strip())
            print()
            # print(fbg.compare(wbg))

        counter += sz
        count += 1
    exit()

# WOR Battle Groups
# These are all the same in WC as FF
if False:
    count = 0
    sz = 0x04
    base = 0xF5500
    mx = base + sz * 64
    counter = base

    wc_monst = []
    ff_monst = []

    while counter < mx:
        f = print_hex(fdata[counter: counter + sz], sz)
        e = print_hex(edata[counter: counter + sz], sz)
        w = print_hex(wdata[counter: counter + sz], sz)

        # fbg = Battlegroup(fdata[counter : counter + sz])
        # wbg = Battlegroup(wdata[counter : counter + sz])

        if counter == base or f != w or counter == mx - sz:
            print(hex(counter))
            if counter == base:
                print("Base for Reference")
            elif counter == mx - sz:
                print("Last for Reference")
            ff = "FF6: %s" % f
            ee = "EDT: %s" % e
            ww = "WC : %s" % w
            print(ff.strip())
            print(ee.strip())
            print(ww.strip())
            print()
            # print(fbg.compare(wbg))

        counter += sz
        count += 1
    exit()

# Map Battlegroups
# These are all the same in WC as FF
if False:
    count = 0
    sz = 0x01
    base = 0xF5600
    mx = base + sz * 512
    counter = base

    wc_monst = []
    ff_monst = []

    while counter < mx:
        f = print_hex(fdata[counter: counter + sz], sz)
        e = print_hex(edata[counter: counter + sz], sz)
        w = print_hex(wdata[counter: counter + sz], sz)

        # fbg = Battlegroup(fdata[counter : counter + sz])
        # wbg = Battlegroup(wdata[counter : counter + sz])

        if counter == base or f != w or counter == mx - sz:
            print(hex(counter))
            if counter == base:
                print("Base for Reference")
            elif counter == mx - sz:
                print("Last for Reference")
            ff = "FF6: %s" % f
            ee = "EDT: %s" % e
            ww = "WC : %s" % w
            print(ff.strip())
            print(ee.strip())
            print(ww.strip())
            print()
            # print(fbg.compare(wbg))

        counter += sz
        count += 1
    exit()

# Aux Battle Data
if False:
    count = 0
    sz = 0x4
    base = 0xF5900
    mx = base + sz * 576
    counter = base

    wc_monst = []
    ff_monst = []

    while counter < mx:
        f = print_hex(fdata[counter: counter + sz], sz)
        e = print_hex(edata[counter: counter + sz], sz)
        w = print_hex(wdata[counter: counter + sz], sz)

        # fbg = Battlegroup(fdata[counter : counter + sz])
        # wbg = Battlegroup(wdata[counter : counter + sz])

        if counter == base or f != w or counter == mx - sz:
            print(hex(counter))
            if counter == base:
                print("Base for Reference")
            elif counter == mx - sz:
                print("Last for Reference")
            ff = "FF6: %s" % f
            ee = "EDT: %s" % e
            ww = "WC : %s" % w
            print(ff.strip())
            print(ww.strip())
            print()
            # print(fbg.compare(wbg))

        counter += sz
        count += 1
    exit()

# Battle Data
# Different position data for Chadarnook
if False:
    count = 0
    sz = 0xF
    base = 0xF6200
    mx = base + sz * 576
    counter = base

    wc_monst = []
    ff_monst = []

    while counter < mx:
        f = print_hex(fdata[counter: counter + sz], sz)
        e = print_hex(edata[counter: counter + sz], sz)
        w = print_hex(wdata[counter: counter + sz], sz)

        # fbg = Battlegroup(fdata[counter : counter + sz])
        # wbg = Battlegroup(wdata[counter : counter + sz])

        if counter == base or f != w or counter == mx - sz:
            print(hex(counter))
            if counter == base:
                print("Base for Reference")
            elif counter == mx - sz:
                print("Last for Reference")
            ff = "FF6: %s" % f
            ee = "EDT: %s" % e
            ww = "WC : %s" % w
            print(ff.strip())
            print(ee.strip())
            print(ww.strip())
            print()
            # print(fbg.compare(wbg))

        counter += sz
        count += 1
    exit()

# Pointers to Monster Scripts
if False:
    count = 0
    sz = 0x2
    base = 0xF8400
    mx = base + sz * 384
    counter = base

    wc_monst = []
    ff_monst = []

    while counter < mx:
        f = print_hex(fdata[counter: counter + sz], sz).strip()
        e = print_hex(edata[counter: counter + sz], sz).strip()
        w = print_hex(wdata[counter: counter + sz], sz).strip()

        # fbg = Battlegroup(fdata[counter : counter + sz])
        # wbg = Battlegroup(wdata[counter : counter + sz])

        if counter == base or f != w or counter == mx - sz or True:
            print("%s -- %s" % (hex(counter), ENEMIES[count]))
            if counter == base:
                print("Base for Reference")
            elif counter == mx - sz:
                print("Last for Reference")
            ff = "FF6: %s -- %s" % (f, hex(int.from_bytes(fdata[counter: counter + sz], "little") + 0xF8700))
            ee = "EDT: %s -- %s" % (e, hex(int.from_bytes(edata[counter: counter + sz], "little") + 0xF8700))
            ww = "WC : %s -- %s" % (w, hex(int.from_bytes(wdata[counter: counter + sz], "little") + 0xF8700))
            print(ff.strip())
            # print (ee.strip())
            print(ww.strip())
            print()
            # print(fbg.compare(wbg))

        counter += sz
        count += 1
    exit()

# Event Scripts
if True:
    count = 0
    sz = 0x10
    base = 0
    mx = 0xCE600
    counter = base

    ff6_events = copy.deepcopy(EVENTS)
    wc1_events = copy.deepcopy(EVENTS)
    wc2_events = copy.deepcopy(EVENTS)

    outfn = "events.html"
    with open(outfn, 'w') as f:
        output = '<html><body bgcolor="black"><font face="monospace" color="green">\n'
        for startaddr in EVENTS.keys():
            length = EVENTS[startaddr]["length"]
            ff6_data = fdata[startaddr: startaddr + length]
            wc1_data = wdata[startaddr: startaddr + length]
            wc2_data = xdata[startaddr: startaddr + length]

            ff6_events[startaddr]["data"] = ff6_data
            wc1_events[startaddr]["data"] = wc1_data
            wc2_events[startaddr]["data"] = wc2_data

            pipe = '&nbsp;<b><font size = "+1" color = "white">|</font></b>&nbsp;'

            if wc1_data != wc2_data:
                output += "<h2>%s</h2>" % EVENTS[startaddr]["description"]
                output += '<font size = "+2"><b>%s</b></font><br/>\n' % (
                            hex(startaddr) + "--" + EVENTS[startaddr]["type"])

                locctr = 0

                output += "<b>FF6:</b>&nbsp;%s<br/>\n" % (print_hex(ff6_data, length).replace(" ", '&nbsp;'))

                output += "<b>WC1:</b>&nbsp;"
                for i in range(length):
                    spacer = "&nbsp;"
                    if locctr != 0 and locctr % 16 == 0:
                        spacer = pipe
                    if wc1_data[i] != wc2_data[i]:
                        output += '<font color="red"><b>%s</b></font>%s' % (print_hex(wc1_data[i], 1).strip(), spacer)
                    else:
                        output += '%s%s' % (print_hex(wc1_data[i], 1).strip(), spacer)
                    locctr += 1

                output += "\n<br/>"
                output += "<b>WC2:</b>&nbsp;"
                locctr = 0

                for i in range(length):
                    spacer = "&nbsp;"
                    if locctr != 0 and locctr % 16 == 0:
                        spacer = pipe
                    if wc1_data[i] != wc2_data[i]:
                        output += '<font color="red"><b>%s</b></font>%s' % (print_hex(wc2_data[i], 1).strip(), spacer)
                    else:
                        output += '%s%s' % (print_hex(wc2_data[i], 1).strip(), spacer)
                    locctr += 1
                output += "\n<br/><hr/>"

        output += "</font></body></html>"
        f.write(output)
        # print (hex(startaddr), "--", EVENTS[startaddr]["type"], "--", EVENTS[startaddr]["description"])
        # print ("-" * 20)
        # print ("FF6:", print_hex(ff6_data, length))
        # print ("WC1:", print_hex(wc1_data, length))
        # print ("WC2:", print_hex(wc2_data, length))
