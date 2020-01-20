import json
import sys
import os 

LEITNER_FILENAME = os.path.join('leitner', f'leitner_{os.path.splitext(sys.argv[1])[0]}.json')

def get_leitner_json(leitner_filename=LEITNER_FILENAME):
    with open(leitner_filename, 'r', encoding='utf-16') as leitner_file:
        leitner_json = json.load(leitner_file)
    return leitner_json


def export_leitner_json(leitner_json, leitner_filename=LEITNER_FILENAME):
    leitner_dump = json.dumps(leitner_json, ensure_ascii=False, indent=4, sort_keys=True)
    with open(leitner_filename, 'w', encoding='utf-16') as leitner_file:
        leitner_file.write(leitner_dump)


def get_stats(leitner_filename=LEITNER_FILENAME):
    leitner_json = get_leitner_json(leitner_filename=leitner_filename)
    box_numbers = list(leitner_json.values())
    for i in range(max(box_numbers) + 1):
        print(f'Number of question in box {i}: {len([box_number for box_number in box_numbers if box_number == i])}')


if __name__ == '__main__':
    get_stats()
