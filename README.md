## Antigen immunogenicity prediction - purifying selection point of view

Current workflow includes the following steps:

- The MHC(s) that are likely to present a given antigen is either specified by user or deduced using third-party MHC binding prediction framework
- A pool of self-peptides presented by the same MHC is deduced
- Certain characterstics of this pool (diversity, entropy, amino acid properties) are computed
- The set of self-peptide similar to selected antigen is deduced
- These characteristics together with amino acid properties of chosen antigen are used by the classifier to quantify the likelihood of a given peptide being immunogenic

Note that MHC anchor points are excluded when computing peptide similarity as well as features fo self-peptide pool. MHC anchor points are also deduced for antigen of interest.

The workflow can be fine-tuned by manually specifying the set of MHCs of an individual/animal and its reference genome together with allelic variants that affect protein-coding regions.


### Planned side features

- Generate list of presented peptides for specified HLA allele list and basic genomic data (e.g. genome fasta files + GTF file with exons)

### References to 3rd party code

- NetMHCPan - http://www.cbs.dtu.dk/services/NetMHCpan/ won't bother obtaining so far - don't have .edu mail
- MHC binding prediction by Hammerbacher et al https://github.com/hammerlab/mhcflurry
- + some useful tools https://github.com/hammerlab/mhctools
- A pipeline similar to what we plan to develop - https://github.com/ambj/MuPeXI 
