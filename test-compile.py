import pytest
from compile import generate


def generate_yaml():
    yml_content = '''
    "ABC":
      - year: "2099"
      - url: "[ABC'99](https://conf.researchr.org/series/abc)"
      - publisher: IEEE
      - rank: "C"
      - core: "<https://portal.core.edu.au/conf-ranks/2099>"
      - scope: "SE"
      - short: "2"
      - full: "10"
      - format: 1C
      - cfp: "2099-12-31"
      - country: Antarctica
    '''
    with open("target/test.yml", "w") as f:
        f.write(yml_content)


def generate_md():
    header = "# Curated List of CFPs\n"
    sep = "<!-- events -->\n"
    bottom = "Explanations for abbreviations.\n"
    md_content = header + sep + sep + bottom
    with open("target/test.md", "w+") as f:
        f.write(md_content)

    headers = ['year', 'name', 'publisher', 'rank', 'core', 'scope', 'short', 'full', 'format', 'cfp', 'country']

    markdown_table = "| " + " | ".join(headers) + " |\n"
    markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    markdown_table += "| " + "2099" + " | "
    markdown_table += "[ABC'99](https://conf.researchr.org/series/abc)" + " | "
    markdown_table += "IEEE" + " | "
    markdown_table += "C" + " | "
    markdown_table += "<https://portal.core.edu.au/conf-ranks/2099>" + " | "
    markdown_table += "SE" + " | "
    markdown_table += "2" + " | "
    markdown_table += "10" + " | "
    markdown_table += "1C" + " | "
    markdown_table += "2099-12-31" + " | "
    markdown_table += "Antarctica" + " |"
    markdown_table.rstrip()
    markdown_table += "\n"

    with open("target/test.md", "r") as f:
        readme = f.read()

    p = readme.split(sep)

    p[1] = "\n" + markdown_table + "\n"
    new = sep.join(p)

    with open("target/test.md", "w+") as f:
        f.write(new)


def create_test_readme():
    header = "# Curated List of CFPs\n"
    sep = "<!-- events -->\n"
    table = ("| year | name | publisher | rank | core | scope | short | full | format | cfp | country |\n| --- | --- | "
             "--- | --- | --- | --- | --- | --- | --- | --- | --- |\n| 2099 | [ABC'99]("
             "https://conf.researchr.org/series/abc) | IEEE | C | <https://portal.core.edu.au/conf-ranks/2099> "
             "| SE | 2 | 10 | 1C | 2099-12-31 | Antarctica |\n")
    bottom = "Explanations for abbreviations.\n"
    md_content = header + sep + "\n" + table + "\n" + sep + bottom
    with open("target/test_README.md", "w+") as f:
        f.write(md_content)


def run():
    generate_yaml()
    generate_md()
    create_test_readme()
    generate('test.yml', 'README.md')


def test_compile():
    run()
    with open("target/test.md", "r") as f, open("target/test_README.md", "r") as g:
        assert f.read() == g.read()


if __name__ == '__main__':
    test_compile()