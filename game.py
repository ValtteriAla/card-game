import ttkbootstrap as tb
from ttkbootstrap.constants import *
from random import randint, choice
import math
import logging
from logging import debug, info, error
import json


class App(tb.Window):
    def __init__(self, title, size, theme='darkly', target_score=0, starting_score=100, logging_level=logging.INFO):
        '''
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
        '''
        super().__init__(themename=theme)
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt='%I:%M:%S',
                            level=logging_level)
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.highscores = self.get_highscores()

        self.style.configure('TButton', font=('Helvetica', 18))
        self.main = Main(self)
        self.game1 = None
        self.mainloop()

    def get_highscores(self) -> dict:
        try:
            with open("highscores.json", "r") as f:
                highscores = json.load(f)
                return highscores
        except Exception as e:
            error(e)
            return {"game1": 0}

    def get_highscore(self, game: str) -> int:
        if self.highscores.get(game):
            return self.highscores[game]
        else:
            error(f"Invalid game name; '{game}' while getting highscore")
            return 0

    def set_highscore(self, game: str, value: int):
        try:
            self.highscores[game] = value
            with open('highscores.json', 'w') as f:
                debug(f"Writing to json: {
                      self.highscores}")
                json.dump(self.highscores, f)
        except Exception as e:
            error(e)
            pass


    def get_current_highscore(self) -> int:
        return self.current_highscore

    def change_window(self, window: str):
        if window == "game1":
            self.game1 = Game1(self)
        elif window == "main":
            self.main = Main(self)
        else:
            self.main = Main(self)


class Main(tb.Frame):
    def __init__(self, parent):
        '''
        # Main window
        ## Game 1: 
        4 cards with different operations, the goal is to get the target score 0
        '''
        self.parent = parent
        self.frame = tb.Frame(self.parent)
        self.frame_games = tb.Frame(self.parent)
        self.frame.grid(column=0, row=0)
        self.frame_games.grid(column=0, row=1)
        self.header = Label(self.frame, (0, 4), "Game Arcade",
                            customizations={"font": ('Helvetica', 24),
                                            "justify": CENTER, "columnspan": 3,
                                            "padding": 20})

        self.game1_button = tb.Button(
            self.frame, text="Game 1", padding=5, command=lambda: self.on_click_game_button("game1"))
        self.game1_button.grid(row=1, column=0, padx=20, pady=20)

    def on_click_game_button(self, game: str):
        self.parent.change_window(game)
        self.destroy()

    def destroy(self):
        self.frame.destroy()
        self.header.destroy()
        self.game1_button.destroy()


class Game1(tb.Frame):
    def __init__(self, parent, starting_score=100, target_score=0, max_highscore=100):
        '''
        # Game 1 window
        'Goal', 'Current Score' and 'You win' labels are on first row.
        'Try again' button appears when game is over.
        Buttons 1-4 are on second row in a form of a card.
        '''
        self.parent = parent

        self.target_score = target_score
        self.starting_score = starting_score
        self.current_score = starting_score
        self.highscore = self.parent.get_highscore("game1")
        self.max_highscore = max_highscore
        self.current_highscore = self.max_highscore


        default_button_width = 30
        self.frame_top_left = tb.Frame(self.parent, padding=0, width=0)
        self.frame_top_right = tb.Frame(self.parent, padding=0, width=0)
        self.frame = tb.Frame(self.parent, padding=0, width=2)
        self.frame_cards = tb.Frame(self.parent, padding=0, width=2)

        self.frame_top_left.grid(column=0, row=0, sticky=NW)
        self.frame_top_right.grid(column=0, row=0, sticky=NE)
        self.frame.grid(column=0, row=1, sticky=N)
        self.frame_cards.grid(column=0, row=2, sticky=N)

        self.back_button = tb.Button(
            self.frame_top_left, text="Quit", command=lambda: self.quit_game())
        self.back_button.grid(row=0, column=0)

        self.current_highscore_label = Label(self.frame_top_left, (0, 1), f'Current score: {
                                             self.current_highscore}', {'font': ('Arial', 14)})
        self.highscore_label = Label(self.frame_top_right, (0, 0), f'Highscore: {
                                     self.highscore}', {'font': ('Arial', 14)})

        self.win_label = Label(self.frame, (0, 0), '')
        self.goal_label = Label(self.frame, (1, 1),
                                f'Goal: {self.target_score}')
        self.try_again_button = tb.Button(self.frame,
                                          text='Play again',
                                          command=self.play_again)
        self.current_score_label = Label(self.frame, (2, 1),
                                   f'Current: {self.current_score}')
        self.card1 = self.init_card(self.frame_cards, 3, 0, 'addition', 0)
        self.card2 = self.init_card(self.frame_cards, 3, 1, 'subtraction', 1)
        self.card3 = self.init_card(
            self.frame_cards, 3, 2, 'multiplication', 2)
        self.card4 = self.init_card(self.frame_cards, 3, 3, 'division', 3)

    def quit_game(self):
        self.parent.change_window("main")
        self.destroy_self()

    def destroy_self(self):
        self.frame.destroy()
        self.frame_cards.destroy()
        self.frame_top_left.destroy()
        self.frame_top_right.destroy()
        self.win_label.destroy()
        self.goal_label.destroy()
        self.try_again_button.destroy()
        self.current_score_label.destroy()
        self.back_button.destroy()
        self.highscore_label.destroy()

    def play_again(self):
        info("Play again button pressed")
        self.try_again_button.grid_remove()
        self.win_label.change_label('')
        self.set_current_score(self.starting_score)
        self.reset_current_highscore()
        self.current_highscore_label.change_label(self.current_highscore)
        self.current_score_label.change_label(self.current_score)
        self.reinit_card(self.card1, 'addition')
        self.reinit_card(self.card2, 'subtraction')
        self.reinit_card(self.card3, 'multiplication')
        self.reinit_card(self.card4, 'division')
        self.enable_cards()

    def set_current_highscore(self, value: int):
        if self.current_highscore > self.highscore:
            self.highscore = self.current_highscore
            self.parent.set_highscore("game1", self.highscore)

    def reset_current_highscore(self):
        self.current_highscore = self.max_highscore
    # Used on start
    def init_card(self, frame, row=0, column=0, card_type='addition', card_index=0):
        return CardButton(frame, (row, column), Card(card_type, card_index),
                          customizations={'on_click': self.on_click_card, 'style': self.get_card_style(card_type)})

    def get_card_style(self, card_type: str) -> str:
        if card_type == "multiplication" or card_type == "division":
            return 'custom.Success.TButton'
        elif card_type == "round_up" or card_type == "round_down":
            return 'custom.Info.TButton'
        else:
            return 'custom.Primary.TButton'

    def disable_cards(self):
        info("All cards disabled")
        self.card1.disable()
        self.card2.disable()
        self.card3.disable()
        self.card4.disable()

    def enable_cards(self):
        info("All cards enabled")
        self.card1.enable()
        self.card2.enable()
        self.card3.enable()
        self.card4.enable()
    # Used when clicking card and 'play again'

    def set_current_score(self, value: int):
        starting_score = self.starting_score
        if value > starting_score:
            self.current_score = starting_score
        elif value < starting_score*-1:
            self.current_score = starting_score*-1
        else:
            self.current_score = value

    def reinit_card(self, card, operation=None):
        info("Reiniting card")
        card_class = card.get_card()
        debug(f"Reiniting card: {card_class.get_card_text()}")
        card_class.reinit_card(operation)
        card.update_text(self.get_card_style(card_class.card_type))

    def update_current_highscore(self):
        if self.current_highscore > 0:
            self.current_highscore -= 1

    def on_click_card(self, card):
        info("Clicked card")
        debug(f"Clicked: {card.get_card_text()}")
        current_score = self.current_score
        card_obj = card.get_card()
        card_value = card_obj['value']
        card_index = card_obj['index']
        if card.operator == '+':
            debug(
                f"Addition -> round(current_score+card_value, 1) = {round(current_score+card_value, 1)}")
            self.set_current_score(round(current_score+card_value, 1))
        elif card.operator == '-':
            debug(f"Subtraction -> round(current_score+card_value, 1) = {
                  round(current_score-card_value, 1)}")
            self.set_current_score(round(current_score-card_value, 1))
        elif card.operator == '*':
            debug(f"Multiplication -> round(current_score*card_value, 1) = {
                  round(current_score*card_value, 1)}")
            self.set_current_score(round(current_score*card_value, 1))
        elif card.operator == '/':
            debug(
                f"Division -> round(current_score/card_value, 1) = {round(current_score/card_value, 1)}")
            self.set_current_score(round(current_score/card_value, 1))
        elif card.operator == 'round_up':
            debug(
                f"Round up -> math.ceil(current_score) = {math.ceil(current_score)}")
            self.set_current_score(math.ceil(current_score))
        elif card.operator == 'round_down':
            debug(
                f"Round down -> math.floor(current_score) = {math.floor(current_score)}")
            self.set_current_score(math.floor(current_score))

        if card_index == 0:
            self.reinit_card(self.card1)
            debug(f"Card 1 is now: {self.card1.get_card().get_card_text()}")
        elif card_index == 1:
            self.reinit_card(self.card2)
            debug(f"Card 2 is now: {self.card2.get_card().get_card_text()}")
        elif card_index == 2:
            self.reinit_card(self.card3)
            debug(f"Card 3 is now: {self.card3.get_card().get_card_text()}")
        elif card_index == 3:
            self.reinit_card(self.card4)
            debug(f"Card 4 is now: {self.card4.get_card().get_card_text()}")

        self.update_current_highscore()
        self.current_score_label.change_label(text=self.current_score)
        self.current_highscore_label.change_label(
            text=f"Score: {self.current_highscore}")
        debug(f"Current score is now: {self.current_score}")

        if self.game_over():
            info('Game ended')
            self.win_label.change_label('You win!')
            self.disable_cards()
            self.try_again_button.grid(row=0, column=4)
            if self.current_highscore > self.highscore:
                self.parent.set_highscore("game1", self.current_highscore)
                self.highscore_label.change_label(
                    f'Highscore: {self.current_highscore}')

    def game_over(self):
        return self.target_score == self.current_score

class Card():
    def __init__(self, card_type: str, index: int, min_value=1, max_value=50):
        '''
        # Card
        Has stored operation type, value and index. Used in CardButton
        ### Parameters:
        - card_type: 'addition', 'subtraction', 'multiplication', 'division', 'round_up', 'round_down'
        - index: Required identifier for updating this card, has to be number 0-3
        - min_value: minimum value that this card's value can get, default=1
        - max_value: maximum value that this card's value can get, default=50
        '''
        self.card_type = card_type
        if self.card_type == "multiplication" or self.card_type == "division":
            self.value = randint(min_value, max_value//2)
        else:
            self.value = randint(min_value, max_value)
        self.index = index
        self.operator = None
        self.min_value = min_value
        self.max_value = max_value

        self.init_value_and_operator()

    def get_card_text(self):
        if len(self.operator) > 1:
            return self.value
        return f'{self.operator}{self.value}'

    def init_value_and_operator(self):
        if self.card_type == 'addition':
            self.operator = '+'
        elif self.card_type == 'subtraction':
            self.operator = '-'
        elif self.card_type == 'multiplication':
            self.value *= choice([-1, 1])
            self.operator = '*'
        elif self.card_type == 'division':
            self.value *= choice([-1, 1])
            self.operator = '/'
        elif self.card_type == 'round_up':
            self.value = 'Round\nup'
            self.operator = 'round_up'
        elif self.card_type == 'round_down':
            self.value = 'Round\ndown'
            self.operator = 'round_down'
        else:
            debug('Invalid card_type:', self.card_type)

    def get_card(self) -> dict:
        return {'value': self.value, 'index': self.index, 'operator': self.operator}

    def reinit_card(self, operation=None):
        if operation:
            self.card_type = operation
        else:
            self.card_type = choice(['addition', 'subtraction', 'multiplication',
                                    'division', 'round_up', 'round_down'])
        if self.card_type == "multiplication" or self.card_type == "division":
            self.value = randint(self.min_value, self.max_value//2)
        else:
            self.value = randint(self.min_value, self.max_value)
        self.init_value_and_operator()
        info("Card has been updated")
        debug(f'Card updated {self.get_card()}')


class CardButton(tb.Frame):
    def __init__(self, parent, row_and_column: tuple, card: Card, customizations: {}):
        '''
        # CardButton
        Button widget that has appearance of a card and uses Card's properties.
        ### Parameters:
        - parent: parent to which this widget belongs
        - row_and_column: as a tuple (row, column)
        - card: Instance of a Card class
        - customizations: default={'width': 12, 'height': 5, 'padx': 5,
                          'style': 'TButton',
                          'on_click': self.on_click, }
        '''
        self.parent = parent

        default_customizations = {
            'width': 8, 'height': 5, 'padx': 8, 'pady': 10,
            'style': 'TButton',
            'on_click': self.on_click, }
        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        self.binded_command = default_customizations['on_click']
        row, col = row_and_column
        width = default_customizations['width']
        self.height = default_customizations['height']
        padx = default_customizations['padx']
        pady = default_customizations['pady']
        style = default_customizations['style']

        self.card = card
        text = self.card.get_card_text()
        break_count = text.count('\n')

        for i in range((self.height - break_count)//2):
            text += '\n'
            text = '\n' + text

        self.button = tb.Button(self.parent, text=text, width=width,
                                bootstyle=style,
                                command=self.on_click,
                                )
        self.button.grid(row=row, column=col, padx=padx, pady=pady)

    def on_click(self):
        self.binded_command(self.card)

    def disable(self):
        self.button.configure(state=DISABLED)

    def enable(self):
        self.button.configure(state=ACTIVE)

    def get_card(self):
        return self.card

    def update_text(self, style: str):
        text = self.card.get_card_text()
        break_count = text.count('\n')

        debug(f"breakcount: {break_count}")

        for i in range((self.height - break_count)//2):
            text += '\n'
            text = '\n' + text

        if break_count > 0:
            text = text[:-1]

        self.button.configure(text=text, bootstyle=style)
        debug(f"Card style is now: {style}")


class Label(tb.Frame):
    def __init__(self, parent, row_and_column: tuple, text: str, customizations=None):
        '''
        ttkbootstrap Label with customizations
        ### Parameters:
        - row_and_column: tuple with row and column values - (0, 0)
        - text: What is shown in the label
        - customizations: {'sticky': None, 'columnspan': 1, 'justify': 'left', 'font': ('Arial', 20), 'padding': 0}
        '''
        super().__init__(parent)

        default_customizations = {'sticky': None,
                                  'columnspan': 1,
                                  'justify': 'left',
                                  'font': ('Arial', 20),
                                  'padding': 0}

        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        sticky = default_customizations['sticky']
        colspan = default_customizations['columnspan']
        justify = default_customizations['justify']
        font = default_customizations['font']
        padding = default_customizations['padding']

        row, col = row_and_column

        self.label = tb.Label(
            parent, text=text, justify=justify, font=font, padding=padding)
        self.label.grid(row=row, column=col, columnspan=colspan, sticky=sticky)

    def change_label(self, text: str):
        self.label.configure(text=text)


App(title='Awesome Card Game v0.3', theme="superhero", size=(
    600, 350), logging_level=logging.DEBUG)
