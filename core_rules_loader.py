import requests
from tinydb import TinyDB
import re

# A file for scraping and parsing the core rules to be loaded in the database
# Ideally this would be batched so the rules would be able to remain up to date with changes without manual intervention

rules_folder_url = "https://api.github.com/repos/coreruleset/coreruleset/contents/rules"
raw_url = "https://raw.githubusercontent.com/coreruleset/coreruleset/refs/heads/main/rules/"

tag_pattern = re.compile("tag:'([^\\s']+)',")
id_pattern = re.compile("\"id:([0-9]+),")


db = TinyDB('db.json')


def get_rules():
    # get the contents of the folder
    response = requests.get(rules_folder_url)

    if response.status_code == 200:
        files = response.json()
        file_names = [file['name'] for file in files]

        rules_files = []

        for file in file_names:
            # discard any non rule files
            if not file.endswith(".conf"):
                continue
            if file.startswith("REQUEST") or file.startswith("RESPONSE"):
                rules_files.append(file)

        built_rules = []

        for rule_file in rules_files:
            contents = requests.get(raw_url+rule_file).text

            rule = ""

            for line in contents.splitlines():
                # a new secrule
                if line.startswith("SecRule"):
                    if rule:
                        built_rules.append(parse_rule(rule))
                    rule = line
                    continue

                # another sec component we don't care about
                if line.startswith("Sec") or line.startswith("#"):
                    if rule:
                        built_rules.append(parse_rule(rule))
                    rule = ""
                    continue

                # only add to rules when we've already identified the start of one
                if line:
                    rule += line

        db.insert_multiple(built_rules)

    else:
        print('Unable to fetch core rules')


def parse_rule(rule: str) -> dict:
    print(rule)
    rule_id = re.search(id_pattern, rule).group(1)
    parent_id = rule_id[:3]
    tags = re.findall(tag_pattern, rule)

    # get capecs tag
    capecs = list(filter(lambda x: "capec" in x, tags))
    if capecs:
        capecs = re.findall(r'([0-9]+)', capecs[0])

    rule = {
        "type": "core_rule",
        "id": rule_id,
        "parent_id": parent_id,
        "tags": tags,
        "capecs": capecs
    }

    print(rule)

    return rule


get_rules()



