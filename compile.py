import yaml

li = []
with open('cfp.yml', 'r') as stream:
    yaml_content = yaml.safe_load(stream)
    li.append(dict(yaml_content))

# for x in li:
#    print(x.keys())
#    print(x.values())

headers = ['name', 'publisher', 'CORE', 'Scope', 'Short pages', 'Full pages', 'Format', 'CFP']

# prepare markdown
markdown_table = "| " + " | ".join(headers) + " |\n"
markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"

for x in li:
    for v in x.values():
        markdown_table += "| "
        for i in v:
            for k, v in i.items():
                if v is None:
                    v = " "
                if type(v) is int:
                    v = str(v)
                markdown_table += v + " | "
        markdown_table += "\n"

print(markdown_table)

with open('generated.md', 'w') as markdown_file:
    markdown_file.write(markdown_table)
