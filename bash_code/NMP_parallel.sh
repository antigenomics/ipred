#!/bin/bash

usage="$(basename "$0") [-h] [-m] [-t] [-n] [-o] [-d] -- a program to run the netMHCpan in parallel

where:
    -h  show this help text
    -m  path to meta file
    -t  do not delete temporary files
    -n  number of cores to use
    -o  original folder
    -d  destination folder"


HLA="HLA-A02:01"
deletetemp=true
folder="./"
destination="./"
ncores="80"
nmp_home="/home/vcvetkov/Projects/ipred/bash_code"

while getopts hm:tn:o:d: opt; do
  case $opt in
    h) echo "$usage"
       exit
       ;;
    m)
	    meta=$OPTARG
	    echo " Metafile $meta "
      ;;
    t)
      deletetemp=false
      echo " Temporary files will not be deleted" >&2
      ;;
    n)
      ncores=$OPTARG
      echo " Script will use $ncores cores "
      ;;
    o)
      folder=$OPTARG
      echo " Script will search the files in $folder folder" >&2
      ;;
    d)
      destination=$OPTARG
      echo " Script will save the results in $destination folder" >&2
      ;;
    \?)
      echo " Invalid option: -$OPTARG" >&2
      ;;
  esac
done

cd $folder

echo "netMHCpan prediction has been started to compute. Reading list of arguments" 
readarray -t arguments < "$meta"

for argument in "${arguments[@]}"; do
  echo "$argument binding prediction has been started to compute" >&2
  if [ ! -d "nmptmp/" ]; then
  	mkdir nmptmp/
    echo "nmptmp/ temporary directory has been created"
  elif [ -d "nmptmp/" ]; then
  	cd nmptmp/
  	rm *
    echo "Temporary directory has been cleared"
  	cd ../
  fi
  
  if [ -e "$argument"* ]; then
    split -d -e -l 5000 --additional-suffix=.txt "$argument"* nmptmp/"$argument"_
    echo "The file for $argument has been splitted"
    bash "$nmp_home/NMP_core.sh" -a "$argument" -n "$ncores" -o "nmptmp/" -d "$destination"  
    echo "Succesfully predicted $argument binding"
    echo "$argument netMHCpan prediction has been completed!" >&2
  elif [ ! -e "$argument"* ]; then
    echo "There is no file for the $argument"
  fi
done