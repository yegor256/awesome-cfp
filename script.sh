#!/bin/bash

# Load YAML file
yaml_content=$(yq eval -o=json cfp.yml)

# Convert JSON to array
li=("$yaml_content")

# Print keys and values
for x in "${li[@]}"; do
    echo $(echo $x | jq 'keys')
    echo $(echo $x | jq 'values')
done

# Define headers
headers=('Name' 'Publisher' 'CORE' 'Scope' 'Short pages' 'Full pages' 'Format' 'CFP')

# Prepare markdown
markdown_table="| "
for header in "${headers[@]}"; do
    markdown_table+="$header | "
done
markdown_table+="\n| "
for header in "${headers[@]}"; do
    markdown_table+="--- | "
done
markdown_table+="\n"

echo $markdown_table

# Write to markdown file
echo -e $markdown_table > generated.md