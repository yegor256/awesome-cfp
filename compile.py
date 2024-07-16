# MIT License
#
# Copyright (c) 2024 Yegor Bugayenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import yaml
import sys


def generate(yaml_path, md_path):
    rows = []
    with open(yaml_path, 'r') as stream:
        yaml_content = yaml.safe_load(stream)
        rows.append(dict(yaml_content))

    headers = ['name', 'publisher', 'rank', 'scope', 'short', 'full', 'format', 'cfp', 'country']

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
                    if not isinstance(v, str):
                        v = str(v)
                    if k == "year":
                        title += f"'{v[-2:]}"
                        continue
                    if k == "url":
                        v = f"[{title}](<{v}>)"
                    if k == "rank":
                        rank = v
                        continue
                    if k == "core":
                        v = f"[{rank}](<{v}>)"
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
