from __future__ import print_function

import os
from tqdm import tqdm, tqdm_notebook
from tqdm import trange

import pandas as pd
# import numpy as np
# import networkx as nx
# import seaborn as sns

import matplotlib.pyplot as plt

# from Bio import SeqIO

# from mhcflurry import predict
# from mhcflurry import class1_allele_specific

from Levenshtein import hamming
from multiprocessing import Pool, Process


if __name__ == "__main__":
    data = pd.read_csv('output/HLA-A0202.csv', index_col=False)
    print(data.shape)

    binding = data[data["Prediction"] <= 500]
    list2 = []
    def ham_dist_dict(data, dist, line):
        dict_ = dict()
        for i, s_line in enumerate(data['Peptide']):
            result = hamming(line, s_line)
        #    if result <= dist:
        #        dict_[i] = result
        return dict_

    data = binding['Peptide']
    dist = 1
    def ham_for_map(line):
        print (line)
        def hamming_(line_):
            r = hamming(line, line_)
            if r <=dist:
                return (line, line_, r)
        return list(map(hamming_, data))


    # pool = Pool(processes=2) 
    # pep_list = tqdm(binding['Peptide'])
    res = list(map(ham_for_map, data))
    print("Finished! Res contains some : {}".format(res[0]))
    # for line in tqdm(binding['Peptide']):
    # #     result = pool.apply_async(ham_dist_dict, (binding, 1, line,)).get()
    #     result = ham_dist_dict(binding, 1, line)
    # #     result = ham_dist_dict(binding, 1, line)
    # #    list2.append(result)

    # pool.close()
    # pool.join()

    # for i, line in enumerate(result):
    #     print(line)
    #     if i == 1:
    #         break
