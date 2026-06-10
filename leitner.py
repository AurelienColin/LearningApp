import json
import os

import learning_with_leitner.local_config as config
from rignak.src.init import assert_argument_types, ExistingFilename, logger


def get_leitner_filename(
        filename: str,
        leitner_root: str = config.LEITNER_ROOT
) -> str:
    leitner_filename = f"{leitner_root}/{os.path.splitext(os.path.basename(filename))[0]}.json"
    return leitner_filename


@assert_argument_types
def get_leitner_json(
        leitner_filename: str
) -> dict:
    if os.path.exists(leitner_filename):
        with open(leitner_filename, 'r', encoding='utf-16') as leitner_file:
            leitner_json = json.load(leitner_file)
    else:
        leitner_json = {}
    return leitner_json


@assert_argument_types
def export_leitner_json(
        leitner_json: dict,
        leitner_filename: str
) -> ExistingFilename:
    leitner_dump = json.dumps(leitner_json, ensure_ascii=False, indent=4, sort_keys=True)

    os.makedirs(os.path.dirname(leitner_filename), exist_ok=True)
    with open(leitner_filename, 'w', encoding='utf-16') as leitner_file:
        leitner_file.write(leitner_dump)
    return ExistingFilename(leitner_filename)


@assert_argument_types
def get_stats(
        filename: ExistingFilename
) -> None:
    leitner_json = get_leitner_json(filename)
    box_numbers = list(leitner_json.values())
    for i in range(max(box_numbers) + 1):
        logger(f'Number of question in box {i}: {len([box_number for box_number in box_numbers if box_number == i])}')
