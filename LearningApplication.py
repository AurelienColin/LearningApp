import os
import sys
from Rignak_LearningApp.Canvas import Canvas
from Rignak_LearningApp.Questions import Questions
from Rignak_LearningApp.Question import Question
from Rignak_LearningApp.leitner import get_leitner_json

QUESTIONS_ROOT = 'input'
MIN_INDEX = 1
MAX_INDEX = 2 ** 20
MAX_QUESTION_BY_SESSION = 75


def parse_input(argvs):
    filename = argvs[1] + '.txt'
    if len(argvs) == 4:
        min_index = int(argvs[2])
        max_index = int(argvs[3])
    else:
        min_index = MIN_INDEX
        max_index = MAX_INDEX
    return filename, min_index, max_index


def get_questions(filename,
                  min_index=MIN_INDEX,
                  max_index=MAX_INDEX,
                  questions_root=QUESTIONS_ROOT,
                  max_question_by_session=MAX_QUESTION_BY_SESSION,
                  leitner_json=get_leitner_json()):
    with open(os.path.join(questions_root, filename), 'r', encoding='utf-16') as file:
        lines = file.readlines()

    questions = Questions([], leitner_json=leitner_json)
    for line in lines[min_index: max_index]:
        question, answer, information = line.split('\t')
        question = Question(question, answer, information[:-1])
        questions.append(question)

    questions = questions.downsample(max_question_by_session)
    return questions


def loop(filename, min_index=MIN_INDEX, max_index=MAX_INDEX):
    questions = get_questions(filename, min_index=min_index, max_index=max_index)
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
    if len(sys.argv) in [2, 4]:
        filename, min_index, max_index = parse_input(sys.argv)
        loop(filename, min_index=min_index, max_index=max_index)
