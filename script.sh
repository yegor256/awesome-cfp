#!/bin/bash

# Parse YAML file using yq
rows=$( yq 'to_entries' cfp.yml)
echo "$rows"
