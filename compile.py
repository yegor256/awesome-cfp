# SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
# SPDX-License-Identifier: MIT

from __future__ import annotations

import datetime
import sys
from copy import deepcopy
from pathlib import Path
from typing import Literal, TypeAlias, TypedDict

import httpx
import yaml


class InvalidUrlError(Exception):
    """Exception threw on fail ping url."""


class ExpiredCfpError(Exception):
    """Exception threw on call for papers date expired."""


DateAsStrT: TypeAlias = str
ClosedStrLiteral = "closed"
UrlStrLiteral = "url"
RankStrLiteral = "rank"
CfpStrLiteral = "cfp"
RawDateT: TypeAlias = DateAsStrT | Literal[ClosedStrLiteral]


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


def build_name(name: str, inf: ConfInfoDict) -> str:
    """Build name.

    >>> build_name('ABC', {'year': '2099', 'url': 'https://google.com', 'later': False})
    "[ABC'99](<https://google.com>)"
    >>> build_name('ABC', {'year': 2099, 'url': 'https://google.com', 'later': False})
    "[ABC'99](<https://google.com>)"
    """
    year = str(inf["year"])[-2:]
    return "[{0}'{1}](<{2}>)".format(
        name,
        year,
        inf[UrlStrLiteral] if inf["later"] else validate_url(inf[UrlStrLiteral]),
    )


def date_actual(date: datetime.date) -> datetime.date:
    today = datetime.datetime.now(tz=datetime.UTC).date()
    if date > today:
        return date
    msg = f"{date} expired for today {today}"
    raise ExpiredCfpError(msg)


def render_date(date: RawDateT | None) -> str:
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
    if date == ClosedStrLiteral:
        return ClosedStrLiteral
    parsed = datetime.datetime.strptime(
        date, "%Y-%m-%d",
    ).replace(tzinfo=datetime.UTC).date()
    return parsed.strftime("%y-%b")


def build_row(name: str, inf: list[dict], template: str) -> str:
    return template.format(
        name=build_name(name, inf),
        publisher=inf["publisher"] or "",
        rank="[{0}](<{1}>)".format(
            inf[RankStrLiteral],
            inf[UrlStrLiteral] if inf["later"] else validate_url(inf["core"]),
        ),
        scope=inf["scope"],
        short=inf["short"] or "",
        full=inf["full"] or "",
        format=inf["format"] or "",
        cfp=render_date(inf[CfpStrLiteral]),
        country=inf["country"],
    )


def md_rows(yml: dict[str, ConfInfoDict], template: str) -> list[str]:
    return [
        build_row(name, inf, template)
        for name, inf in sorted(
            yml.items(),
            key=_sort_key,
        )
    ]


def _sort_key(elem: str) -> int:
    srtd = {
        char: idx
        for idx, char in enumerate(["A*", "A", "B", "C", "D", "E", "F"])
    }
    return srtd[elem[1][RankStrLiteral]]


def validate_url(url: str) -> str:
    response = httpx.get(url)
    success = httpx.codes.is_success(response.status_code)
    allow = success or httpx.codes.is_redirect(response.status_code)
    if not allow:
        msg = f"Url = '{url}' return status = {response.status_code}"
        raise InvalidUrlError(msg)
    return url


def mark_expired_dates(path: str) -> None:
    yml = Path(path).read_text()
    origin = yaml.safe_load(yml)
    updated = deepcopy(origin)
    for name, inf in yaml.safe_load(yml).items():
        if not inf[CfpStrLiteral] or inf[CfpStrLiteral] == ClosedStrLiteral:
            continue
        try:
            date_actual(
                datetime.datetime.strptime(
                    inf[CfpStrLiteral],
                    "%Y-%m-%d",
                ).replace(tzinfo=datetime.UTC).date(),
            )
        except ExpiredCfpError:
            updated[name][CfpStrLiteral] = ClosedStrLiteral
    write_yaml_file(path, updated)


def write_yaml_file(path: str, yml: ConfInfoDict) -> None:
    records = []
    for name, record in yml.items():
        dumped = yaml.safe_dump({name: record})
        lines = sorted(
            dumped.splitlines()[1::],
            key=_sort_lines_key,
        )
        records.append(
            "{0}\n{1}\n".format(
                dumped.splitlines()[0],
                "\n".join(lines),
            ),
        )
    Path(path).write_text(
        "{0}---\n{1}".format(
            Path(path).read_text().split("---")[0],
            "\n".join(records),
        ),
    )


def _sort_lines_key(line: str) -> int:
    weights = {
        name: idx
        for idx, name in enumerate([
            "year",
            UrlStrLiteral,
            "publisher",
            RankStrLiteral,
            "core",
            "scope",
            "short",
            "full",
            "format",
            CfpStrLiteral,
            "country",
            "later",
        ])
    }
    return weights[line.strip().split(":")[0]]


def generate(yml: str, md: str) -> None:
    mark_expired_dates(yml)
    headers = [
        "name",
        "publisher",
        RankStrLiteral,
        "scope",
        "short",
        "full",
        "format",
        CfpStrLiteral,
        "country",
    ]
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
