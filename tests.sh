#!/bin/bash -e

for dir in fixtures/*
do
  python3 compile.py "$dir/input.yml" "$dir/README.md"
  diff "$dir/expected.md" "$dir/README.md"
  if [ $? -eq 0 ]; then
    echo "Test passed for $dir"
  else
    echo "Test failed for $dir"
  fi
done
