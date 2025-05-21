# SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
# SPDX-License-Identifier: MIT

# flake8: noqa: WPS202

import datetime
import sys
from pathlib import Path
from typing import Literal, TypeAlias, TypedDict
from copy import deepcopy

import httpx
import yaml


class InvalidUrlError(Exception):
    """Exception thrown on fail ping url."""


class ExpiredCfpError(Exception):
    """Exception thrown on call for papers date expired."""


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

    >>> build_name('ABC', {'year': '2099', 'url': 'https://google.com', 'later': False})
    "[ABC'99](<https://google.com>)"
    >>> build_name('ABC', {'year': 2099, 'url': 'https://google.com', 'later': False})
    "[ABC'99](<https://google.com>)"
    """
    year_last_two_digit = str(conf_info["year"])[-2:]
    return "[{0}'{1}](<{2}>)".format(
        conf_name,
        year_last_two_digit,
        validate_url(conf_info["url"]) if not conf_info["later"] else conf_info["url"],
    )


def date_actual(date: datetime.date) -> datetime.date:
    today = datetime.datetime.now(tz=datetime.UTC).date()
    if date > today:
        return date
    raise ExpiredCfpError("{0} expired for today {1}".format(date, today))


def render_date(raw_date: RawDateT | None):
    """Render date.

    >>> render_date("2090-01-01")
    '90-Jan'
    >>> render_date("closed")
    'closed'
    >>> render_date(None)
    ''
    """
    if not raw_date:
        return ""
    if raw_date == "closed":
        return "closed"
    parsed_date = datetime.datetime.strptime(raw_date, "%Y-%m-%d").date()
    return parsed_date.strftime("%y-%b")


def build_row(conf_name: str, conf_info: list[dict], markdown_table_row_template: str):
    return markdown_table_row_template.format(
        name=build_name(conf_name, conf_info),
        publisher=conf_info["publisher"] or "",
        rank="[{0}](<{1}>)".format(
            conf_info["rank"],
            validate_url(conf_info["core"]) if not conf_info["later"] else conf_info["url"],
        ),
        scope=conf_info["scope"],
        short=conf_info["short"] or "",
        full=conf_info["full"] or "",
        format=conf_info["format"] or "",
        cfp=render_date(conf_info["cfp"]),
        country=conf_info["country"],
    )


def md_rows(yaml_as_dict: dict[str, ConfInfoDict], markdown_table_row_template: str):
    sorting_dict = {char: idx for idx, char in enumerate(["A*", "A", "B", "C", "D", "E", "F"])}
    return [
        build_row(conf_name, conf_info, markdown_table_row_template)
        for conf_name, conf_info in sorted(
            yaml_as_dict.items(),
            key=lambda x: sorting_dict[x[1]["rank"]]
        )
    ]


def validate_url(url: str) -> str:
    response = httpx.get(url)
    status_success = httpx.codes.is_success(response.status_code)
    allow_status = status_success or httpx.codes.is_redirect(response.status_code)
    if not allow_status:
        raise InvalidUrlError("Url = '{0}' return status = {1}".format(url, response.status_code))
    return url


def mark_expired_dates(yaml_path: str):
    yaml_content = Path(yaml_path).read_text()
    origin_yaml = yaml.safe_load(yaml_content)
    updated_yaml = deepcopy(origin_yaml)
    for conf_name, conf_info in yaml.safe_load(yaml_content).items():
        if not conf_info["cfp"] or conf_info["cfp"] == "closed":
            continue
        try:
            date_actual(
                datetime.datetime.strptime(conf_info["cfp"], "%Y-%m-%d").date(),
            )
        except ExpiredCfpError:
            updated_yaml[conf_name]["cfp"] = "closed"
    write_yaml_file(yaml_path, updated_yaml)


def write_yaml_file(path, yaml_structure):
    yaml_content = Path(path).read_text()
    weights = {
        name: idx
        for idx, name in enumerate([
            "year",
            "url",
            "publisher",
            "rank",
            "core",
            "scope",
            "short",
            "full",
            "format",
            "cfp",
            "country",
            "later",
        ])
    }
    sorted_records = []
    for name, record in yaml_structure.items():
        dumped_str = yaml.safe_dump({name: record})
        record_lines = dumped_str.splitlines()[1::]
        sorted_record_lines = sorted(
            record_lines,
            key=lambda record_line: weights[record_line.strip().split(":")[0]]
        )
        sorted_records.append(
            "{0}\n{1}\n".format(
                dumped_str.splitlines()[0],
                "\n".join(sorted_record_lines),
            ),
        )
    Path(path).write_text(
        "{0}---\n{1}".format(
            yaml_content.split("---")[0],
            "\n".join(sorted_records)
        ),
    )


def generate(yaml_path, md_path):
    mark_expired_dates(yaml_path)
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
    split_md = Path(md_path).read_text().split(sep)
    split_md[1] = "\n{0}\n\n".format("\n".join(markdown_table_rows))
    Path(md_path).write_text(sep.join(split_md))


if __name__ == "__main__":
    generate(sys.argv[1], sys.argv[2])  # pragma: no cover
