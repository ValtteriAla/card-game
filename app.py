import ttkbootstrap as tb  # type: ignore
from ttkbootstrap.constants import CENTER  # type: ignore
import logging
from logging import debug, error
from helperClasses import Label

import json

import os

from wormGame import Game as WormGame
from cardGame import Game as CardGame


class App(tb.Window):
    def __init__(
        self,
        title: str,
        size: tuple,
        theme='darkly',
        logging_level=logging.INFO,
    ) -> None:
        """
        # Main window
        ### Parameters:
        - title: Title of the app
        - size: x and y dimensions of the window. This is also the minimum size
        - target_score: score that ends the game
        - starting_score: starting point at the start of the game
        - theme: your custom theme or one of the above:\n
                  'cosmo', 'flatly', 'litera',\n
                  'minty', 'lumen', 'sandstone', 'yeti',\n
                  'pulse', 'united', 'morph', 'journal',\n
                  'darkly', 'superhero', 'solar',\n
                  'cyborg', 'vapor', 'simplex', 'cerculean'
        - logging_level: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        """
        super().__init__(themename=theme)
        logging.basicConfig(
            format='%(asctime)s %(levelname)s: %(message)s',
            datefmt='%I:%M:%S',
            level=logging_level,
        )
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.highscore_path = self.get_highscore_path()
        self.highscores = self.get_highscores()

        self.style.configure('TButton', font=('Helvetica', 18))
        self.main = Main(self)
        self.game1 = CardGame(self)
        self.game2 = WormGame(self)
        self.mainloop()

    def get_highscore_path(self) -> str:
        path_arr = os.path.abspath(__file__).split('\\')[:-1]
        folder_path = '/'.join(path_arr)
        file_path = folder_path + '/highscores.json'
        return file_path

    def get_highscores(self) -> dict:
        try:
            with open(self.highscore_path, 'r') as f:
                highscores = json.load(f)
                return highscores
        except Exception as e:
            error(e)
            return {'game1': 0}

    def get_highscore(self, game: str) -> int:
        if self.highscores.get(game):
            return self.highscores[game]
        else:
            error(f"Invalid game name; '{game}' while getting highscore")
            return 0

    def get_current_highscore(self) -> int:
        return self.current_highscore

    # Writes to file
    def set_highscore(self, game: str, value: int) -> None:
        try:
            self.highscores[game] = value
            with open(self.highscore_path, 'w') as f:
                debug(f'Writing to json: {self.highscores}')
                json.dump(self.highscores, f)
        except Exception as e:
            error(e)
            pass

    def change_window(self, window: str) -> None:
        self.main.hide()
        self.game1.hide()
        self.game2.hide()
        if window == 'game1':
            self.game1.show()
        elif window == 'game2':
            self.game2.show()
        elif window == 'main':
            self.main.show()
        else:
            self.main.show()


class Main(tb.Frame):
    def __init__(self, parent) -> None:
        """
        # Main window
        ## Game 1:
        4 cards with different operations, the goal is to get the target score 0
        """
        self.parent = parent
        self.frame = tb.Frame(self.parent)
        self.frame_games = tb.Frame(self.parent)
        self.frame.grid(column=0, row=0)
        self.frame_games.grid(column=0, row=1)
        self.header = Label(
            self.frame,
            (0, 0),
            'Game Arcade',
            customizations={
                'font': ('Helvetica', 24),
                'justify': CENTER,
                'columnspan': 3,
                'padding': 20,
            },
        )

        self.game1_button = tb.Button(
            self.frame,
            text='Game 1',
            padding=5,
            command=lambda: self.on_click_game_button('game1'),
        )
        self.game2_button = tb.Button(
            self.frame,
            text='Game 2',
            padding=5,
            command=lambda: self.on_click_game_button('game2'),
        )
        self.game1_button.grid(row=1, column=0, padx=20, pady=20)
        self.game2_button.grid(row=1, column=1, padx=20, pady=20)

    def on_click_game_button(self, game: str) -> None:
        debug(f'onclick game_button: {game}')
        self.parent.change_window(game)

    def hide(self) -> None:
        debug('Hide main window')
        self.frame.grid_remove()
        self.header.grid_remove()

    def show(self) -> None:
        debug('Show main window')
        self.frame.grid(column=0, row=0)
        self.header.grid(column=0, row=0)


App(
    title='Game Arcade v0.5',
    theme='superhero',
    size=(600, 650),
    logging_level=logging.INFO,
)
