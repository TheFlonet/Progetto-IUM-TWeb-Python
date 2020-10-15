import re

from .player import Player
from .position import Position
from .colors import Colors


def get_player_id(index, players) -> str:
    """
    get a player id from standard input

    :param index: player position in the list
    :param players: list of players already initialized
    :return: a valid id
    """
    exit_flag = False
    p_num = index + 1
    p_id = None
    while not exit_flag:
        present = False
        p_id = input(f'Player {p_num} insert your id: ')
        for i in range(len(players)):
            if players[i].player_id == p_id:
                present = True
        if present is False:
            exit_flag = True
    return p_id


class GameBoard:
    game_finished = False
    board = None
    config = None
    players = None
    round_num = 1
    spot_left = 0

    def __init__(self, config):
        """
        :param config: a config object for game settings
        """
        self.config = config
        self.board = [['.' for _ in range(config.matrix_dim)] for _ in range(config.matrix_dim)]
        self.players = []
        for i in range(self.config.player_num):
            self.players.append(Player(get_player_id(i, self.players)))
        self.spot_left = config.matrix_dim ** 2

    def __str__(self) -> str:
        n = range(len(self.board))
        result = 'Game Board:\n'
        for x in n:
            for y in n:
                result += self.board[x][y] + self.config.spacing
            result += '\n'
        return result

    def update_state(self, pos, player_num):
        """
        update game board and check if the player makes a point

        :param pos: position of cell to update
        :param player_num: player id
        """
        self.board[pos.x][pos.y] = self.players[player_num].player_id  # f'{chr(65 + player_num)}'
        self.spot_left -= 1
        self.check_board(pos, player_num)
        if self.players[player_num].score >= self.config.win_score or self.spot_left <= 0:
            self.game_finished = True

    def print_state(self):
        """
        print the current game state (board + players' scores)
        """
        print(f'{Colors.HEADER}Round: ' + str(self.round_num) + Colors.END)
        print(self)
        print(Colors.BOLD, end='')
        print('Stats:')
        for i in range(len(self.players)):
            print(f'Player {self.players[i].player_id}: ')  # print(f'Player {i + 1}:')
            print('\t' + f'Score: {self.players[i].score}')
        self.round_num += 1
        print(Colors.END)
        if self.game_finished:
            print(f'{Colors.UNDERLINE}Game Ended:{Colors.END}')
            self.print_score_rankings()

    def player_round(self, player_num):
        """
        round of a player

        :param player_num: player id
        """
        pos = None
        while not self.is_valid(pos):
            pos = self.get_position(player_num)
        self.update_state(pos, player_num)

    def is_valid(self, pos) -> bool:
        """
        check if a position is valid for the current board

        :param pos: position coordinates
        :return: True if pos is valid, False otherwise
        """
        if pos is None:
            return False
        elif self.board[pos.x][pos.y] == '.':
            return True
        else:
            return False

    def init_game(self):
        print(Colors.HEADER, end='')
        print('Filetto:\n\t-Generic version of TicTacToe-')
        print('Rules:')
        print(f'- You will play in a {self.config.matrix_dim}x{self.config.matrix_dim} board')
        print(
            f'- Valid positions are from (1, 1) -upper left corner- to ({self.config.matrix_dim}, {self.config.matrix_dim}) -bottom right corner-')
        print(f'- Game is set with {self.config.player_num} players')
        print(f'- The first one who get {self.config.win_score} point(s) win')
        print('- The sequence of characters could be in a row, column or diagonal')
        self.config.score_table()
        print(Colors.END, end='')
        print(self)

    def check_sequence(self, x, y, player, keys, delta_x=0, delta_y=0) -> int:
        """
        check if exist a valid sequence

        :param x: x coordinate
        :param y: y coordinate
        :param player: player id
        :param keys: list of keys
        :param delta_x: x offset
        :param delta_y: y offset
        :return: how many cell equal to player are in the same direction
        """
        inspect_area = range(keys[len(keys) - 1])
        result = 0
        for _ in inspect_area:
            x += delta_x
            y += delta_y
            if 0 <= x < self.config.matrix_dim and 0 <= y < self.config.matrix_dim and self.board[x][y] == player:
                result += 1
            else:
                break
        return result

    def check_board(self, pos, player_num):
        """
        check if a player make a sequence

        :param pos: position of the last cell added
        :param player_num: player id
        """
        sequence_around = {'UP': 0, 'UR': 0, 'RT': 0, 'BR': 0, 'BT': 0, 'BL': 0, 'LT': 0, 'UL': 0}
        keys = list(self.config.len_score.keys())
        keys.sort()
        player = f'{self.players[player_num].player_id}'  # f'{chr(65 + player_num)}'

        # ROW
        sequence_around['LT'] += self.check_sequence(pos.x, pos.y, player, keys, delta_y=-1)
        sequence_around['RT'] += self.check_sequence(pos.x, pos.y, player, keys, delta_y=1)
        # COL
        sequence_around['UP'] += self.check_sequence(pos.x, pos.y, player, keys, delta_x=-1)
        sequence_around['BT'] += self.check_sequence(pos.x, pos.y, player, keys, delta_x=1)
        # DIAGONAL Q1-Q3
        sequence_around['UR'] += self.check_sequence(pos.x, pos.y, player, keys, delta_x=-1, delta_y=1)
        sequence_around['BL'] += self.check_sequence(pos.x, pos.y, player, keys, delta_x=1, delta_y=-1)
        # DIAGONAL Q2-Q4
        sequence_around['UL'] += self.check_sequence(pos.x, pos.y, player, keys, delta_x=-1, delta_y=-1)
        sequence_around['BR'] += self.check_sequence(pos.x, pos.y, player, keys, delta_x=1, delta_y=1)

        row_seq = sequence_around['LT'] + sequence_around['RT'] + 1
        col_seq = sequence_around['UP'] + sequence_around['BT'] + 1
        dia_seq_q1_q3 = sequence_around['UR'] + sequence_around['BL'] + 1
        dia_seq_q2_q4 = sequence_around['UL'] + sequence_around['BR'] + 1

        if row_seq >= keys[0]:
            if sequence_around['LT'] >= keys[0]:
                self.players[player_num].score -= self.assign_point(keys, sequence_around['LT'])
            if sequence_around['RT'] >= keys[0]:
                self.players[player_num].score -= self.assign_point(keys, sequence_around['RT'])
            self.players[player_num].score += self.assign_point(keys, row_seq)
        if col_seq >= keys[0]:
            if sequence_around['UP'] >= keys[0]:
                self.players[player_num].score -= self.assign_point(keys, sequence_around['UP'])
            if sequence_around['BT'] >= keys[0]:
                self.players[player_num].score -= self.assign_point(keys, sequence_around['BT'])
            self.players[player_num].score += self.assign_point(keys, col_seq)
        if dia_seq_q1_q3 >= keys[0]:
            if sequence_around['UR'] >= keys[0]:
                self.players[player_num].score -= self.assign_point(keys, sequence_around['UR'])
            if sequence_around['BL'] >= keys[0]:
                self.players[player_num].score -= self.assign_point(keys, sequence_around['BL'])
            self.players[player_num].score += self.assign_point(keys, dia_seq_q1_q3)
        if dia_seq_q2_q4 >= keys[0]:
            if sequence_around['UL'] >= keys[0]:
                self.players[player_num].score -= self.assign_point(keys, sequence_around['UL'])
            if sequence_around['BR'] >= keys[0]:
                self.players[player_num].score -= self.assign_point(keys, sequence_around['BR'])
            self.players[player_num].score += self.assign_point(keys, dia_seq_q2_q4)

    def assign_point(self, keys, seq_len) -> int:
        if len(keys) == 1:
            return self.config.len_score[keys[0]] if seq_len >= keys[0] else 0
        elif len(keys) == 2:
            if keys[0] <= seq_len < keys[1]:
                return self.config.len_score[keys[0]]
            elif seq_len >= keys[1]:
                return self.config.len_score[keys[1]]
            else:
                return 0
        else:
            if seq_len < keys[0]:
                return 0
            for i in range(len(keys) - 1):
                if keys[i] <= seq_len < keys[i + 1]:
                    return self.config.len_score[keys[i]]

            return self.config.len_score[keys[len(keys) - 1]]

    def get_position(self, player_num) -> Position:
        """
        get a new position from standard input

        :param player_num: player id
        :return: position gotten
        """
        exit_flag = False
        pattern = re.compile('\\d+,\\s?\\d+$')
        pos = None
        while not exit_flag:
            pos = input(
                f'{Colors.GREEN}Player {self.players[player_num].player_id}{Colors.END} insert coordinates (x, y): ').strip()
            print('')
            if pattern.match(pos):
                pos = pos.split(',')
                pos = Position(int(pos[0]) - 1, int(pos[1]) - 1)
                if 0 <= pos.x < self.config.matrix_dim and 0 <= pos.y < self.config.matrix_dim:
                    exit_flag = True
        return pos

    def print_score_rankings(self):
        players_copy = self.players.copy()
        players_copy.sort(key=lambda x: x.score, reverse=True)
        print(f'{Colors.BLUE}-Ranking-')
        for i in range(len(players_copy)):
            print(f'Player {players_copy[i].player_id}: {players_copy[i].score}')
        print(Colors.END, end='')
