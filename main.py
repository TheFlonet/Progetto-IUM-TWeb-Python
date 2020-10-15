import os

from util.colors import Colors
from util.game import GameBoard
from util.config import Config


def main_loop():
    config = Config(os.path.join(os.path.dirname(__file__), 'config.json'))
    game_matrix = GameBoard(config)
    game_matrix.init_game()
    i = 0
    while not game_matrix.game_finished:
        i = i % len(game_matrix.players)
        game_matrix.player_round(i)
        game_matrix.print_state()
        i += 1
    print(f'\n{Colors.HEADER}Thanks for playing Filetto\nBy Mario Bifulco\nMatr: 881727{Colors.END}')


if __name__ == '__main__':
    main_loop()
