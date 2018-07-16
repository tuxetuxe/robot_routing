#!/usr/bin/env bash

sudo docker build -t robot_routing .

for folder in problems/* ; do
  if [[ $folder == *sample ]]; then
    continue
  fi
  if [ -d "$folder" ]; then
    echo "==============================================================================="
    echo "Solving problem in $folder"
    echo "==============================================================================="
    sudo docker run -v $(pwd)/problems:/problems robot_routing $folder/problem.txt $folder/solution.txt
  fi
done
