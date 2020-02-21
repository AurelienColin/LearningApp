import random

LEITNER_FILENAME = 'leitner.json'


class Questions(list):
    def __init__(self, question_list, leitner_json):
        super().__init__()

        for question in question_list:
            self.append(question)
        self.leitner_json = leitner_json

    def downsample(self, max_number):
        if max_number >= len(self):
            return self

        for question in self:
            if str(question) not in self.leitner_json:
                self.leitner_json[str(question)] = 0

        kept_questions = Questions([], leitner_json=self.leitner_json)
        while len(kept_questions) < max_number:
            if len(self) == 1:
                i = 0
            else:
                i = random.randint(0, len(self) - 1)
            if random.random() < 2 ** -self.leitner_json[str(self[i])]:
                kept_questions.append(self.pop(i))
        return kept_questions

    def export(self, results):
        for question in self:
            if results[str(question)]['failure']:
                self.leitner_json[str(question)] = 0
            else:
                self.leitner_json[str(question)] = self.leitner_json.get(str(question), -1) + 1
        return self.leitner_json

    def random_choice(self, result):
        sublist = [question
                   for question in self
                   if result[str(question)]['success'] < question.required_success]
        question = random.choice(sublist)
        return question

    def remaining_length(self, result):
        return len([question
                    for question in self
                    if result[str(question)]['success'] < question.required_success])
