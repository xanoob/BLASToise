from __future__ import print_function
from collections import defaultdict
from Bio import SeqIO
import os
import csv
import re

# Store ar14_GI in dictionary
print("Storing ar14_GI.tab in dictionary ... this might take a while ...")
with open("ar14_GI.tab", "rb") as f_in:
    arGI = defaultdict(list)
    reader = csv.reader(f_in, delimiter='\t')
    ct = 1
    for row in reader:
        print(ct)
        ct += 1
        if row[1] in arGI.keys():
            arGI[row[1]].append(row[0])
        else:
            arGI[row[1]] = [row[0]]
print("Done.")

# Store ar14_anno in dictionary
print ("Now storing ar14_anno.tab in dictionary ...")
with open("ar14_anno.tab", "rb") as f_in:
    arANNO = defaultdict(list)
    reader = csv.reader(f_in, delimiter='\t')
    for row in reader:
        arANNO[row[0]] = (row[1], row[2])
print("Done.")

# Combine both dictionaries
print("Now combining both dictionaries...")
arALL = defaultdict(list)
for a,b in arGI.items() + arANNO.items():
    arALL[a].append(b)
print("Done.")


# Some extra info
print("Creating and saving combined dictionary in arCOG_combined.tab...")
with open("arCOG_combined.tab", "wb") as f_out:
    print("arCOG_ID", "\t", "arCOG_cat", "\t", "annotation", "\t", "num_seqs", "\t", "seq_GIs", file=f_out)
    for k,v in arALL.items():
        print(k, "\t", v[1][0], "\t", v[1][1], "\t", len(v[0]), "\t".join([str(i) for i in v[0]]), sep="\t", file=f_out)
print("Done.")


print("Creating and saving arCOG sequence count table in arCOG_seqct.txt...")
with open("arCOG_seqct.txt", "wb") as f_out:
    lenGI = 0
    for k in sorted(arALL):
        print(k, len(arALL[k][0]), file=f_out)
        lenGI += len(arALL[k][0])
    print("arCOGs: ", len(arALL), file=f_out)
    print("total seqs: ", lenGI, file=f_out)
print("Done! Check out arCOG_seqct.txt.")


# Duplicate finding
print("Now finding which sequences belong to multiple arCOGs (or have multiple domains) ...")
with open("ar14_GI.tab", "rb") as f:
    reader = csv.reader(f, delimiter='\t')
    GI = defaultdict(list)
    GI_dup = defaultdict(list)
    ct = 1
    for row in reader:
        print("dup:", ct)
        ct += 1
        if row[0] in GI.keys():
            GI_dup[row[0]] = [GI[row[0]]]
            GI_dup[row[0]].append(row[1])
        else:
            GI[row[0]] = row[1]

with open("arCOG_multiples.tab", "wb") as f_out:
    for k,v in GI_dup.items():
        print(k, "\t".join([str(i) for i in v]), sep="\t", file=f_out)

"""
print("Loading faa_seqs.")
faa_seqs = SeqIO.parse(open("ar14.fa"), 'fasta')

print("Sorting fasta seqs into arCOGs...this REALLY takes a while...")
fcount = 0
for faa in faa_seqs:
    match = re.findall(r"gi\|(\d+)", faa.id)
    fcount += 1
    for k,v in sorted(arALL.items()):
        for n in v[0]:
            if n == match[0]:
                print(fcount, n, k, faa.id)
                faa_name = os.path.join(k + ".faa")
                with open(faa_name, 'a') as out:
                    print(">" + faa.id, file=out)
                    print(str(faa.seq), file=out)
"""
