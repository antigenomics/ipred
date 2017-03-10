import pandas as pd
from mhcflurry import predict
from mhcflurry import class1_allele_specific

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