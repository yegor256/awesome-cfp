#!/bin/bash

# Parse YAML file using yq
rows=$(yq e '.events[]' cfp.yml)
echo "$rows"

keys=$(echo rows | jq -r '.[0].event | keys[]')

# Start the Markdown table
markdown_table="|"

# Add the headers to the Markdown table
for key in $keys
do
    markdown_table+=" $key |"
done

markdown_table+="\n|"

# Add the separator line
for key in $keys
do
    markdown_table+=" --- |"
done

# Add the rows to the Markdown table
for row in $(echo $yaml_data | jq -c '.[]')
do
    markdown_table+="\n|"
    for key in $keys
    do
        value=$(echo $row | jq -r ".row.$key")
        markdown_table+=" $value |"
    done
done

# Print the Markdown table
echo -e $markdown_table