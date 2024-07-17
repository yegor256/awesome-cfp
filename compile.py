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

import datetime
import sys
from pathlib import Path
from typing import Literal, TypeAlias, TypedDict

import yaml

DateAsStrT: TypeAlias = str
RawDateT: TypeAlias = DateAsStrT | Literal["closed"]


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


def build_name(conf_name: str, conf_info: ConfInfoDict) -> str:
    """Build name.

    >>> build_name('ABC', {'year': '2099', 'url': 'https://google.com'})
    "[ABC'99](<https://google.com>)"
    >>> build_name('ABC', {'year': 2099, 'url': 'https://google.com'})
    "[ABC'99](<https://google.com>)"
    """
    year_last_two_digit = str(conf_info["year"])[-2:]
    return "[{0}'{1}](<{2}>)".format(conf_name, year_last_two_digit, conf_info["url"])


def render_date(raw_date: RawDateT):
    """Render date.

    >>> render_date("2020-01-01")
    '20-Jan'
    >>> render_date("closed")
    'closed'
    """
    if raw_date == "closed":
        return "closed"
    return datetime.datetime.strptime(raw_date, "%Y-%m-%d").strftime("%y-%b")


def build_row(conf_name: str, conf_info: list[dict], markdown_table_row_template: str):
    conf_info_dict = {}
    for row in conf_info:
        row_key = next(iter(row.keys()))
        row_value = next(iter(row.values()))
        conf_info_dict[row_key] = row_value
    return markdown_table_row_template.format(
        name=build_name(conf_name, conf_info_dict),
        publisher=conf_info_dict["publisher"],
        rank="[{0}](<{1}>)".format(conf_info_dict["rank"], conf_info_dict["core"]),
        scope=conf_info_dict["scope"],
        short=conf_info_dict["short"],
        full=conf_info_dict["full"],
        format=conf_info_dict["format"],
        cfp=render_date(conf_info_dict["cfp"]),
        country=conf_info_dict["country"],
    )


def md_rows(yaml_as_dict: dict[str, ConfInfoDict], markdown_table_row_template: str):
    return [
        build_row(conf_name, conf_info, markdown_table_row_template)
        for conf_name, conf_info in yaml_as_dict.items()
    ]


def generate(yaml_path, md_path):
    headers = ["name", "publisher", "rank", "scope", "short", "full", "format", "cfp", "country"]
    markdown_table_row_template = "".join([
        "| {name} ",
        "| {publisher} ",
        "| {rank} ",
        "| {scope} ",
        "| {short} ",
        "| {full} ",
        "| {format} ",
        "| {cfp} ",
        "| {country} |",
    ])
    markdown_table_rows = ["| {0} |".format(" | ".join(headers))]
    markdown_table_rows.append(
        "| {0} |".format(
            " | ".join(["---" for _ in range(len(headers))]),
        ),
    )
    markdown_table_rows.extend(
        md_rows(
            yaml.safe_load(Path(yaml_path).read_text()),
            markdown_table_row_template,
        ),
    )
    sep = "<!-- events -->"
    splitted_md = Path(md_path).read_text().split(sep)
    splitted_md[1] = "\n{0}\n\n".format("\n".join(markdown_table_rows))
    Path(md_path).write_text(sep.join(splitted_md))


if __name__ == "__main__":
    generate(sys.argv[1], sys.argv[2])
