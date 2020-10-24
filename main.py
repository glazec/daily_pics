from __future__ import print_function, unicode_literals
import sys
from plugins.pixiv.pixiv import *
from plugins.twitter.twitter import *
from pprint import pprint
from PyInquirer import prompt, Separator

if __name__ == "__main__":
    # create necessary files and folders

    # command prompt
    questions = [
        {
            'qmark': '+',
            'type': 'checkbox',
            'name': 'platform',
            'message': 'Which platform to check new likes?',
            'choices': [{'name': "Pixiv"}, {'name': 'Twitter'}]
        }
    ]
    answers = prompt(questions)
    # pprint(answers)
    if 'Pixiv' in answers['platform']:
        pixiv()
    if 'Twitter' in answers['platform']:
        twitter()

    # Delete empty folders
