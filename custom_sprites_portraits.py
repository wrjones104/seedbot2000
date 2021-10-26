import random
from portraits import id_portrait
from sprites import id_sprite
from palettes import id_palette

ffiv = " -name Rydia.CecilP.CecilD.Edge.Palom.Porom.Rosa.Tellah.RydiaC.Cid.Kain.Edward.FuSoYa.Yang" \
       " -cpal 98.110.30.87.109.33.61 -cpor 74.36.34.41.66.67.72.77.73.38.53.42.47.80.46" \
       " -cspr 110.41.40.50.99.100.108.121.109.43.80.51.63.134.119.62.18.19.91.73" \
       " -cspp 0.1.2.2.3.3.1.4.0.5.2.3.4.5.5.3.0.5.4.6"
tmnt = " -name VENUS.CASEY.LEO.MIKEY.BEBOP.RAPH.APRIL.SPLINT.SHREDR.DONNY.KRANG.BARON.FOOT.ROCK" \
       " -cpal 131.96.88.142.0.47.3" \
       " -cspr 3.32.3.3.33.3.6.82.56.3.129.61.97.13.14.15.18.19.20.21" \
       " -cspp 4.2.5.0.2.2.3.1.3.1.5.4.4.4.1.0.0.1.0.6"
badguys = " -name EDEA.BOMB.LEO.GOLBEZ.VICKS.WEDGE.KUJA.GEST.KEFKA.EXDETH.SEYMOR.GREG.GHOST.IMP" \
          " -cpor 100.33.15.50.18.18.82.48.56.102.105.104.17.14.11" \
          " -cspr 49.38.16.73.14.14.138.71.21.56.117.72.20.15.2.11.49.1.6.123" \
          " -cspp 3.3.0.1.1.0.1.3.3.4.4.3.0.0.4.3.6.1.0.2"
moogles = " -name KUPEK.KUMAMA.KUPOP.KUSHU.KUKU.KAMOG.KURIN.KURU.KUPO.KUTAN.MOG.KUPAN.GOGO.UMARO" \
          " -cpor 10.10.10.10.10.10.10.10.10.10.10.10.12.13.14" \
          " -cspr 10.10.10.10.10.10.10.10.10.10.10.10.12.13.82.15.10.19.20.82" \
          " -cspp 5.5.5.5.5.5.5.5.5.5.5.5.3.5.1.0.6.1.0.3"
mario = " -name DAISY.MARIO.HMRBRO.PAULIN.KAMEK.BOWSER.PEACH.TOAD.TOADET.JUNIOR.KNGBOO.LUIGI.GOOMBA.YOSHI" \
        " -cpal 138.34.88.37.62.137.64" \
        " -cspr 103.120.119.145.132.56.115.149.149.61.38.42.128.39.155.59.95.149.146.153" \
        " -cspp 3.1.4.3.4.2.5.3.5.2.5.2.3.0.6.3.3.1.5.6"
halloween_sotw_2021 = " -name Lilith.Locke.Frog.Shadow.Sans.Paprus.Leo.Galuf.Aeris.Kuja.PJMog.Mage.Gogo.Zerker" \
                      " -cpal 0.1.2.4.132.134.6 -cpor 0.1.103.3.89.88.15.7.97.82.95.59.12.31.17" \
                      " -cspr 144.19.61.3.148.146.69.64.30.138.155.90.12.35.20.20.18.20.20.21" \
                      " -cspp 4.1.0.3.5.5.0.3.0.4.4.0.3.1.0.0.6.0.0.0"
cirno_day = " -name Reimu.Locke.Gilga.Shadow.Gerad.Mash.Leo.Tellah.Cirno.Setzer.Mog.Gau.Gogo.Umaro" \
            " -cpal 0.1.127.34.4.80.6 -cpor 83.1.104.3.4.5.15.77.106.9.60.11.12.13.46" \
            " -cspr 139.1.72.3.4.5.69.121.44.9.92.11.12.142.42.62.44.145.147.21" \
            " -cspp 2.1.3.4.1.0.0.1.3.4.5.0.3.5.2.0.6.0.0.3"
alternates = "-name TERRA.LOCKE.CYAN.SHADOW.GERAD.SABIN.CELES.STRAGO.RELM.SETZER.MOG.GAU.GOGO.UMARO" \
             " -cpor 78.96.2.3.4.5.6.7.69.9.95.11.12.13.14" \
             " -cspr 122.156.2.97.4.5.6.64.105.9.155.68.152.142.14.15.18.19.20.21" \
             " -cspp 0.2.1.4.1.1.0.1.3.0.5.3.3.5.1.0.6.1.0.3"


def spraypaint():
    cpalf = random.choices(list(id_palette.keys()), k=7)
    cporf = random.choices(list(id_portrait.keys()), k=15)
    csprf = random.choices(list(id_sprite.keys()), k=20)
    csppf = random.choices(list(range(0, 6)), k=14)
    csppf2 = random.choices(list(range(0, 7)), k=6)

    cpal = ' '.join([' -cpal', '.'.join([str(cpalf[0]), str(cpalf[1]), str(cpalf[2]), str(cpalf[3]), str(cpalf[4]),
                     str(cpalf[5]), str(cpalf[6])])])
    cpor = ' '.join([' -cpor', '.'.join([str(cporf[0]), str(cporf[1]), str(cporf[2]), str(cporf[3]), str(cporf[4]),
                     str(cporf[5]), str(cporf[6]), str(cporf[7]), str(cporf[8]), str(cporf[9]), str(cporf[10]),
                     str(cporf[11]), str(cporf[12]), str(cporf[13]), str(cporf[14])])])
    cspr = ' '.join([' -cspr', '.'.join([str(csprf[0]), str(csprf[1]), str(csprf[2]), str(csprf[3]), str(csprf[4]),
                     str(csprf[5]), str(csprf[6]), str(csprf[7]), str(csprf[8]), str(csprf[9]), str(csprf[10]),
                     str(csprf[11]), str(csprf[12]), str(csprf[13]), str(csprf[14]), str(csprf[15]), str(csprf[16]),
                     str(csprf[17]), str(csprf[18]), str(csprf[19])])])
    cspp = ' '.join([' -cspp', '.'.join([str(csppf[0]), str(csppf[1]), str(csppf[2]), str(csppf[3]), str(csppf[4]),
                     str(csppf[5]), str(csppf[6]), str(csppf[7]), str(csppf[8]), str(csppf[9]), str(csppf[10]),
                     str(csppf[11]), str(csppf[12]), str(csppf[13]), str(csppf2[0]), str(csppf2[1]), str(csppf2[2]),
                     str(csppf2[3]), str(csppf2[4]), str(csppf2[5])])])

    custom_select = random.choice([ffiv, moogles, tmnt, badguys, mario, halloween_sotw_2021, ''.join([cpal, cspp]),
                                   ''.join([cpal, cpor, cspr, cspp, cirno_day, alternates])])
    return custom_select
