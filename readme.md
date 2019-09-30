# Learning Application

## Requirements

- os
- sys
- fire
- random
- tkinter


## How to use

````
> python LearningApplication.py --help
NAME
    LearningApplication.py
    
SYNOPSIS
    LearningApplication.py FILENAME MIN_INDEX MAX_INDEX <flags>
    
POSITIONAL ARGUMENTS
    FILENAME
        name of the file containing the questions
    MIN_INDEX
        index of the first question to ask
    MAX_INDEX
        index of the last question to ask
        
FLAGS
    --questions_root=QUESTIONS_ROOT
        name of the folder containing the questions
    --max_question_by_session=MAX_QUESTION_BY_SESSION
        max number of question to ask
    --leitner_json=LEITNER_JSON
        json containing a leitner dictionnary
````