import tkinter as tk

from Rignak_LearningApp.leitner import export_leitner_json

HEIGHT = 100
WIDTH = 400
BUTTON_WIDTH = WIDTH // 40
ENTRY_WIDTH = WIDTH // 40 * 3
TEXT_WIDTH = WIDTH // 2
TEXT_HEIGHT = HEIGHT // 5
FONT = 'Arial 25'


class Canvas(tk.Tk):
    def __init__(self, questions, width=WIDTH, height=HEIGHT, button_width=BUTTON_WIDTH, entry_width=ENTRY_WIDTH,
                 font=FONT, text_width=TEXT_WIDTH, text_height=TEXT_HEIGHT):
        self.questions = questions

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

        self.results = {str(question): {'failure':False, 'success':0} for question in questions}
        self.current_question = None

    def run(self, question):
        self.current_question = question
        self.canvas.delete(self._text)
        self._text = self.canvas.create_text(self.text_width, self.text_height, text=self.current_question.question,
                                             font=self.font)
        self.canvas.pack()
        self._update = False

    def on_button_check(self, event=None):
        if self.entry.get() == self.current_question.answer:
            if self.results[str(self.current_question)]['failure']:
                self.results[str(self.current_question)]['success'] += 1
            else:
                self.results[str(self.current_question)]['success'] += self.current_question.required_success-1
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

    def print_answer(self, right_or_false):
        print(f'{right_or_false}: {self.current_question.question}->{self.current_question.answer} '
              f'{self.questions.remaining_length(self.results)} ({self.current_question.information})')

    def on_button_pass(self):
        self._update = True

    def on_button_break(self):
        print()
        print('--------------------------------')
        leitner_json = self.questions.export(self.results)
        export_leitner_json(leitner_json)
        self.destroy()
