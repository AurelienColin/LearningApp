import random

from rignak.src.init import assert_argument_types
from learning_with_leitner.question import Question


class Questions(list):
    @assert_argument_types
    def __init__(
            self: "Questions",
            question_list: list,
            leitner_json: dict
    ) -> None:
        super().__init__()

        for question in question_list:
            self.append(question)
        self.leitner_json = leitner_json

    @assert_argument_types
    def downsample(
            self: "Questions",
            max_number: int
    ) -> "Questions":
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

    @assert_argument_types
    def export(
            self: "Questions",
            results: dict
    ) -> dict:
        for question in self:
            if results[str(question)]['failure']:
                self.leitner_json[str(question)] = 0
            else:
                self.leitner_json[str(question)] = self.leitner_json.get(str(question), -1) + 1
        return self.leitner_json

    @assert_argument_types
    def random_choice(
            self: "Questions",
            result: dict
    ) -> Question:
        sublist = [question
                   for question in self
                   if result[str(question)]['success'] < question.required_success]
        question = random.choice(sublist)
        return question

    @assert_argument_types
    def remaining_length(
            self: "Questions",
            result: dict
    ) -> int:
        length = len(
            [question
             for question in self
             if result[str(question)]['success'] < question.required_success]
        )
        return length
