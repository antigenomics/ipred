#!/usr/bin/env python

# ipred script is designed to make netMHCpan predictions for a dataset of epitopes with different MHC's

import os, sys, subprocess, argparse, tempfile, shutil
import pandas as pd
import numpy as np
from tqdm import tqdm
import logging
from datetime import datetime

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help = 'Path to the table file with k-mers and HLA')
    parser.add_argument('--destination', '-d', default = os.getcwd(), help = 'Path where to store output, default is current wd')
    args = parser.parse_args()

    # set up logging to file
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='logs/ipred_{}.log'.format(datetime.now().isoformat() ),
                        filemode='w')

    f = args.file
    d = args.destination

    f = str(f)
    d = str(d)

    destination=d
    ncores="80"
    netmhcpan = '/home/vcvetkov/Tools/netMHCpan-4.0/netMHCpan'
    # netmhcpan = '/home/vts/Tools/netMHCpan-3.0/netMHCpan'

    df = pd.read_csv(f)
    mhc = []
    for col in ['mhc', 'hla', 'allele', 'MHC', 'Allele', 'HLA']:
        if col in df.columns:
            mhc.append(col)
    if len(mhc) != 1:
        raise Exception("Please specify the MHC column in your table file")

    tmpdir = tempfile.mkdtemp()
    parallel_tmpdir = tempfile.mkdtemp()
    nmp_tempdir = tempfile.mkdtemp()

    pdf = df.groupby(by=mhc)
    mhclst = np.unique(df[mhc].values)
    for group in mhclst:
        with_imm = tmpdir + "/fornmp_{}.csv".format(group.replace('*', ''))
        wout_imm = tmpdir + "/imminf_{}.csv".format(group.replace('*', ''))

        pdf.get_group(group)['peptide'].to_csv(with_imm, index=False)
        pdf.get_group(group)[['peptide', 'Immunogenicity']].to_csv(wout_imm, index=False)


    for allele in tqdm(mhclst):
        prefix = tmpdir + "/fornmp_"
        midpoint = nmp_tempdir + '/unprocessed_{}.csv'.format(allele.replace('*', ''))
        hla_allele = allele.replace('*', '')
      
        process = subprocess.run('{} -p -BA -a {} \
                                 -f {} > {}'.format(netmhcpan,
                                                    hla_allele,
                                                    prefix + hla_allele + '.csv',
                                                    midpoint), shell=True, stdout=subprocess.PIPE)

        process = subprocess.run("sed -i '/^ /!d' {}".format(midpoint), shell=True)

        if os.stat(midpoint).st_size == 0:
            os.remove(midpoint)
            logging.warning('{} file was removed for some reason. Probably not a correct MHC'.format(allele))

    print('netmhcpan has finished computing!')

    tdf = pd.DataFrame()
    for f in tqdm(os.listdir(nmp_tempdir)):
        allele = f.strip('unprocessed_').split('.')[0]
        with open(nmp_tempdir + '/' + f, 'r+') as file:
            lines = []
            for line in file:
                lines.append(line.strip().split()[:14])
            columnlst = lines[0]
            lines = [line for line in lines if line != columnlst]

        idf = pd.read_csv(tmpdir + "/imminf_{}.csv".format(allele))

        wdf = pd.DataFrame(lines, columns=columnlst)
        wdf = wdf[['HLA', 'Peptide', '%Rank']]
        wdf['Immunogenicity'] = idf['Immunogenicity']

        tdf = pd.concat([tdf, wdf], axis=0, ignore_index=True)

    tdf.to_csv(destination, index=False)
    print("Predictions have been made correctly")
    
    shutil.rmtree(tmpdir)
    shutil.rmtree(parallel_tmpdir)
    shutil.rmtree(nmp_tempdir)