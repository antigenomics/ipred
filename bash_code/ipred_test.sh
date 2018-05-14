#!/bin/bash

while getopts hf:a opt; do
  case $opt in
    h) echo "$usage"
       exit
       ;;
    f)
      file=$OPTARG
      echo "The temp file is: $OPTARG" >&2
      ;;
    a)
      all=true
      ;;
    \?)
      echo " Invalid option: -$OPTARG" >&2
      ;;
  esac
done

echo "$(pwd)"
cat "$file" | head > file.out