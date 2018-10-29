import subprocess, argparse
import pandas as pd
import os
import time
import logging 
from datetime import datetime


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help='Path to the file with fasta sequence to generate k-mers')
    args = parser.parse_args()

    f = args.file

    dest = f.split('/')[-1].split('_')[0]

    # set up logging to file
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='logs/ipred1_{}_{}.log'.format(dest, datetime.now().isoformat() ), # timespec='microseconds' is available only in python 3.6
                        filemode='w')


    hlalst = ['HLA-A*01:01',
     'HLA-A*02:01',
     'HLA-A*02:02',
     'HLA-A*02:03',
     'HLA-A*02:05',
     'HLA-A*02:06',
     'HLA-A*02:07',
     'HLA-A*02:11',
     'HLA-A*02:17',
     'HLA-A*03:01',
     'HLA-A*11:01',
     'HLA-A*23:01',
     'HLA-A*24:02',
     'HLA-A*24:03',
     'HLA-A*25:01',
     'HLA-A*26:01',
     'HLA-A*29:02',
     'HLA-A*30:01',
     'HLA-A*30:02',
     'HLA-A*31:01',
     'HLA-A*32:01',
     'HLA-A*33:01',
     'HLA-A*33:03',
     'HLA-A*68:01',
     'HLA-A*68:02',
     'HLA-B*07:02',
     'HLA-B*08:01',
     'HLA-B*14:02',
     'HLA-B*15:01',
     'HLA-B*15:03',
     'HLA-B*15:10',
     'HLA-B*27:02',
     'HLA-B*27:05',
     'HLA-B*35:01',
     'HLA-B*35:02',
     'HLA-B*35:03',
     'HLA-B*35:14',
     'HLA-B*37:01',
     'HLA-B*38:01',
     'HLA-B*39:01',
     'HLA-B*39:05',
     'HLA-B*39:06',
     'HLA-B*40:01',
     'HLA-B*40:02',
     'HLA-B*40:06',
     'HLA-B*41:02',
     'HLA-B*42:01',
     'HLA-B*44:02',
     'HLA-B*44:03',
     'HLA-B*45:01',
     'HLA-B*48:01',
     'HLA-B*50:01',
     'HLA-B*51:01',
     'HLA-B*52:01',
     'HLA-B*53:01',
     'HLA-B*55:01',
     'HLA-B*55:02',
     'HLA-B*57:01',
     'HLA-B*57:03',
     'HLA-B*58:01',
     'HLA-C*02:02',
     'HLA-C*03:03',
     'HLA-C*03:04',
     'HLA-C*04:01',
     'HLA-C*06:02',
     'HLA-C*07:01',
     'HLA-C*08:01',
     'HLA-C*08:02']


    logging.info('Reading {} file with proteome sequence'.format(f))

    for hla in hlalst:
        for i in [8, 9, 10, 11, 12, 13]:
            destination = "../output/nmp/{}_{}_{}_nmp.txt".format(dest, hla, i)
            process = subprocess.run("python ipred1.py -l {length:02} \
                                      -f {file} -d {destination} \
                                      -a {hla}".format(length=i,
                                                       file=f,\
                                                       destination=destination,\
                                                       hla=hla), shell=True)
            if not process.returncode:
                print('.', end='')
            else:
                logging.warning(process)

            if not os.stat(destination).st_size == 0:
                logging.info('{} {} {}. Everything is going OK!'.format(dest, hla, i))
            else:
                logging.warning('{} {} {}. Something went WRONG!'.format(dest, hla, i))

        localtime = time.asctime( time.localtime(time.time()) )
        print( "Local current time :", localtime)

    tdf = pd.DataFrame()
    for item in os.listdir('../output/nmp/'):
        if item.startswith(dest):
            df = pd.read_csv('../output/nmp/' + item)
            tdf = pd.concat([tdf, df], axis=0)

    tdf['Origin_name'] = dest

    final = '../output/tmp/' + dest + '_nmp.csv'

    tdf.to_csv(final, index=False)

    if not os.stat(final).st_size == 0:
        logging.info('Predictions for {} finished computing'.format(f))
    else:
        logging.warning('Predictions for {} failed to compute!'.format(f))
