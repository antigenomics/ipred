#!/bin/bash

usage="$(basename "$0") [-h] [-a] [-t] [-n] [-o] [-d] [-f] -- a program to run the netMHCpan in parallel

where:
    -h  show this help text
    -a  set \"-a\" argument in netMHCpan (default: HLA-A02:01)
    -t  do not delete temporary files
    -n  number of cores to use
    -o  original folder
    -d  destination folder"


HLA="HLA-A02:01"
deletetemp=true
folder="nmptmp/"
destination="./"
ncores="80"
nmp_home="/home/vcvetkov/Projects/ipred/bash_code"
file="$HLA"


while getopts ha:tn:o:d:f: opt; do
  case $opt in
    h) echo "$usage"
       exit
       ;;
    a)
      HLA=$OPTARG
      file="$HLA"
      # echo " \"-a\" argument of netMHCpan has been set to $HLA" >&2
      ;;
    t)
      deletetemp=false
      # echo " Temporary files will not be deleted" >&2
      ;;
    n)
      ncores=$OPTARG
      # echo " Script will use $ncores cores "
      ;;
    o)
      folder=$OPTARG
      # echo " Script will search the files in $folder folder" >&2
      ;;
    d)
      destination=$OPTARG
      # echo " Script will save the results in $destination folder" >&2
      ;;
    f)
      file=$OPTARG
      # echo " $file file prefix has been set" >&2
      ;;
    \?)
      echo " Invalid option: -$OPTARG" >&2
      ;;
  esac
done

# exit when any command fails
# set -e

# Parallel is used to increase the computational speed.

cd "$folder"
echo " Current working directory is $(pwd)"
echo "  $HLA binding prediction started"

i="$(ls -1 | wc -l)"
i="$((i-=1))"

if [ "$i" -eq 0 ]; then
  echo $"   The $folder contains no files to process"
elif [ ! "$i" -eq 0 ]; then
  echo $"   The $folder contains $i files to process"
  parallel --eta --jobs "$ncores" --tmpdir /home/vcvetkov/tmp/ \
   /home/vcvetkov/Tools/netMHCpan-4.0/netMHCpan \
 -p -BA -a "${HLA//\*}" -f ::: "$file"* > "$destination"/"$HLA"_NMP_tmp1.txt
fi

cd "$destination"
echo "    Current working directory is $(pwd)"


# A command to delete useless and empty lines from file. 

sed -i '/^ /!d' "$HLA"_NMP_tmp1.txt

# A command to select only specific columns from a file

awk '{ print $2, $3, $13 }' "$HLA"_NMP_tmp1.txt > "$HLA"_NMP_tmp2.txt

# Next command will remove duplicates to get rid of multiple titles
# left after parallel

awk '!a[$0]++' "$HLA"_NMP_tmp2.txt > "$HLA"_NMP_processed.txt

if [ "$deletetemp" == true ]; then
  rm *tmp1.txt
  rm *tmp2.txt
fi

echo " The $HLA peptide binding has been predicted succesfully!"