import yaml
import sys


def generate(yaml_path, md_path):
    rows = []
    with open(yaml_path, 'r') as stream:
        yaml_content = yaml.safe_load(stream)
        rows.append(dict(yaml_content))

    headers = ['name', 'publisher', 'rank', 'core', 'scope', 'short', 'full', 'format', 'cfp', 'country']

    sep = "<!-- events -->"
    markdown_table = "| " + " | ".join(headers) + " |\n"
    markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    for row in rows:
        for key, val in row.items():
            title = key
            markdown_table += "| "
            for i in val:
                for k, v in i.items():
                    if v is None:
                        v = " "
                    if type(v) is not str:
                        v = str(v)
                    if k == "year":
                        title += f"'{v[-2:]}"
                        continue
                    if k == "url":
                        v = f"[{title}](<{v}>)"
                    if k == "core":
                        v = f"<{v}>"
                    markdown_table += v + " | "
                markdown_table.rstrip()
            markdown_table = markdown_table[:-1]
            markdown_table += "\n"

    with open(md_path, "r") as f:
        readme = f.read()

    p = readme.split(sep)

    p[1] = "\n" + markdown_table + "\n"
    new = sep.join(p)

    with open(md_path, "w+") as f:
        f.write(new)


if __name__ == '__main__':
    generate(sys.argv[1], sys.argv[2])
