import os

import fire

import learning_with_leitner.local_config as config
from rignak.src.init import assert_argument_types, ExistingFilename, logger
from learning_with_leitner.canvas import Canvas
from learning_with_leitner.leitner import get_leitner_json, get_leitner_filename
from learning_with_leitner.question import Question
from learning_with_leitner.questions import Questions


@assert_argument_types
def get_args(
        filename: str = config.DEFAULT_FILENAME,
        questions_root: str = config.DEFAULT_QUESTIONS_ROOT,
        max_question_per_session: int = config.DEFAULT_MAX_QUESTION_PER_SESSION
) -> tuple:
    filename = ExistingFilename(os.path.join(questions_root, filename))
    leitner_filename = get_leitner_filename(filename)
    return filename, leitner_filename, max_question_per_session


@assert_argument_types
def get_questions(filename: ExistingFilename, leitner_filename: str, max_question_by_session: int) -> Questions:
    leitner_json = get_leitner_json(leitner_filename)
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()[:config.NUMBER_OF_QUESTIONS]

    questions = Questions([], leitner_json=leitner_json)

    for line in lines:
        logger(line)
        question, answer, information = line.split('\t')
        question = Question(question, answer, information[:-1])
        questions.append(question)

    questions = questions.downsample(max_question_by_session)
    return questions


@assert_argument_types
def loop(questions: Questions, leitner_filename: str) -> None:
    logger(f'You have {len(questions)} questions')

    frame = Canvas(questions, leitner_filename)
    while True:
        if isinstance(frame._update, Question):
            question = frame._update
            frame.run(question)
        else:
            if not frame.questions.remaining_length(frame.results):
                frame.on_button_break()
                return
            frame.run(frame.questions.random_choice(frame.results))
        frame.update()
        while True:
            frame.update()
            if frame._update:
                frame.canvas.delete(frame._text)
                break


if __name__ == '__main__':
    _filename, _leitner_filename, _max_question_per_session = fire.Fire(get_args())
    _questions = get_questions(_filename, _leitner_filename, _max_question_per_session)
    loop(_questions, _leitner_filename)
