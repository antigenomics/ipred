import os
import sys
from tqdm import tqdm, tqdm_notebook, tqdm_pandas
from tqdm import trange
import time
from scipy import stats
from scipy.stats import shapiro
import multiprocessing as mp
from kidera import score_positions, score_sequence
from numba import jit

import pandas as pd
import numpy as np
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt

pdf = pd.read_csv('../output/kidera/hpeptides_9mers_kidera.csv')
idf1 = pd.read_csv('../data/immunogenic_peptides.csv')
idf2 = pd.read_csv('../data/immunogenic_peptides.txt', sep='\t')
idf2 = idf2[idf2['Species']=='Homo']
idf1 = idf1[idf1['Length']==9]
idf2 = idf2[idf2['Peptide'].str.len()==9]
idf1 = idf1.drop(['Epitope Start', 'Epitope End', ' Epitope Source Organism Name', 'Length'], axis=1)
idf2 = idf2.drop(['Species'], axis=1)
idf1.columns = ['Peptide', 'MHC', 'Immunogenicity']
idf1 = idf1.reset_index(drop=True)
idf2 = idf2.reset_index(drop=True)
idf = pd.concat([idf1, idf2], axis=0)
idf.Immunogenicity = idf.Immunogenicity.map({'immunogenic': 1, 'non-immunogenic': 0,
                                             'Positive': 1, 'Negative': 0})
idf1 = idf.Peptide.apply(lambda s: score_sequence(s))
idf = pd.concat([idf, idf1], axis=1)
idf = idf.drop('MHC', axis=1)
features = ["helix.bend.pref", "side.chain.size",\
        "extended.str.pref", "hydrophobicity", "double.bend.pref", "partial.spec.vol",\
        "flat.ext.pref", "occurrence.alpha.reg", "pK.C", "surrounding.hydrop"]
idf.columns = ['Peptide', 'Immunogenicity'] + features
pdf['Immunogenicity'] = 2
pdf = pdf[['Peptide', 'Immunogenicity'] + features]
tdf = pd.concat([idf, pdf], axis=0)

print(idf.shape, pdf.shape, tdf.shape)

noself = tdf[(tdf['Immunogenicity']==0) | (tdf['Immunogenicity']==1)]
noself = noself.reset_index(drop=True)
self = tdf[tdf['Immunogenicity']==2].sample(10000)
self = self.reset_index(drop=True)
tsne_df = pd.concat([self, noself], axis=0)
tsne_df = tsne_df.reset_index(drop=True)
print(noself.shape, self.shape, tsne_df.shape)

cores = mp.cpu_count() #Number of CPU cores on your system
partitions = cores #Define as many partitions as you want

df1 = noself[features]
df2 = pdf[features]
df3 = noself[features].values
df4 = pdf[features].values

@jit
def np_distance(inds):
    return np.linalg.norm(df3[inds[0],:] - df4[inds[1],:])

start = time.time()
dist = []
with mp.Pool(cores) as pool:
    for j in trange(10):
        imres = np.array(pool.map(np_distance, [(j, i) for i in range(len(pdf))]))
#        print("Size is {}".format(sys.getsizeof(imres)))
#        dist.append(imres[np.argpartition(imres, -np.int(len(pdf)*0.05))[-np.int(len(pdf)*0.05):]].mean())
print(time.time() - start)