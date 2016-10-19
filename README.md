# Antigen immunogenicity prediction - purifying selection point of view

Current workflow includes the following steps:

- The MHC(s) that are likely to present a given peptide is either specified by user or deduced using third-party MHC binding prediction framework
- A pool of self-peptides presented by the same MHC is deduced
- Certain characterstics of this pool (diversity, entropy, amino acid properties) are computed
- The set of self-peptide similar to selected antigen is deduced
- These characteristics together with amino acid properties of chosen antigen are used by the classifier to quantify the likelihood of a given peptide being immunogenic

The workflow can be fine-tuned by manually specifying the set of MHCs of an individual/animal and its reference genome together with allelic variants that affect protein-coding regions.



