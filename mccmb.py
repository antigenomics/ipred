import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


from multiprocessing import Pool, Process

import itertools
from modules.aa_properties import score_hydrophobicity_sequence, score_positions, score_sequence

from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import roc_curve, auc, classification_report
from sklearn.model_selection import RandomizedSearchCV

from joblib import dump, load

import warnings
warnings.filterwarnings('ignore')

aa =   ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']
ignore = ["*", "U", "X"]
viruses = ['CMV_StrainAD169', 'YFV_Strain17D', 'HIV-1_StrainHXB2', 'HCV_StrainIsolateH', 'EBV_StrainAG876']
bacteria = ['SHGLsonnei', 'SLMLenteritidis', 'MYPLpneumoniae', 'MYBTsmegmatis', 'SLMLtyphimurium', 
            'YERSpseudotuberculosis', 'YERSenterocolitica', 'CLMDtrachomatis', 'MYPLsynoviae', 'KLEBpneumoniae',
            'CPBTjejuni', 'SHGLflexneri', 'CLOSdificile']
kidera = ["helix.bend.pref", "side.chain.size",
           "extended.str.pref", "hydrophobicity", "double.bend.pref", "partial.spec.vol",
           "flat.ext.pref", "occurrence.alpha.reg", "pK.C", "surrounding.hydrop"]
fts = ['ft1', 'ft2', 'ft3', 'ft4', 'ft5']

cdf = pd.read_csv('data/chowell.csv')
cdf = cdf[['peptide', 'Immunogenicity']]
cdf.Immunogenicity = cdf.Immunogenicity.map({'Positive':1,'Negative':0})

factors = pd.read_csv("modules/NewAAFactors.csv", index_col=0)

def score_factors(sequence, norm=False):
    if norm:
        return factors.loc[list(sequence)].sum() / len(sequence)
    else:
        return factors.loc[list(sequence)].sum()
    
adf = pd.concat([
        cdf,
        cdf.peptide.apply(lambda s: score_factors(s)),
        cdf.peptide.apply(lambda s: score_sequence(s))
    ], axis=1)

adf.columns = ['peptide', 'Immunogenicity'] + fts + kidera
X_train, X_test, y_train, y_test = train_test_split(adf[fts+kidera].values, adf.Immunogenicity, test_size=.25)
clf = RandomForestClassifier(n_estimators=400)

# scores = cross_val_score(clf, X=X_train, y=y_train, cv=5)
clf.fit(X_train, y_train);

dump(clf, "mccmbclf.jl")

probs = clf.predict_proba(X_test)
preds = probs[:,1]
fpr, tpr, threshold = roc_curve(y_test, preds)
roc_auc = auc(fpr, tpr)


fig, ax = plt.subplots(figsize=(8, 6))
plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
fig.set_dpi(300)
plt.savefig("mccmbclfres.png", bbox_inches='tight', pad_inches=0)
