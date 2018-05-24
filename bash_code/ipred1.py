#!/usr/bin/env python

# Ipred1 script is intended to get kmers from fasta file of viral or human proteome
# and predict their binding affinity to MHC via netMHCpan in parallel

import os, sys, subprocess, argparse, tempfile, shutil
import pandas as pd
from tqdm import tqdm
from Bio import SeqIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--length', '-l', help='The length of generated peptides')
    parser.add_argument('--file', '-f', help='Path to the file with fasta sequence to generate k-mers')
    parser.add_argument('--destination', '-d', default='CMV_HLA-A02:01_nmp.txt',
                        help='Path where to store output, full path is prefered')
    parser.add_argument('--hla', '-a', default="HLA-A02:01", help='HLA allele for prediction')
    args = parser.parse_args()

    l = args.length
    f = args.file
    d = args.destination
    a = args.hla

    length = int(l)
    fasta_file = str(f)
    destination = str(d)
    hla_allele = str(a).replace('*', '')

    # This is path to netMHCpan in your system. Don't forget to change it accordingly!

    netmhcpan = '/home/vcvetkov/Tools/netMHCpan-4.0/netMHCpan'

    # Reading fasta file with proteome sequence

    record_dict = SeqIO.index(fasta_file, "fasta")

    # Generating k-mer peptides dataframe containing origin protein info for each peptide
    # pdf is peptide dataframe

    pdf = pd.DataFrame()
    for key in tqdm(record_dict):
        lst = []
        df = pd.DataFrame()
        for i in range(len(record_dict[key].seq)-length):
            string = str(record_dict[key].seq[i:i+length])
            lst.append(string)
        df['Peptide'] = lst
        df['Origin_protein'] = key.split('|')[-1]
        pdf = pd.concat([pdf, df], axis=0)

    pdf = pdf.reset_index(drop=True)

    # Creating temporary directories for files

    tmpdir = tempfile.mkdtemp()
    parallel_tmpdir = tempfile.mkdtemp()
    nmp_tempdir = tempfile.mkdtemp()

    prefix = tmpdir + "/split_"
    midpoint = nmp_tempdir + '/unprocessed_file_nmp.txt'

    # Splitting into 5000 line files (netMHCpan constaint)

    for i in range(1, len(pdf)//5000 + 2):
        if i > len(pdf)//5000:
            df = pdf.iloc[5000*(i-1):,:]
        else:
            df = pdf.iloc[5000*(i-1):5000*i,:]
        df['Peptide'].to_csv(prefix + "{0:04}".format(i) + '.txt', index=False, header=False)
     
    # Paralleling netMHCpan with gnu parallel

    process = subprocess.run('parallel --eta --jobs 80 -k \
                             --tmpdir {} {} -p -BA -a {} \
                             -f ::: {} > {}'.format(parallel_tmpdir,
                                                    netmhcpan,
                                                    hla_allele,
                                                    prefix + '*',
                                                    midpoint), shell=True)

    # print('Subprocess returned code {}'.format(process.returncode))
    if not process.returncode: print('.', end='')

    process = subprocess.run("sed -i '/^ /!d' {}".format(midpoint), shell=True)
    # print('Subprocess returned code {}'.format(process.returncode))
    if not process.returncode: print('.', end='')

    if os.path.isfile(midpoint): print('.', end='')
    if not os.stat(midpoint).st_size == 0: print('.', end='')

    # netMHCpan's output format is weird and pandas cannot read it properly.
    # Here we remove extra spaces and the last column. The latter could be used
    # but it is not necessary

    with open(midpoint, 'r+') as file:
        lines = []
        for line in file:
            lines.append(line.strip().split()[:14])
        columnlst = lines[0]
        lines = [line for line in lines if line != columnlst]

    tdf = pd.DataFrame(lines, columns=columnlst)
    tdf = tdf[['HLA', 'Peptide', 'Aff(nM)']]
    tdf['Origin_protein'] = pdf['Origin_protein'].values

    # Check that the order is preserved and each peptide matches with its origin protein

    lst1 = list(pdf['Peptide'].values)
    lst2 = list(tdf['Peptide'].values)
    diff = []
    for i in range(len(lst1)):
        if lst1[i] != lst2[i]:
            diff.append(i)
    if not len(diff): print('.')

    # There are overall five checks in this script. If there are five dots in the output
    # then the final file should have been processed correctly

    flag = False

    if os.path.exists(destination):
        smart_name = destination + '/' + os.path.basename(fasta_file).split('.')[0] + '_' + hla_allele + '_nmp'
        if not os.path.isfile(smart_name + '.csv'):
            tdf.to_csv(smart_name + '.csv', index=False)
            flag = True
        else:
            for i in range(10):
                if not os.path.isfile(smart_name + '{0:02}.csv'.format(i)):
                    tdf.to_csv(smart_name + '{0:02}.csv'.format(i), index=False)
                    flag = True
                if flag:
                    break
    else:
        tdf.to_csv(destination, index=False)
        flag = True

    if not flag:
        tdf.to_csv(destination, index=False)
        flag = True

    if flag:
        print("Predictions have been made correctly")
    else:
        print("Something went wrong")


    shutil.rmtree(tmpdir)
    shutil.rmtree(parallel_tmpdir)
    shutil.rmtree(nmp_tempdir)