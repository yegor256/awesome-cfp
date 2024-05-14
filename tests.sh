#!/bin/bash

for dir in fixtures/*
do
  mkdir temp
  cp "$dir/input.yml" temp/cfp.yml
  cp "$dir/input.md" temp/README.md
  python3 compile.py temp/cfp.yml temp/README.md
  diff "$dir/expected.md" temp/README.md
  if [ $? -eq 0 ]; then
    echo "Test passed for $dir"
  else
    echo "Test failed for $dir"
  fi
  rm -rf temp
done