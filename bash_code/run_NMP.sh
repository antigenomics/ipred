#!/bin/bash

mapfile -t arguments < arguments.txt
for argument in $arguments; do
  {
    bash NMP_predict.sh -t -m -a $argument && \
    "Succesfully predicted $argument binding" >> NMP_prediction.log
  } || {
    "Failed to predict $argument binding" >> NMP_prediction.log
  }
  echo "    $argument netMHCpan prediction has been completed!    " >&2
done

