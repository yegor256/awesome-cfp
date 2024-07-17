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

import sys
from pathlib import Path

import yaml


def generate(yaml_path, md_path):
    yaml_content = yaml.safe_load(Path(yaml_path).read_text())
    headers = ["name", "publisher", "rank", "scope", "short", "full", "format", "cfp", "country"]
    sep = "<!-- events -->"
    markdown_table = "| {0} |\n".format(" | ".join(headers))
    markdown_table += "| {0} |\n".format(" | ".join(["---"] * len(headers)))
    for key, val in yaml_content.items():
        title = key
        markdown_table += "| "
        for i in val:
            for k, v in i.items():
                if v is None:
                    v = " "
                if not isinstance(v, str):
                    v = str(v)
                if k == "year":
                    title += "'{0}".format(v[-2:])
                    continue
                if k == "url":
                    v = "[{0}](<{1}>)".format(title, v)
                if k == "rank":
                    rank = v
                    continue
                if k == "core":
                    v = "[{0}](<{1}>)".format(rank, v)
                markdown_table += v + " | "
            markdown_table.rstrip()
        markdown_table = markdown_table[:-1]
        markdown_table += "\n"
    readme = Path(md_path).read_text()
    p = readme.split(sep)
    p[1] = "\n" + markdown_table + "\n"
    new = sep.join(p)
    Path(md_path).write_text(new)


if __name__ == '__main__':
    generate(sys.argv[1], sys.argv[2])
