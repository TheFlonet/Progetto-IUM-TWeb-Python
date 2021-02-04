import os
import re
import PySimpleGUI as sg

from util.colors import colors
from game.game import GameBoard
from game.config import Config
from graphics.layout import inflate_initial_layout, inflate_player_layout, inflate_game_layout
from util.position import Position


def are_valid(nicks):
    """
    check if a list of nicknames is valid (no identical nicknames and every nick is set)

    :param nicks: list of nicknames
    :return: true if it is valid, false otherwise
    """
    if not len(nicks) == len(set(nicks)):
        return False
    used_nicks = []
    for nick in nicks:
        if nick not in used_nicks:
            used_nicks.append(nick)
        else:
            return False

    return True


def main_loop():
    game = GameBoard(Config(os.path.join(os.path.dirname(__file__), 'config.json')))
    sg.theme('Default1')
    window = sg.Window('Filetto', inflate_initial_layout(), element_justification='c')
    color_list = colors(game.config.player_num)
    nicks = []
    btn_pattern = re.compile('[0-9]+, [0-9]+')
    i = 0
    next_turn = False
    set_turn = False

    while not game.game_finished:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == 'Play':  # from main window to nicknames window
            window.close()
            window = sg.Window('Filetto', inflate_player_layout(game.config.player_num))
        elif event == 'Rules':
            sg.popup('Rules', game.game_info())
        elif event == 'Exit':  # back to main window
            window.close()
            game = GameBoard(game.config)
            window = sg.Window('Filetto', inflate_initial_layout(), element_justification='c')
            set_turn = False
        elif event == 'Start':  # from nicknames window to game board window
            nicks.clear()
            for x in range(game.config.player_num):
                nicks.append(values[f'-PLAYER{x}-'].strip())

            if nicks == ['' for _ in range(game.config.player_num)]:
                sg.popup('Warning', 'The game will use default nicks')
                nicks = [chr(x + 65) for x in range(game.config.player_num)]

            if are_valid(nicks):
                window.close()
                window = sg.Window('Filetto',
                                   inflate_game_layout(game.config.matrix_dim, game.config.player_num, nicks,
                                                       color_list))
                game.init_players(nicks)
                set_turn = True
                window.finalize()
            else:
                sg.popup('Error', 'Nicks are not valid\n\nCheck that every nick is different')
        elif btn_pattern.match(event):  # player input in a spot of the board
            btn_pos = Position(*(event.split(',')))
            if game.is_valid(btn_pos):
                window[event].update(button_color=('black', color_list[i]))
                game.update_state(btn_pos, i)
                for x in range(game.config.player_num):
                    window[f'-SCORE{x}-'].update(game.players[x].score)
                next_turn = True

        if next_turn:
            i += 1
            next_turn = False
        i = i % game.config.player_num
        if set_turn:
            window['-ROUND-'].update(f'Round {i + 1}\n{nicks[i]}\'s turn')

    if game.game_finished:
        sg.popup('Game finished', game.score_rankings())
    window.close()


if __name__ == '__main__':
    main_loop()
