import tkinter as tk

import local_config
from rignak.src.init import assert_argument_types, logger
from learning_with_leitner.leitner import export_leitner_json, get_stats
from learning_with_leitner.question import Question
from learning_with_leitner.questions import Questions


class Canvas(tk.Tk):
    @assert_argument_types
    def __init__(
            self: 'Canvas',
            questions: Questions,
            leitner_filename: str,
            width: (int, float) = local_config.WIDTH,
            height: (int, float) = local_config.HEIGHT,
            button_width: (int, float) = local_config.BUTTON_WIDTH,
            entry_width: (int, float) = local_config.ENTRY_WIDTH,
            font: (int, float) = local_config.FONT,
            text_width: (int, float) = local_config.TEXT_WIDTH,
            text_height: (int, float) = local_config.TEXT_HEIGHT
    ) -> None:
        self.questions = questions
        self.leitner_filename = leitner_filename

        self.window = tk.Tk.__init__(self)
        self.bind('<Return>', self.on_button_check)
        self._update = False

        self.canvas = tk.Canvas(self.window, width=width, height=height)

        self.font = font
        self.text_width = text_width
        self.text_height = text_height

        self._text = self.canvas.create_text(text_width, text_height, text='', font=self.font)
        self.canvas.pack()

        self.entry = tk.Entry(self.window, width=entry_width)
        self.entry.pack()

        self.button_check = tk.Button(self, text='Check', command=self.on_button_check, width=button_width)
        self.button_check.pack()

        self.button_pass = tk.Button(self, text='Pass', command=self.on_button_pass, width=button_width)
        self.button_pass.pack()

        self.button_break = tk.Button(self, text='Break', command=self.on_button_break, width=button_width)
        self.button_break.pack()

        self.results = {str(question): {'failure': False, 'success': 0} for question in questions}
        self.current_question = None
        self.total = 0

    @assert_argument_types
    def run(self: 'Canvas', question: Question) -> None:
        self.current_question = question
        self.canvas.delete(self._text)
        self._text = self.canvas.create_text(self.text_width, self.text_height, text=self.current_question.question,
                                             font=self.font)
        self.canvas.pack()
        self._update = False

    @assert_argument_types
    def on_button_check(self: 'Canvas', event: (None, tk.Event) = None) -> None:
        self.total += 1
        if self.entry.get() == self.current_question.answer:
            if self.results[str(self.current_question)]['failure']:
                self.results[str(self.current_question)]['success'] += 1
            else:
                self.results[str(self.current_question)]['success'] += self.current_question.required_success - 1
            self.print_answer(True)
            self._update = True
        else:
            self.results[str(self.current_question)]['failure'] = True
            self.results[str(self.current_question)]['success'] = 0
            self.print_answer(False)
            self._update = self.current_question
        self.entry.delete(0, 'end')
        self.entry.insert(0, '')
        self.entry.pack()

    @assert_argument_types
    def print_answer(self: 'Canvas', right_or_false: bool) -> None:
        logger(f'{right_or_false}: {self.current_question.question}->{self.current_question.answer} '
               f'{self.questions.remaining_length(self.results)} ({self.current_question.information})')

    @assert_argument_types
    def on_button_pass(self: 'Canvas') -> None:
        self._update = True

    @assert_argument_types
    def on_button_break(self: 'Canvas') -> None:
        leitner_json = self.questions.export(self.results)
        leitner_filename = export_leitner_json(leitner_json, self.leitner_filename)
        get_stats(leitner_filename)
        logger(f"Completed in {self.total} questions.")

        nb_errors = len([entry for entry in self.results.values() if entry['failure']])
        logger(f"Errors on {nb_errors} questions.")
        self.destroy()
