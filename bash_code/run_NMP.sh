#!/bin/sh

readarray -t arguments < arguments.txt

for argument in "${arguments[@]}"; do
  {
    echo "$argument"
    bash NMP_predict.sh -m -a $argument && \
    "Succesfully predicted $argument binding" >> NMP_prediction.log
  } || {
    "Failed to predict $argument binding" >> NMP_prediction.log
    echo "Failed to predict $argument binding" >&2
  }
  echo "    $argument netMHCpan prediction has been completed!    " >&2
done

