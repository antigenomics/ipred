#!/usr/bin/python

import argparse
import sys
from tqdm import tqdm
from Bio import SeqIO

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_kmers(length, record_dict):
    filename = 'output/peptides_raw.txt'
    target = open(filename, 'w+')
    for key in tqdm(record_dict):
        for i in range(len(record_dict[key].seq)-length):
            target.write(str(record_dict[key].seq[i:i+length])+'\n')
    target.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--length', '-l', help = 'The length of generated peptides')
    args = parser.parse_args()

    l = args.length

    record_dict = SeqIO.index("data/UP000005640_9606.fasta", "fasta")
    eprint("Dictionary has been loaded")
    get_kmers(l, record_dict)
    eprint("Processing complete")

