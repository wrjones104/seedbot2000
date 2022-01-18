import os
import subprocess
from zipfile import ZipFile

flag_presets = {
    "jones_special": "-cg -oa 2.5.5.1.r.1.r.1.r.1.r.1.r.1.r.1.r.1.r -ob 0.1.1.1.r -oc 0.1.1.1.r -od 0.1.1.1.r -oe "
                     "0.1.1.1.r -sc1 random -sc2 random -sc3 random -sal -eu -csrp 85 115 -fst -brl -slr 1 5 "
                     "-lmprp 75 125 -lel -srr 3 15 -rnl -rnc -sdr 1 1 -das -dda -dns -com "
                     "98989898989898989898989898 -rec1 28 -rec2 23 -xpm 3 -mpm 5 -gpm 5 -nxppd -lsced 2.5 -hmced "
                     "2.5 -xgced 1.5 -ase 2 -msl 50 -sed -bbs -be -bnu -res -fer 0 -escr 100 -dgne -wnz -mmnu "
                     "-cmd -esr 1 5 -ebr 68 -emprp 75 125 -nm1 random -rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi "
                     "-gp 5000 -smc 3 -sws 2 -sfd 3 -sto 1 -ieor 33 -ieror 33 -csb 3 12 -mca -stra -saw -sisr 15 "
                     "-sprp 75 125 -sdm 4 -npi -ccrt -cms -cor -crr -crvr 71 126 -crm -ari -anca -adeh -nfps -nu "
                     "-fs -fe -fvd -fr -fj -fbs -fedc -as -ond -rr -etn",
    "aj_special": "-cg -oa 2.2.2.1.r.1.r.1.r -ob 0.1.1.1.r -oc 0.1.1.1.r -od 0.1.1.1.r -sc1 random -sc2 random -sal "
                  "-eu -fst -brl -slr 1 5 -lmprp 75 125 -lel -srr 3 15 -rnl -rnc -sdr 1 1 -das -dda -dns -com "
                  "98989898989898989898989898 -rec1 28 -rec2 23 -xpm 3 -mpm 5 -gpm 5 -nxppd -lsced 2 -hmced 2 -xgced "
                  "2 -ase 2 -msl 40 -sed -bbs -be -bnu -res -fer 0 -escr 100 -dgne -wnz -mmnu -cmd -esr 1 5 -ebr 68 "
                  "-emprp 75 125 -nm1 random -rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi -smc 3 -ieor 33 -ieror 33 -csb "
                  "1 32 -mca -stra -saw -sisr 20 -sprp 75 125 -sdm 4 -npi -ccsr 20 -cms -cor -crr -crvr 255 255 -ari "
                  "-anca -adeh -nfps -nu -fs -fe -fvd -fr -fj -fbs -fedc -as -ond -rr",
    "standard_race": "-cg -oa 2.2.2.2.7.7.4.10.10 -ob 30.8.8.1.1.11.8 -sc1 random -sc2 random -sal -eu -fst -brl -slr "
                     "1 5 -lmprp 75 125 -lel -srr 3 15 -rnl -rnc -sdr 1 1 -das -dda -dns -com "
                     "98989898989898989898989898 -rec1 28 -rec2 23 -xpm 3 -mpm 5 -gpm 5 -nxppd -lsced 2 -hmced 2 "
                     "-xgced 2 -ase 2 -msl 40 -sed -bbs -be -bnu -res -fer 0 -escr 100 -dgne -wnz -mmnu -cmd -esr 1 5 "
                     "-ebr 68 -emprp 75 125 -nm1 random -rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi -smc 3 -ieor 33 "
                     "-ieror 33 -csb 1 32 -mca -stra -saw -sisr 20 -sprp 75 125 -sdm 4 -npi -ccsr 20 -cms -cor -crr "
                     "-crvr 255 255 -ari -anca -adeh -nfps -nu -fs -fe -fvd -fr -fj -fbs -fedc -as -ond -rr",
    "loot": "-cg -oa 2.5.5.1.r.1.r.1.r.1.r.1.r.1.r.1.r.1.r -ob 0.1.1.1.r -oc 0.1.1.1.r -od 0.1.1.1.r -oe "
                     "0.1.1.1.r -sc1 random -sc2 random -sc3 random -sal -eu -csrp 85 115 -fst -brl -slr 1 5 "
                     "-lmprp 75 125 -lel -srr 3 15 -rnl -rnc -sdr 1 1 -das -dda -dns -com "
                     "98989898989898989898989898 -rec1 28 -rec2 23 -xpm 3 -mpm 5 -gpm 5 -nxppd -lsced 2.5 -hmced "
                     "2.5 -xgced 1.5 -ase 2 -msl 50 -sed -bbs -be -bnu -res -fer 0 -escr 100 -dgne -wnz -mmnu "
                     "-cmd -esr 1 5 -ebr 68 -emprp 75 125 -nm1 random -rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi "
                     "-gp 5000 -smc 3 -sws 2 -sfd 3 -sto 1 -ieor 33 -ieror 33 -csb 3 12 -mca -stra -saw -sie "
                     "-sprp 75 125 -sdm 4 -npi -cce -cms -cor -crr -crvr 71 126 -crm -ari -anca -adeh -nfps -nu "
                     "-fs -fe -fvd -fr -fj -fbs -fedc -as -ond -rr -etn",
    "ex_test": "-open -sl -oa 2.2.2.2.7.7.4.10.10 -ob 56.1.1.11.8 -sc1 randomngu -sc2 randomngu -sc3 random -sal -fst "
               "-slr 5 8 -lmprp 75 125 -lel -srr 15 30 -rnl -sdr 1 1 -dda -dns -rec1 28 -rec2 23 -xpm 4 -mpm 5 -gpm 5 "
               "-nxppd -lsa 1 -hma 1 -xga 1 -msl 40 -sed -sfb -be -escr 100 -dgne -wnz -mmnu -cmd -esr 1 5 -ebr 100 "
               "-emprp 75 125 -ems -nm1 random -rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi -gp 5000 -smc 3 -sfd 3 -sto "
               "1 -ieor 33 -ierr 14 14 -csb 1 16 -mca -stra -saw -sisr 100 -sdm 5 -npi -ccsr 100 -cor -crr -crvr 75 "
               "128 -crm -ari -anca -adeh -nmc -nfce -fs -fe -fvd -fr -fj -fbs -fedc -as -ond -rr "
}


def local_wc(flags, filename):
    home = os.getcwd()
    args = ("python3 wc.py -i ff3.smc -o seedbot.smc " + flags)
    os.chdir('../worldscollide')
    try:
        os.mkdir('zips')
    except FileExistsError:
        pass
    try:
        subprocess.check_call(args)
        # create a ZipFile object
        zipObj = ZipFile('zips/'+filename+'.zip', 'w')
        # Add multiple files to the zip
        zipObj.write('seedbot.smc', arcname=filename+'.smc')
        zipObj.write('seedbot.txt', arcname=filename+'.txt')
        # close the Zip File
        zipObj.close()
        os.chdir(home)
    except subprocess.CalledProcessError:
        os.chdir(home)
        raise AttributeError


def twit_practice():
    flags = "-cg -sl -oa 2.2.2.2.6.6.4.8.8 -ob 3.2.2.2.7.7.4.10.10 -oc 26.3.3.1.1.12.7 -od 30.3.3.1.1.12.2.12.5 " \
            "-oe 38.1.1.12.4 -of 35.1.1.12.3 -og 48.15.15.1.1.12.1 -oh 29.10.10.1.1.11.44 -oi " \
            "31.7.10.3.3.11.10.11.13.11.3 -oj 40.1.1.11.22 -ok 23.5.5.1.1.11.52 -ol 22.5.5.1.1.12.8 -om " \
            "21.5.5.1.1.12.9 -sc1 sabin -sc2 gau -sc3 setzer -sal -eu -csrp 85 120 -fst -brl -slr 3 5 -lmprp 75 " \
            "125 -lel -srr 15 30 -rnl -rnc -sdr 1 3 -das -dda -dns -com 98169898980798989810981298 -rec1 28 -rec2 " \
            "13 -rec3 6 -rec4 14 -xpm 3 -mpm 5 -gpm 5 -nxppd -lsced 3 -hmced 2.5 -xgced 2.5 -ase 3 -msl 50 -sed " \
            "-bbs -be -bnu -res -fer 0 -escr 100 -dgne -wnz -mmnu -cmd -esr 1 5 -ebr 68 -emprp 75 125 -nm1 random " \
            "-rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi -gp 10000 -smc 3 -sws 2 -sfd 2 -sto 1 -ieor 40 -ieror 75 " \
            "-csb 4 12 -mca -stra -saw -sisr 15 -sprp 70 100 -sdm 5 -npi -snbr -snee -snil -ccsr 50 -cms -cspp " \
            "2.1.4.4.0.0.0.3.3.4.5.3.3.5.1.0.6.1.0.0 -cor -crr -crvr 100 100 -crm -cnee -cnil -ari -anca -adeh " \
            "-nee -nil -nu -nfps -fs -fe -fvd -fr -fj -fbs -fedc -as -ond -rr -etn "
    args = ("-i ff3.smc -o seedbot.smc " + flags)
    os.chdir('wc_official')
    os.system("py wc.py " + args)
    os.chdir('..')
