import json

LEITNER_FILENAME = 'leitner.json'


def get_leitner_json(leitner_filename=LEITNER_FILENAME):
    with open(leitner_filename, 'r', encoding='utf-16') as leitner_file:
        leitner_json = json.load(leitner_file)
    return leitner_json


def export_leitner_json(leitner_json, leitner_filename=LEITNER_FILENAME):
    leitner_dump = json.dumps(leitner_json, ensure_ascii=False, indent=4, sort_keys=True)
    with open(leitner_filename, 'w', encoding='utf-16') as leitner_file:
        leitner_file.write(leitner_dump)
