import yaml

li = []
with open('cfp.yml', 'r') as stream:
    yaml_content = yaml.safe_load(stream)
    li.append(dict(yaml_content))

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
please send us a pull request.
'''

markdown_table = header
markdown_table += "\n"

headers = ['name', 'publisher', 'CORE', 'Scope', 'Short pages', 'Full pages', 'Format', 'CFP']

markdown_table += "| " + " | ".join(headers) + " |\n"
markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"

for x in li:
    for v in x.values():
        markdown_table += "| "
        for i in v:
            for k, v in i.items():
                if v is None:
                    v = " "
                if type(v) is int:
                    v = str(v)
                markdown_table += v + " | "
        markdown_table += "\n"

bottom = '''
SE stands for "Software Engineering", SA for "Software Architecture", PL for "Programming Languages", ST for "Software Testing".

SRC stands for "Student Research Competition," where they usually expect 2-pages papers (sometimes up to three pages) from a single student, who must physically attend the event.

NIER stands for "New Ideas and Emerging Results," where they usually expect 4-pages papers.

Format should be either LNCS, 2C (two columns), or 1C (one column).
'''
markdown_table += bottom

with open('README.md', 'w') as markdown_file:
    markdown_file.write(markdown_table)
