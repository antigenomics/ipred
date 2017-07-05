from __future__ import print_function

import os
from tqdm import tqdm, tqdm_notebook
from tqdm import trange

import pandas as pd
import numpy as np
import networkx as nx
import seaborn as sns

import matplotlib.pyplot as plt

from Bio import SeqIO

from mhcflurry import predict
from mhcflurry import class1_allele_specific

from Levenshtein import hamming
from multiprocessing import Pool, Process


if __name__ == "__main__":
    data = pd.read_csv('output/HLA-A0201.csv', index_col=False)
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

    pool = Pool(processes=5) 

    for line in tqdm(binding['Peptide']):
    #     result = pool.apply_async(ham_dist_dict, (binding, 1, line,)).get()
        result = pool.apply(ham_dist_dict, (binding, 1, line,))
    #     result = ham_dist_dict(binding, 1, line)
    #    list2.append(result)

    # pool.close()
    # pool.join()

    for i, line in enumerate(result):
        print(line)
        if i == 1:
            break
