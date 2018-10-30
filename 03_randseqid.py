"""
Format names for PSI-BLAST PSSM generation -- append random numbers to seq_id as PSI-BLAST demands unique IDs

"""

from __future__ import print_function
from random import *
import re
import argparse


def getheaders(infile): # only read until newline
    headers = []
    rheaders = []
    with open(infile, "rb") as f_in:
        for _ in range(3): # skip first 3 lines
            next(f_in)
        for line in f_in:
            match = re.findall(r"(arCOG\d{5}_\d{3,})(\s.+)", line)
            if line.startswith("\n"):
                break
            if match:
                headers.append(match[0][0])
    for item in headers:
        x = randint(1,500)
        rheaders.append(item + "_" + "%03d" % x)
    return(rheaders)


def printh(infile, outfile, headers):
    with open(infile, "rb") as f:
        with open(outfile, "wb") as f_out:
            headerpop = list(headers)
            for line in f:
                match = re.findall(r"(arCOG\d{5}_\d{3,})(\s.+)", line)
                if match:
                    for item in headerpop:
                        itembit = re.findall(r"(arCOG\d{5}_\d{3,})_\d{3}", item)
                        if match[0][0] == itembit[0]:
                            print(item, match[0][1], file=f_out)
                            if len(headerpop) == 1:
                                headerpop = list(headers)
                            else:
                                headerpop.remove(item)
                elif line.startswith("CLUSTAL"):
                    print(line.rstrip(), file=f_out)
                elif line.startswith("\n"):
                    print(line.rstrip(), file=f_out)


parser = argparse.ArgumentParser(
    description='-i is infile, -o is outfile')
parser.add_argument('-i',
                    help='infile')
parser.add_argument('-o',
                    help='outfile')
args = parser.parse_args()


printh(args.i, args.o, getheaders(args.i))








