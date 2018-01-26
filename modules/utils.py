import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
# from mhcflurry import predict
# from mhcflurry import class1_allele_specific

def coding(col, codeDict):
    colCoded = pd.Series(col, copy=True)
    for key, value in codeDict.items():
        colCoded.replace(key, value, inplace=True)
    return colCoded

def make_predictions(df):
    predictions = pd.DataFrame()
    warning = pd.DataFrame()
    warnings = 0
    warning_loc = []
    for i in range(len(df)):
        try:
            prediction = predict(alleles=df["MHC"].iloc[i:i+1].reset_index(drop=True),
                                       peptides=df["Peptide"].iloc[i:i+1].reset_index(drop=True))
            frame = [predictions, prediction]
            predictions = pd.concat(frame)
        except ValueError:
            warnings += 1
            frame = [warning, df.iloc[i]]
            warning = pd.concat(frame)
            warning_loc.append(i)
    if len(predictions):
        print("Predictions made")
    else:
        print("Something went wrong")
    print("Number of warnings is {}".format(warnings))
    print(warning)
    return predictions, warning_loc

def count_freq(filepath):
    aa = {'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, 'H': 6, 'I': 7,\
      'K': 8, 'L': 9, 'M': 10, 'N': 11, 'P': 12, 'Q': 13, 'R': 14,\
      'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19}
    data = pd.read_csv(filepath, index_col=False, sep=" ")
    binding = data[data.ix[:,2] <= 500]
    freq = np.zeros((20,9))
    for line in binding.ix[:,1]:
        for i, a in enumerate(line):
            try:
                freq[int(aa[a]), i] = freq[aa[a],i]+1
            except KeyError:
                pass
    freq_norm = np.true_divide(freq, 409088)
    freq_norm_r = np.round(freq_norm, 2)
    aa_df = pd.DataFrame(freq_norm_r, index=[i for i in sorted(aa.keys())], columns=np.arange(1,10))
    return aa_df

def plot_freq(aa_df, axes):
#     fig = plt.figure(figsize=(3, 5))
    ax = sns.heatmap(aa_df, ax = axes)
#     plt.show()

def plot_entr(input_df, axes):
    df = pd.DataFrame([stats.entropy(input_df[i], base=2) for i in input_df.columns], columns = ['entropy'])
    df['position'] = input_df.columns
    clrs = ['grey' if x > 3 else 'red' for x in df['entropy']]
#     fig = plt.figure(figsize=(5, 3))
    sns.barplot(data=df, x='position', y='entropy', palette = clrs, ax = axes)