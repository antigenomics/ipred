while getopts hl: opt; do
  case $opt in
    h) echo "$usage"
       exit
       ;;
    l)
      length = $OPTARG
      echo "The peptide length has been set to $OPTARG" >&2
      ;;
    \?)
      echo " Invalid option: -$OPTARG" >&2
      ;;
  esac
done

python modules/get_kmers.py "$length"

sort ../output/peptides_raw.txt | uniq > ../output/human_peptides_"$length"mers.txt

echo "$length-mers have been produced"

