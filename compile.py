import yaml

li = []
with open('cfp.yml', 'r') as stream:
    yaml_content = yaml.safe_load(stream)
    li.append(dict(yaml_content))

for x in li:
    print(x.keys())
    print(x.values())

headers = ['name', 'publisher', 'CORE', 'Scope', 'Short pages', 'Full pages', 'Format', 'CFP']

# prepare markdown
markdown_table = "| " + " | ".join(headers) + " |\n"
markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
print(markdown_table)

with open('generated.md', 'w') as markdown_file:
    markdown_file.write(markdown_table)
