import PySimpleGUI as sg


def inflate_initial_layout():
    return [[sg.Text('FILETTO', justification='c', font='Any 18')], [sg.Button('Play', size=(15, 2))],
            [sg.Button('Rules')],
            [sg.Text('Game by: Barraco Christian, Bifulco Mario, Sciuto Samuele', justification='l')]]


def inflate_player_layout(player_num):
    player_frame = sg.Frame('', [[sg.Text(f'Player {i + 1}')] for i in range(player_num)], border_width=0)
    input_frame = sg.Frame('', [[sg.InputText(tooltip='Nickname', size=(15, 1), key=f'-PLAYER{x}-')] for x in
                                range(player_num)], border_width=0)

    return [[sg.Column([[player_frame, input_frame]], scrollable=True, size=(250, 200))],
            [sg.Button('Start'), sg.Button('Exit')]]


def inflate_game_layout(matrix_dim, player_num, nicks, color_list):
    matrix_frame = sg.Column(
        [[sg.Button(size=(3, 1), key=f'{x}, {y}') for y in range(matrix_dim)] for x in range(matrix_dim)],
        scrollable=True, size=(600, 400))

    nicks_list = sg.Frame('', [[sg.Text(f'{nicks[i]}: ')] for i in
                               range(player_num)], border_width=0)
    scores = sg.Frame('', [[sg.Text('0', size=(5, 1), key=f'-SCORE{i}-')] for i in range(player_num)],
                      border_width=0)
    color_spot = sg.Frame('', [[sg.Text('', size=(5, 1), background_color=color_list[i])] for i in range(player_num)],
                          border_width=0)
    players = sg.Column([[sg.Text('Players score:')], [nicks_list, scores, color_spot]], scrollable=True,
                        size=(250, 200))

    aside = sg.Frame('', [[players], [sg.Button('Exit')]], border_width=0)

    return [[sg.Text('', key='-ROUND-', size=(20, 2))],
            [matrix_frame, aside]]
