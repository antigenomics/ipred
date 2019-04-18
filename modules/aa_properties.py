import pandas
import warnings
import os
path, _ = os.path.split(__file__)
kidera_factors = pandas.read_csv(os.path.join(path, 'kidera.csv'),
                                 header=None,
                                 index_col=0)
aa_properties = pandas.read_csv(os.path.join(path, 'aa_property_table.csv'),
                                 header=0,
                                 index_col=0)
aa_hydrophobicity = pandas.read_csv(os.path.join(path, 'hydrophobicity.csv'))
symbol_lookup = { 'ALA': 'A', 'ARG': 'R',
                  'ASN': 'N', 'ASP': 'D',
                  'CYS': 'C', 'GLN': 'Q',
                  'GLU': 'E', 'GLY': 'G',
                  'HIS': 'H', 'ILE': 'I',
                  'LEU': 'L', 'LYS': 'K',
                  'MET': 'M', 'PHE': 'F',
                  'PRO': 'P', 'SER': 'S',
                  'THR': 'T', 'TRP': 'W',
                  'TYR': 'Y', 'VAL': 'V' }

kidera_factors.index = kidera_factors.index \
                                     .map(lambda x: symbol_lookup[x])
aa_properties.index = aa_properties.index \
                                     .map(lambda x: symbol_lookup[x])
aa_hydrophobicity = aa_hydrophobicity.set_index('aa', drop=True)


def score_positions(sequence):
    warnings.warn(
            "score_positions will be removed",
            DeprecationWarning
        )
    return kidera_factors.loc[list(sequence)]

def score_sequence(sequence, norm=False):
    warnings.warn(
            "score_sequence will be removed",
            DeprecationWarning
        )
    if norm:
        return kidera_factors.loc[list(sequence)].sum() / len(sequence)
    else:
        return kidera_factors.loc[list(sequence)].sum()

def alprop_sequence(sequence, norm=False):
    if norm:
        return aa_properties.loc[list(sequence)].sum() / len(sequence)
    else:
        return aa_properties.loc[list(sequence)].sum()

def score_hydrophobicity_sequence(sequence, scale="Kyte-Doolittle", norm=False):
    """
    Scores hydrophobicity of amino acids with different scales from
    http://resources.qiagenbioinformatics.com/manuals/clcgenomicsworkbench/650/Hydrophobicity_scales.html
    :param sequence: your sequence
    :param scale: One of the following scales:
        Kyte-Doolittle  Hopp-Woods  Cornette  Eisenberg   Rose  Janin   Engelman GES
    :param norm: if False returns sum, else mean of the hydrophobicity scores
    :return: score
    """
    if norm:
        return aa_hydrophobicity.loc[list(sequence), scale].sum() / len(sequence)
    else:
        return aa_hydrophobicity.loc[list(sequence), scale].sum()