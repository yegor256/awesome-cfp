import re
from datetime import datetime


def date_in_past(date):
    return datetime.strptime(date, "%Y-%m-%d") < datetime.now()


date_pattern = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")

new_readme_content = ""
with open("README.md", "r") as f:
    for line in f.readlines():
        new_readme_content += date_pattern.sub(
            lambda match: "closed" if date_in_past(match.group(0)) else match.group(0),
            line)

with open("README.md", "w") as f:
    f.writelines(new_readme_content)
