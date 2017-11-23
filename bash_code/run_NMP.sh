#!/bin/sh
echo "netMHCpan prediction has been started to compute. Reading list of arguments" \
 | tee NMP_prediction.log
readarray -t arguments < new_arguments.txt

for argument in "${arguments[@]}"; do
  echo "$argument binding prediction has been started to compute" >&2
  bash NMP_predict.sh -m -a $argument
  echo "Succesfully predicted $argument binding" | tee NMP_prediction.log
  echo "    $argument netMHCpan prediction has been completed!    " >&2
done

