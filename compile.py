# SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
# SPDX-License-Identifier: MIT

import datetime
import sys
from pathlib import Path
from typing import Literal, TypeAlias, TypedDict
from copy import deepcopy

import httpx
import yaml


class InvalidUrlError(Exception):
    """Exception threw on fail ping url."""


class ExpiredCfpError(Exception):
    """Exception threw on call for papers date expired."""


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


def build_name(name: str, info: ConfInfoDict) -> str:
    """Build name.

    >>> build_name('ABC', {'year': '2099', 'url': 'https://google.com', 'later': False})
    "[ABC'99](<https://google.com>)"
    >>> build_name('ABC', {'year': 2099, 'url': 'https://google.com', 'later': False})
    "[ABC'99](<https://google.com>)"
    """
    year = str(info["year"])[-2:]
    return "[{0}'{1}](<{2}>)".format(
        name,
        year,
        validate_url(info["url"]) if not info["later"] else info["url"],
    )


def date_actual(date: datetime.date) -> datetime.date:
    today = datetime.datetime.now(tz=datetime.UTC).date()
    if date > today:
        return date
    raise ExpiredCfpError("{0} expired for today {1}".format(date, today))


def render_date(date: RawDateT | None):
    """Render date.

    >>> render_date("2090-01-01")
    '90-Jan'
    >>> render_date("closed")
    'closed'
    >>> render_date(None)
    ''
    """
    if not date:
        return ""
    if date == "closed":
        return "closed"
    parsed = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    return parsed.strftime("%y-%b")


def build_row(name: str, info: list[dict], template: str):
    return template.format(
        name=build_name(name, info),
        publisher=info["publisher"] or "",
        rank="[{0}](<{1}>)".format(
            info["rank"],
            validate_url(info["core"]) if not info["later"] else info["url"],
        ),
        scope=info["scope"],
        short=info["short"] or "",
        full=info["full"] or "",
        format=info["format"] or "",
        cfp=render_date(info["cfp"]),
        country=info["country"],
    )


def md_rows(yml: dict[str, ConfInfoDict], template: str):
    srtd = {char: idx for idx, char in enumerate(["A*", "A", "B", "C", "D", "E", "F"])}
    return [
        build_row(name, info, template)
        for name, info in sorted(
            yml.items(),
            key=lambda x: srtd[x[1]["rank"]]
        )
    ]


def validate_url(url: str) -> str:
    response = httpx.get(url)
    success = httpx.codes.is_success(response.status_code)
    allow = success or httpx.codes.is_redirect(response.status_code)
    if not allow:
        raise InvalidUrlError("Url = '{0}' return status = {1}".format(url, response.status_code))
    return url


def mark_expired_dates(path: str):
    yml = Path(path).read_text()
    origin = yaml.safe_load(yml)
    updated = deepcopy(origin)
    for name, info in yaml.safe_load(yml).items():
        if not info["cfp"] or info["cfp"] == "closed":
            continue
        try:
            date_actual(
                datetime.datetime.strptime(info["cfp"], "%Y-%m-%d").date(),
            )
        except ExpiredCfpError:
            updated[name]["cfp"] = "closed"
    write_yaml_file(path, updated)


def write_yaml_file(path, yml):
    content = Path(path).read_text()
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
    records = []
    for name, record in yml.items():
        dumped = yaml.safe_dump({name: record})
        lines = sorted(
            dumped.splitlines()[1::],
            key=lambda line: weights[line.strip().split(":")[0]]
        )
        records.append(
            "{0}\n{1}\n".format(
                dumped.splitlines()[0],
                "\n".join(lines),
            ),
        )
    Path(path).write_text(
        "{0}---\n{1}".format(
            content.split("---")[0],
            "\n".join(records)
        ),
    )


def generate(yml, md):
    mark_expired_dates(yml)
    headers = ["name", "publisher", "rank", "scope", "short", "full", "format", "cfp", "country"]
    template = "".join([
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
    rows = ["| {0} |".format(" | ".join(headers))]
    rows.append(
        "| {0} |".format(
            " | ".join(["---" for _ in range(len(headers))]),
        ),
    )
    rows.extend(
        md_rows(
            yaml.safe_load(Path(yml).read_text()),
            template,
        ),
    )
    sep = "<!-- events -->"
    split = Path(md).read_text().split(sep)
    split[1] = "\n{0}\n\n".format("\n".join(rows))
    Path(md).write_text(sep.join(split))


if __name__ == "__main__":
    generate(sys.argv[1], sys.argv[2])  # pragma: no cover
