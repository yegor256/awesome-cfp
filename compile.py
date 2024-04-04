import yaml

li = []
with open('cfp.yml', 'r') as stream:
    yaml_content = yaml.safe_load(stream)
    li.append(dict(yaml_content))

for x in li:
    print(x.keys())
    print(x.values())

headers = ['publisher', 'CORE', 'Scope', 'Short pages', 'Full pages', 'Format', 'CFP']
