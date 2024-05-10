import pytest
from compile import generate


def generate_simple_expected_md(expected_md_path):
    header = "# Curated List of CFPs\n"
    sep = "<!-- events -->\n"
    table = ("| year | name | publisher | rank | core | scope | short | full | format | cfp | country |\n| --- | --- | "
             "--- | --- | --- | --- | --- | --- | --- | --- | --- |\n| 2099 | [ABC'99]("
             "https://conf.researchr.org/series/abc) | IEEE | C | <https://portal.core.edu.au/conf-ranks/2099> "
             "| SE | 2 | 10 | 1C | 2099-12-31 | Antarctica |\n")
    bottom = "Explanations for abbreviations.\n"
    md_content = header + sep + table + "\n" + sep + bottom
    with open(expected_md_path, "w+") as f:
        f.write(md_content)


def test_compile():
    generate_simple_expected_md('fixtures/simple/expected.md')
    generate('fixtures/simple/input.yml', 'fixtures/simple/input.md')

    with open("fixtures/simple/input.md", "r") as f, open("fixtures/simple/expected.md", "r") as g:
        assert f.read() == g.read()


if __name__ == '__main__':
    test_compile()
