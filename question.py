import learning_with_leitner.local_config as config

from rignak.src.init import assert_argument_types


class Question:
    @assert_argument_types
    def __init__(
            self: 'Question',
            question: str,
            answer: str,
            information: str,
            required_success: int = config.REQUIRED_SUCCESS
    ) -> None:
        self.question = question
        self.answer = answer
        self.information = information
        self.required_success = required_success

    @assert_argument_types
    def __str__(
            self: 'Question'
    ):
        return f"question:{self.question}, answer:{self.answer}, information:{self.information}"
