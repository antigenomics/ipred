#!/usr/bin/env python

import os, sys, subprocess, argparse, tempfile, shutil
import pandas as pd
from tqdm import tqdm
from Bio import SeqIO

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_kmers(length, seq_dict, tempfile):
    for key in tqdm(seq_dict):
        for i in range(len(seq_dict[key].seq)-length):
            string = str(seq_dict[key].seq[i:i+length])+'\n'
            tempfile.write(string.encode())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--length', '-l', help = 'The length of generated peptides')
    parser.add_argument('--file', '-f', help = 'Path to the file with fasta sequence to generate k-mers')
    parser.add_argument('--destination', '-d', dafault = os.getcwd(), help = 'Path where to store output, default is current wd')
    args = parser.parse_args()

    l = args.length
    f = args.file
    d = args.destination

    l = int(l)
    f = str(f)
    d = str(d)

    destination=d
    ncores="80"
    nmp_home="/home/vcvetkov/Projects/ipred/bash_code"

    record_dict = SeqIO.index(f, "fasta")

    with tempfile.NamedTemporaryFile(suffix='_temp', prefix='jd_', dir='/tmp', delete=False) as temp:
        get_kmers(l, record_dict, temp)
        temp.seek(0)
        name = temp.name
    
    # subprocess.run("./ipred_test.sh -f {}".format(name), shell=True)

    tmpdir = tempfile.mkdtemp()
    prefix = tmpdir + "/split_"

    print("split -d -e -l 5000 --additional-suffix=.split {name} {prefix}".format(name=name, prefix=prefix))

    subprocess.run("split -d -e -l 5000 --additional-suffix=.split {name} {prefix}".format(name=name, prefix=prefix), shell=True)

    print(os.listdir(tmpdir))

    subprocess.run("./NMP_core.sh -a {} -n {} -o {} -d {} -f {}".format("HLA-A02:01", ncores, tmpdir, destination, "split_"), shell=True)
    
    os.unlink(name)
    shutil.rmtree(tmpdir)
