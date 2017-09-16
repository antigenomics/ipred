all=false
while getopts hl:a opt; do
  case $opt in
    h) echo "$usage"
       exit
       ;;
    l)
      length=$OPTARG
      echo "The peptide length has been set to $OPTARG" >&2
      ;;
    a)
      all=true
      ;;
    \?)
      echo " Invalid option: -$OPTARG" >&2
      ;;
  esac
done

if [ "$all" == false ]; then
  echo "Getting $length-mers"
  python ../modules/get_kmers.py -l "$length"
  sort ../output/peptides_raw.txt | \
   uniq > ../output/human_peptides_"$length"mers.txt
  echo "$length-mers have been produced"
else
  for len in 10 11 12 13 14 15
  do
    echo "Getting $len-mers"
    python ../modules/get_kmers.py -l "$len"
    sort ../output/peptides_raw.txt | \
     uniq > ../output/human_peptides_"$len"mers.txt
    echo "$len-mers have been produced"
  done
fi
