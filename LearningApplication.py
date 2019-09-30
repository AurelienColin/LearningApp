import os
import sys
import fire

from Rignak_LearningApp.Canvas import Canvas
from Rignak_LearningApp.Questions import Questions
from Rignak_LearningApp.Question import Question
from Rignak_LearningApp.leitner import get_leitner_json

QUESTIONS_ROOT = 'input'
MAX_QUESTION_BY_SESSION = 75


def get_questions(filename, min_index, max_index,
                  questions_root=QUESTIONS_ROOT,
                  max_question_by_session=MAX_QUESTION_BY_SESSION,
                  leitner_json=get_leitner_json()):
    """

    :param filename: name of the file containing the questions
    :param min_index: index of the first question to ask
    :param max_index: index of the last question to ask
    :param questions_root: name of the folder containing the questions
    :param max_question_by_session: max number of question to ask
    :param leitner_json: json containing a leitner dictionnary
    :return:
    """
    with open(os.path.join(questions_root, filename), 'r', encoding='utf-16') as file:
        lines = file.readlines()

    questions = Questions([], leitner_json=leitner_json)
    for line in lines[min_index: max_index]:
        question, answer, information = line.split('\t')
        question = Question(question, answer, information[:-1])
        questions.append(question)

    questions = questions.downsample(max_question_by_session)
    return questions


def loop(questions):
    print(f'You have {len(questions)} questions')

    frame = Canvas(questions)
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
    questions = fire.Fire(get_questions)
    loop(questions)
