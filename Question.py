REQUIRED_SUCCESS = 5

class Question:
    def __init__(self, question, answer, information, required_succes = REQUIRED_SUCCESS):
        self.question = question
        self.answer = answer
        self.information = information
        self.required_success = REQUIRED_SUCCESS

    def __str__(self):
        return f"question:{self.question}, answer:{self.answer}, information:{self.information}"
