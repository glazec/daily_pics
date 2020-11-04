from __future__ import print_function, unicode_literals
import sys
from plugins.pixiv.pixiv import *
from plugins.twitter.twitter import *
from pprint import pprint
from PyInquirer import prompt, Separator
from utilities.digest import *

if __name__ == "__main__":
    # create necessary files and folders
    current_date = '0'
    if datetime.datetime.now().hour < 3:
        current_date = date.today()-datetime.timedelta(days=1)
    else:
        current_date = date.today()
    if not os.path.exists(f'assets/{current_date}'):
        os.makedirs(f'assets/{current_date}')

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
    if len(os.listdir(f'assets/{current_date}'))==0:
        os.rmdir(f'assets/{current_date}')
    else:
        digest(f'assets/{current_date}')

