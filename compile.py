import yaml
import sys

yaml_path = sys.argv[1]
md_path = sys.argv[2]

rows = []
with open(yaml_path, 'r') as stream:
    yaml_content = yaml.safe_load(stream)
    rows.append(dict(yaml_content))

sep = "<!-- events -->"
headers = ['year', 'name', 'publisher', 'rank', 'core', 'scope', 'short', 'full', 'format', 'cfp', 'country']

markdown_table = "| " + " | ".join(headers) + " |\n"
markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"

for item in rows:
    for val in item.values():
        markdown_table += "| "
        for i in val:
            for k, v in i.items():
                if v is None:
                    v = " "
                if type(v) is int:
                    v = str(v)
                markdown_table += v + " | "
            markdown_table.rstrip()
        markdown_table += "\n"

with open(md_path, "r") as f:
    readme = f.read()

p = readme.split(sep)

p[1] = "\n" + markdown_table + "\n"
new = sep.join(p)

with open("README.md", "w") as f:
    f.write(new)
