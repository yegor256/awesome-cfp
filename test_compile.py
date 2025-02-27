# SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
# SPDX-License-Identifier: MIT

import shutil
from pathlib import Path

import httpx
import pytest
import yaml
from more_itertools import flatten

from compile import InvalidUrlError, generate


@pytest.fixture
def _mock_http(respx_mock):
    respx_mock.route(path__regex=".*")
    yield


@pytest.fixture
def _mock_fail_http(respx_mock):
    route = respx_mock.route(path__regex=".*")

    def _side_effect(request):
        return httpx.Response(404)

    route.side_effect = _side_effect
    yield


@pytest.mark.usefixtures("_mock_http")
@pytest.mark.parametrize("fixture_dir", list(Path("fixtures").iterdir()))
def test_format(fixture_dir, tmp_path):
    shutil.copytree(fixture_dir, tmp_path, dirs_exist_ok=True)
    generate(tmp_path / "input.yml", tmp_path / "README.md")

    assert (tmp_path / "README.md").read_text() == (tmp_path / "expected.md").read_text()


@pytest.mark.usefixtures("_mock_fail_http")
def test_http_fail():
    with pytest.raises(InvalidUrlError):
        generate("fixtures/simple/input.yml", "fixtures/simple/README.md")


@pytest.mark.usefixtures("_mock_http")
def test_expired_date_updated(tmp_path):
    shutil.copytree(Path("fixtures/update-expired-date"), tmp_path, dirs_exist_ok=True)
    generate(tmp_path / "input.yml", tmp_path / "README.md")

    assert (tmp_path / "input.yml").read_text().count("  cfp: closed")
    assert (tmp_path / "input.yml").read_text().count("# SPDX-License-Identifier: MIT.\n"), "yml file not contain license"


@pytest.mark.usefixtures("_mock_fail_http")
def test_later_conf(tmp_path):
    shutil.copytree(Path("fixtures/later_conf"), tmp_path, dirs_exist_ok=True)
    generate(tmp_path / "input.yml", tmp_path / "README.md")

    assert (tmp_path / "README.md").read_text() == (tmp_path / "expected.md").read_text()


@pytest.mark.slow
def test_cfp_content(tmp_path):
    shutil.copytree(Path("fixtures/simple"), tmp_path, dirs_exist_ok=True)
    shutil.copy2(Path("cfp.yml"), tmp_path)
    generate(tmp_path / "cfp.yml", tmp_path / "README.md")

    assert (tmp_path / "README.md").read_text().split('<!-- events -->')[1].splitlines()


@pytest.mark.slow
@pytest.mark.parametrize(
    "url",
    flatten(
        (conf_info["core"], conf_info["url"])
        for conf_info in yaml.safe_load(Path("cfp.yml").read_text()).values()
        if not conf_info["later"]
    ),
)
def test_links(url):
    resource_status = httpx.get(url).status_code

    assert resource_status in range(200, 400), "Resource '{0}' unavailable. Failed with: {1}".format(
        url, resource_status,
    )
