#!/bin/sh


splitfile=false

while getopts ":s" opt; do
  case $opt in
    s)
      splitfile=true
      echo "Split option was triggered" >&2
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

cd ../output/

if [ ! -d "tmp/" ]; then
  mkdir tmp/
  splitfile=true
  echo "Split option was inexplicitly triggered" >&2
fi

if [ "$splitfile" == true ]; then
  split -d -l 5000 --additional-suffix=.txt human_peptides.txt tmp/hpeptides_
fi

cd tmp/
parallel --eta netMHCpan -p -a HLA-A02:06 ::: *.txt > ../HLA-A0201_NMP.txt

