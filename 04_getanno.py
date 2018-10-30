from __future__ import print_function
import re
import os
import argparse


def checkEmpty(infile):
    return os.path.isfile(infile) and os.path.getsize(infile) == 0

def getBlastResults(infile, ftype): 
    with open(infile) as f_in:
        fname = os.path.basename(f_in.name)
        final = {}
        ardict = {}
        if checkEmpty(infile):
            print(str(fname) + "\t" + "no arCOG hits found.")
        else:
            prev = " "
            for line in f_in:
                values = line.split("\t")
                if values[0] == prev:
                    pass
                else:
                    ardict[values[0]] = values[1]
                    prev = values[0]
            if ftype == "group":
                expected = next(iter(ardict.values()))
                check = all(value == expected for value in ardict.values())
                if check:
                    expected_re = re.findall(r"(arCOG[0-9]+)\_[0-9]+_[0-9]+", expected)
                    result = expected_re[0]
                else:
                    ex_values = list(set(ardict.values()))
                    r = re.compile(r'(arCOG[0-9]+)\_[0-9]+_[0-9]+')
                    result = [m.group(1) for m in (r.match(x) for x in ex_values) if m]
                final[fname] = result
            elif ftype == "single":
                for k,v in ardict.items():
                    exp_v = re.findall(r"(arCOG[0-9]+)\_[0-9]+_[0-9]+", v)
                    ardict[k] = exp_v[0]
                final = ardict
    return final

def getAnno(final, artab):
    if not final:
        pass
    else:
        arANNO = {}
        with open(artab) as f_in:
            for line in f_in:
                values = line.split("\t")
                arANNO[values[0].replace('"', '')] = (values[1].replace('"', ''), values[2].replace('"', ''))
        for k, v in sorted(final.items()):
            for x, y in arANNO.items():
                if isinstance(v, list):
                    for a in v:
                        if a == x:
                            print(str(k) + "\t" + str(x) + "\t" + str(y[0]) + "\t" + str(y[1]), end="")
                else:
                    if final[k] == x:
                        print(str(k) + "\t" + str(x) + "\t" + str(y[0]) + "\t" + str(y[1]), end="")



parser = argparse.ArgumentParser(
    description='-i is infile, -t is path of arANNO_tab ')
parser.add_argument('-i',
                    help='blast file path')
parser.add_argument('-a',
                    help='arANNO tab path')
parser.add_argument('-t',
                    help='file type')
args = parser.parse_args()


getAnno(getBlastResults(args.i, args.t), args.a)








