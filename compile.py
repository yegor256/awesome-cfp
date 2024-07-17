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
from typing import TypedDict

import yaml


class ConfInfoDict(TypedDict):

    name: str
    year: str
    url: str
    publisher: str
    rank: str
    core: str
    scope: str
    short: str
    full: str
    format: str
    cfp: str
    country: str


def _build_name(conf_name: str, conf_info: ConfInfoDict) -> str:
    """Build name.
    
    >>> _build_name('ABC', {'year': '2099', 'url': 'https://google.com'})
    "[ABC'99](https://google.com)"
    >>> _build_name('ABC', {'url': 'https://google.com'})
    '[ABC](https://google.com)'
    """
    year_last_two_digit = conf_info["year"][-2:]
    return "[{0}'{1}](<{2}>)".format(conf_name, year_last_two_digit, conf_info["url"])


def generate(yaml_path, md_path):
    yaml_content = yaml.safe_load(Path(yaml_path).read_text())
    headers = ["name", "publisher", "rank", "scope", "short", "full", "format", "cfp", "country"]
    sep = "<!-- events -->"
    markdown_table_row_template = "".join([
        "| {name} ",
        "| {publisher} ",
        "| {rank} ",
        "| {scope} ",
        "| {short} ",
        "| {full} ",
        "| {format} ",
        "| {cfp} ",
        "| {country} |\n"
    ])
    markdown_table_rows = ["| {0} |".format(" | ".join(headers))]
    markdown_table_rows.append("| {0} |".format(" | ".join(["---"] * len(headers))))
    for conf_name, conf_info in yaml_content.items():
        conf_info_dict = {}
        for row in conf_info:
            conf_info_dict[next(iter(row.keys()))] = next(iter(row.values()))
        markdown_table_rows.append(
            markdown_table_row_template.format(
                name=_build_name(conf_name, conf_info_dict),
                publisher=conf_info_dict["publisher"],
                rank="[{0}](<{1}>)".format(conf_info_dict["rank"], conf_info_dict["core"]),
                scope=conf_info_dict["scope"],
                short=conf_info_dict["short"],
                full=conf_info_dict["full"],
                format=conf_info_dict["format"],
                cfp=conf_info_dict["cfp"],
                country=conf_info_dict["country"],
            )
        )
    readme = Path(md_path).read_text()
    p = readme.split(sep)
    p[1] = "\n" + "\n".join(markdown_table_rows) + "\n"
    new = sep.join(p)
    Path(md_path).write_text(new)


if __name__ == '__main__':
    generate(sys.argv[1], sys.argv[2])
