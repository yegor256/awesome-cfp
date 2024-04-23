import pytest
from compile import generate


def generate_yaml():
    yml_content = '''
    "ABC":
      - year: "2099"
      - url: "[ABC'99](https://conf.researchr.org/series/abc)"
      - publisher: IEEE
      - rank: "C"
      - core: "(https://portal.core.edu.au/conf-ranks/2099/)"
      - score: "SE"
      - short: "2"
      - full: "10"
      - format: 1C
      - cfp: "2099-12-31"
      - country: Antarctica
    '''
    with open('test.yml', 'w') as f:
        f.write(yml_content)


def generate_md():
    header = '''# Curated List of CFPs

This is a curated list of currently open Calls for Papers for computer
science conferences. You are welcome to make changes and suggest conferences
(and journals) that deserve inclusion. Obviously, our list is not complete
and is not intended to be. For a larger and more complete list of
currently open CFPs,
you may check the [WikiCFP](http://www.wikicfp.com/cfp/) and
[call4paper](https://www.call4paper.com/) websites.
Our job is to regularly update the last column in the list, ensuring that
you don't need to visit all conference websites. If you want your favorite
conference to be included so you won't miss its deadline,
please send us a pull request.\n'''
    sep = "<!-- events -->"
    bottom = '''
**SE** stands for "Software Engineering",
**SA** for "Software Architecture",
**PL** for "Programming Languages",
**ST** for "Software Testing".
**SRC** stands for "Student Research Competition," where they _usually_ expect
2-pages papers (sometimes up to three pages)
from a single student, who must physically attend the event.
**NIER** stands for "New Ideas and Emerging Results," where
they _usually_ expect 4-pages papers.
**Format** should be either LNCS, 2C (two columns), or 1C (one column).'''
    md_content = header + sep + "\n" + sep + bottom
    with open("test.md", "w") as f:
        f.write(md_content)

    headers = ['year', 'name', 'publisher', 'rank', 'core', 'scope', 'short', 'full', 'format', 'cfp', 'country']

    markdown_table = "| " + " | ".join(headers) + " |\n"
    markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    markdown_table += "| " + "2099" + " | "
    markdown_table += "[ABC'99](https://conf.researchr.org/series/abc)" + " | "
    markdown_table += "IEEE" + " | "
    markdown_table += "C" + " | "
    markdown_table += "[link](https://portal.core.edu.au/conf-ranks/2099)" + " | "
    markdown_table += "SE" + " | "
    markdown_table += "2" + " | "
    markdown_table += "10" + " | "
    markdown_table += "1C" + " | "
    markdown_table += "2099-12-31" + " | "
    markdown_table += "Antarctica" + " |"
    markdown_table.rstrip()
    markdown_table += "\n"

    with open("test.md", "r") as f:
        readme = f.read()

    p = readme.split(sep)

    p[1] = "\n" + markdown_table + "\n"
    new = sep.join(p)

    with open("test.md", "w") as f:
        f.write(new)


def run():
    generate_yaml()
    generate_md()
    generate('test.yml', 'README.md')


def test_compile():
    run()
    with open("test.md", "r") as f, open("test_README.md", "r") as g:
        assert f.read() == g.read()


if __name__ == '__main__':
    test_compile()
