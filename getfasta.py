from __future__ import print_function
import os
import shutil
import argparse


def getFam(namelist, basedir, newfolder):
    fastanames = [line.rstrip('\n') for line in open(namelist)]
    filepaths = [os.path.join(basedir,f) for f in fastanames]
    newdir = os.path.join(basedir, newfolder)
    for f in filepaths:
        if not os.path.isdir(newdir):
            os.makedirs(newdir)
        shutil.copy(f, newdir)



parser = argparse.ArgumentParser(
    description='-f is txt file of fasta filenames, -d base directory to look for files, -n new directory name ')
parser.add_argument('-f',
                    help='Path to text file with fasta filenames')
parser.add_argument('-d',
                    help='Base directory to look for files')
parser.add_argument('-n',
                    help='Name of new directory.')
args = parser.parse_args()


getFam(args.f, args.d, args.n)



