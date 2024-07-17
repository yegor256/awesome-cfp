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

from pathlib import Path

import httpx
import pytest

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
def test_format(fixture_dir):
    generate(fixture_dir / "input.yml", fixture_dir / "README.md")

    assert (fixture_dir / "README.md").read_text() == (fixture_dir / "expected.md").read_text()


@pytest.mark.usefixtures("_mock_fail_http")
def test_http_fail():
    with pytest.raises(InvalidUrlError):
        generate("fixtures/simple/input.yml", "fixtures/simple/README.md")
