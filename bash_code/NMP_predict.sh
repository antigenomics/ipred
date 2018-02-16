#!/bin/sh

usage="$(basename "$0") [-h] [-s] [-a] [-t] [-m] [-k] -- a program to run the netMHCpan in parallel

where:
    -h  show this help text
    -s  split file into 5000 line chunks
    -a  set \"-a\" argument in netMHCpan (default: HLA-A02:01)
    -t  do not delete temporary files
    -m  use it on mihuge server
    -k  the length of k-mers"

splitfile=false
HLA="HLA-A02:01"
mihuge=false
deletetemp=true
kmers=9

while getopts hmk:sa:t opt; do
  case $opt in
    h) echo "$usage"
       exit
       ;;
    m)
      mihuge=true
      echo " Script will run under mihuge server" >&2
      ;;
    k)
      kmers=$OPTARG
      echo " The length of k-mers has been set to $kmers" >&2
      ;;
    s)
      splitfile=true
      echo " Split option has been triggered" >&2
      ;;
    a)
      HLA=$OPTARG
      echo " \"-a\" argument of netMHCpan has been set to $HLA" >&2
      ;;
    t)
      deletetemp=false
      echo " Temporary files will not be deleted" >&2
      ;;
    \?)
      echo " Invalid option: -$OPTARG" >&2
      ;;
  esac
done

cd ../output/

# Makes new tmp/ directory if needed. If there is no tmp/ directory, it is supposed that the human peptide file hasn't been processed yet and splitfile will be set to true inexplicitly to process it, even if it was not passed via shell explicitly.

if [ ! -d "tmp/" ]; then
  mkdir tmp/
  splitfile=true
  echo "Split option was inexplicitly triggered" >&2
fi

# All splitted files are stored in tmp/ directory.

if [ "$splitfile" == true ]; then
  split -d -l 5000 --additional-suffix=.txt k-mers/human_peptides_"$kmers"mers.txt tmp/hpeptides_"$kmers"mers_
fi

# Parallel is used to increase the computational speed.

cd tmp/
echo "$HLA binding prediction"
if [ "$mihuge" == true ]; then
  parallel --eta --jobs 40 /home/vcvetkov/Tools/netMHCpan-4.0/netMHCpan \
 -p -a "$HLA" -f ::: hpeptides_"$kmers"mers_* > "../netMHCpan/"$HLA"_NMP_tmp1.txt"
else
  parallel --eta netMHCpan -p -a \
 "$HLA" ::: hpeptides_"$kmers"mers_ > "../netMHCpan/"$HLA"_NMP_tmp1.txt"
fi

cd ../netMHCpan/

# A command to delete useless and empty lines from file. 

sed -i '/^ /!d' "$HLA"_NMP_tmp1.txt

# A command to select only specific columns from a file

awk '{ print $2, $3, $13 }' "$HLA"_NMP_tmp1.txt > "$HLA"_NMP_tmp2.txt

# Next command will remove duplicates to get rid of multiple titles
# left after parallel

awk '!a[$0]++' "$HLA"_NMP_tmp2.txt > "$HLA"_NMP_"$kmers"mer_proc.txt

if [ "$deletetemp" == true ]; then
  rm *tmp1.txt
  rm *tmp2.txt
fi

echo " The $HLA peptide binding has been predicted succesfully!"
