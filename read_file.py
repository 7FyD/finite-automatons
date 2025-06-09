import json
import re

data = {}

def remove_comments(json_str):
    def replacer(match):
        s = match.group(0)
        return "" if s.startswith('/') else s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    cleaned = re.sub(pattern, replacer, json_str)
    return cleaned


def load_rules(f):
    with open(f) as json_file:
        content = remove_comments(json_file.read())
        global data
        data = json.loads(content)
        return data


def get_sections(f):
    if not data:
        load_rules(f)
    return list(data.keys())


def get_section_data(f, section):
    if not data:
        load_rules(f)
    return data[section]