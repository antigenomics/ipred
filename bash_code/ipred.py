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
    args = parser.parse_args()

    l = args.length
    f = args.file

    l = int(l)
    f = str(f)

    destination="./"
    ncores="80"
    nmp_home="/home/vcvetkov/Projects/ipred/bash_code"

    record_dict = SeqIO.index(f, "fasta")

    with tempfile.NamedTemporaryFile(suffix='_temp', prefix='jd_', dir='/tmp', delete=False) as temp:
        get_kmers(l, record_dict, temp)
        temp.seek(0)
        name = temp.name
    
    subprocess.run("./ipred_test.sh -f {}".format(name), shell=True)

    """
    tmpdir = tempfile.mkdtemp()
    folder = tmpdir + "/"

    print("split -d -e -l 5000 --additional-suffix=.split {name} {dir}".format(name=name, dir=folder))

    subprocess.run("split -d -e -l 5000 --additional-suffix=.split {name} {dir}".format(name=name, dir=folder), shell=True)

    print(os.listdir(tmpdir))

    subprocess.run("./NMP_core.sh -a {} -n {} -o {} -d {}".format("HLA-A02:01", ncores, tmpdir, destination), shell=True)

    os.unlink(name)
    shutil.rmtree(tmpdir)
    """