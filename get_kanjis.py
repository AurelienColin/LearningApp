from rignak.src.custom_requests.request_utils import request_with_retry
from rignak.src.init import logger
from rignak.src.textfile_utils import get_lines, safe_file_replacement
from learning_with_leitner.learning_application import get_args


def get_kanji_information(kanji: str) -> tuple:
    url = 'https://www.dictionnaire-japonais.com/search.php?w=' + kanji
    soup = request_with_retry(url, soup=True)

    ul_element = soup.find('ul', class_='resultsList')
    li_element = ul_element.find('li')
    if li_element is None:
        return kanji, '', ''

    kanji = li_element.find('span', class_='jp').text
    transliteration = li_element.find('span', class_='romaji').text
    translation = li_element.find('span', class_='fr').text
    return kanji, transliteration, translation


def main() -> None:
    filename = get_args()[0]

    lines_with_definition = []
    kanjis_without_definition = []
    new_lines = []

    kanjis = []
    lines = get_lines(filename)
    for line in lines:
        split_line = line.split('\t')
        if len(split_line) == 3 and all(split_line):
            lines_with_definition.append(line + '\n')
            kanjis.append(split_line[0])
        else:
            kanjis_without_definition.append(split_line[0])
    logger(f"{len(lines_with_definition)} kanjis with definition.")
    logger(f"{len(kanjis_without_definition)} kanjis to retrieve.")

    logger.set_iterator(len(kanjis_without_definition), percentage_threshold=1)
    for kanji in kanjis_without_definition:
        kanji, transliteration, translation = get_kanji_information(kanji)
        if kanji not in kanjis and transliteration and translation:
            kanjis.append(kanji)
            new_lines.append(f"{kanji}\t{transliteration}\t{translation}\n")

        logger.iterate()

    safe_file_replacement(filename, lines_with_definition + new_lines)


if __name__ == '__main__':
    main()
