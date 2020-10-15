import json
import os
import sys

from util.colors import Colors


def check_settings(settings):
    """
    check if the configuration file is valid

    :param settings: config object
    """
    if settings is None:
        print(f'{Colors.FAIL}Settings not found{Colors.END}')
        sys.exit(-1)

    settings_keys = settings.keys()

    if 'matrixDim' not in settings_keys or settings['matrixDim'] < 3:
        print(f'{Colors.FAIL}Matrix dimension is absent or is less than 3{Colors.END}')
        sys.exit(-1)

    if 'playerNum' not in settings_keys or settings['playerNum'] < 2:
        print(f'{Colors.FAIL}Players\' number absent or is less than 2{Colors.END}')
        sys.exit(-1)

    if 'winScore' not in settings_keys or settings['winScore'] < 1:
        print(f'{Colors.FAIL}Winning score is absent or is less than 1{Colors.END}')
        sys.exit(-1)

    if 'lenScore' not in settings_keys:
        print(f'{Colors.FAIL}Length-Score table is absent{Colors.END}')
        sys.exit(-1)

    len_score = settings['lenScore']
    len_score = {int(key): int(value) for key, value in len_score.items()}

    if len_score is None or not bool(len_score):
        print(f'{Colors.FAIL}Table score is not valid{Colors.END}')
        sys.exit(-1)

    score_keys = list(len_score.keys())
    if 0 in score_keys or any(x < 0 for x in score_keys):
        print(f'{Colors.FAIL}To get point(s) you should at least play one round{Colors.END}')
        sys.exit(-1)

    if 'spacing' not in settings_keys or not settings['spacing'].isspace():
        print(f'{Colors.FAIL}Spacing option is absent or is not valid{Colors.END}')
        sys.exit(-1)


class Config:
    matrix_dim = 0
    player_num = 0
    win_score = 0
    len_score = {}
    spacing = ""

    def __init__(self, path):
        if not os.path.isfile(path):
            print(f'{Colors.FAIL}Configuration file does not exist {Colors.END}')
            sys.exit(-1)
        with open(path) as config_file:
            json_config = json.load(config_file)
            check_settings(json_config)
        self.matrix_dim = json_config['matrixDim']
        self.player_num = json_config['playerNum']
        self.win_score = json_config['winScore']
        self.len_score = json_config['lenScore']
        self.len_score = {int(key): int(value) for key, value in self.len_score.items()}
        self.spacing = json_config['spacing']

    def __str__(self) -> str:
        config_obj = f'{Colors.BOLD}Config:\n'
        config_obj += f'Board dimension: {self.matrix_dim}\n'
        config_obj += f'Player Numbers: {self.player_num}\n'
        config_obj += f'Score to win: {self.win_score}\n'
        config_obj += f'Score map (len: score): {self.len_score}{Colors.END}\n'
        return config_obj

    def score_table(self):
        """
        print the score table formatted
        """
        keys = list(self.len_score.keys())
        keys.sort()
        print(f'{Colors.BOLD}Score table\n\t-format: Sequence length = Score-')
        for i in range(len(keys)):
            print(f'{keys[i]} = {self.len_score[keys[i]]}')
        print(Colors.END, end='')
