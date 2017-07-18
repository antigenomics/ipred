#!/bin/sh

usage="$(basename "$0") [-h] [-s n] -- a programme to run the netMHCpan in parallel

where:
    -h  show this help text
    -s  split file into 5000 line chunks
    -a  set \"-a\" argument in netMHCpan (default: HLA-A02:01)"

splitfile=false
HLA="HLA-A02:01"

while getopts ":hsa:" opt; do
  case $opt in
    h) echo "$usage"
       exit
       ;;
    s)
      splitfile=true
      echo "Split option was triggered" >&2
      ;;
    a)
      HLA=$OPTARG
      echo " \"-a\" argument of netMHCpan was set to " "$HLA"  >&2
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

cd ../output/

# Make new tmp/ directory if needed.
# If there is no tmp/ directory it is supposed that file hasn't been processed yet,
# and splitfile sets to true inexplicitly to process it, even if it was not passed
# via shell explicitly.

if [ ! -d "tmp/" ]; then
  mkdir tmp/
  splitfile=true
  echo "Split option was inexplicitly triggered" >&2
fi

# All generated files are stored in tmp/ directory.

if [ "$splitfile" == true ]; then
  split -d -l 5000 --additional-suffix=.txt human_peptides.txt tmp/hpeptides_
fi

# Parallel is used to increase the computational speed.

cd tmp/
parallel --eta netMHCpan -p -a "$HLA" ::: *.txt > ../HLA-A0201_NMP.txt

