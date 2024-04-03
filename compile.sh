#!/bin/bash

# Check if yq is installed
if ! command -v yq &> /dev/null
then
    echo "yq could not be found. Please install it using 'pip install yq'"
    exit
fi

# Read the YAML file
yaml_data=$(yq r $1)

# Extract the keys from the YAML data
keys=$(echo $yaml_data | jq -r '.[0].row | keys[]')

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