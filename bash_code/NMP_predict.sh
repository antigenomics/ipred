#!/bin/sh

usage="$(basename "$0") [-h] [-s] [-a] [-t] [-m] -- a program to run the netMHCpan in parallel

where:
    -h  show this help text
    -s  split file into 5000 line chunks
    -a  set \"-a\" argument in netMHCpan (default: HLA-A02:01)
    -t  do not delete temporary files
    -m  use it on mihuge server"

splitfile=false
HLA="HLA-A02:01"
mihuge=false
deletetemp=true

while getopts ":hsa:" opt; do
  case $opt in
    h) echo "$usage"
       exit
       ;;
    s)
      splitfile=true
      echo " Split option was triggered" >&2
      ;;
    a)
      HLA=$OPTARG
      echo " \"-a\" argument of netMHCpan was set to $HLA"  >&2
      ;;
    t)
      deletetemp=false
      echo "Temporary files will not be deleted"
      ;;
    m)
      mihuge=true
      echo " Script runs under mihuge server"
      ;;
    \?)
      echo " Invalid option: -$OPTARG" >&2
      ;;
  esac
done

cd ../output/

# Makes new tmp/ directory if needed.
# If there is no tmp/ directory, it is supposed that the human petide
# file hasn't been processed yet and splitfile sets to true inexplicitly
# to process it, even if it was not passed via shell explicitly.

if [ ! -d "tmp/" ]; then
  mkdir tmp/
  splitfile=true
  echo "Split option was inexplicitly triggered" >&2
fi

# All splitted files are stored in tmp/ directory.

if [ "$splitfile" == true ]; then
  split -d -l 5000 --additional-suffix=.txt human_peptides.txt tmp/hpeptides_
fi

# Parallel is used to increase the computational speed.

cd tmp/
if [ "$mihuge"==true ]
then
  parallel --eta /home/vcvetkov/Tools/netMHCpan-3.0/bin/netMHCpan \
 -p -expfix -a "$HLA" ::: *.txt > "../"$HLA"_NMP_tmp1.txt"
else
  parallel --eta netMHCpan -p -expfix -a "$HLA" ::: *.txt > "../"$HLA"_NMP_tmp1.txt"
fi

# Python script for some reason creates empty lines

cd ../
python ../modules/NMP_process.py -f "$HLA"_NMP_tmp1.txt > "$HLA"_NMP_tmp2.txt

# A command to delete empty lines from file. 
# d is the sed command to delete a line. ^$ is a regular expression matching
# only a blank line, a line start followed by a line end.

sed -i '/^$/d' "$HLA"_NMP_tmp2.txt

# A command to select only specific columns from a file

awk '{ print $2 $3 $12 }' "$HLA"_NMP_tmp2.txt > "$HLA"_NMP_proc.txt

if [ "$deletetemp"==true ]
then
  rm *tmp1.txt
  rm *tmp2.txt
fi

echo " The $HLA peptide binding has been predicted succesfully!"
