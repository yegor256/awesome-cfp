#!/bin/bash

for dir in fixtures/*
do
  mkdir temp
  python3 compile.py "$dir/input.yml" "$dir/README.md"
  diff "$dir/expected.md" "$dir/README.md"
  if [ $? -eq 0 ]; then
    echo "Test passed for $dir"
  else
    echo "Test failed for $dir"
  fi
  rm "$dir/README.md"
done
