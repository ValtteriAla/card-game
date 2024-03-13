import ttkbootstrap as tb
from ttkbootstrap.constants import *
from random import randint, choice
import math


class App(tb.Window):
    def __init__(self, title, size, theme='darkly', target_score=0, starting_score=100):
        '''
        # Main window
        ### Parameters:
        - title: Title of the app
        - size: x and y dimensions of the window. This is also the minimum size
        - target_score: score that ends the game
        - starting_score: starting point at the start of the game
        - theme(NOT IN USE): your custom theme or one of the above:\n
                  'cosmo', 'flatly', 'litera',\n
                  'minty', 'lumen', 'sandstone', 'yeti',\n
                  'pulse', 'united', 'morph', 'journal',\n
                  'darkly', 'superhero', 'solar',\n
                  'cyborg', 'vapor', 'simplex', 'cerculean'
        '''
        super().__init__(themename=theme)
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.target_score = target_score
        self.starting_score = starting_score
        self.current_score = starting_score

        self.style.configure('TButton', font=('Helvetica', 18))

        self.main = Main(self)
        self.mainloop()

    # Not used

    def change_theme(self, theme):
        self.style.theme_use(theme)

    def get_target_score(self):
        return self.target_score

    def get_current_score(self):
        return self.current_score

    def get_starting_score(self):
        return self.starting_score

    def set_current_score(self, value: int):
        starting_score = self.get_starting_score()
        if value > starting_score:
            self.current_score = starting_score
        elif value < starting_score*-1:
            self.current_score = starting_score*-1
        else:
            self.current_score = value

    def game_over(self):
        return self.get_target_score() == self.get_current_score()


class Main(tb.Frame):
    def __init__(self, parent):
        '''
        # Main window
        'Goal', 'Current Score' and 'You win' labels are on first row.
        'Try again' button appears when game is over.
        Buttons 1-4 are on second row in a form of a card.
        '''
        self.parent = parent
        default_button_width = 30

        self.frame = tb.Frame(self.parent, padding=8, width=2)
        self.frame.grid(column=0, row=0, sticky=N)

        self.win_label = Label(self.frame, (0, 0), '')
        goal_label = Label(self.frame, (1, 0),
                           f'Goal: {self.parent.get_target_score()}')
        self.try_again_button = tb.Button(self.frame,
                                          text='Play again',
                                          command=self.play_again)
        self.current_score = Label(self.frame, (1, 1),
                                   f'Current: {self.parent.get_current_score()}')
        self.card1 = self.init_card(self.frame, 2, 0, 'addition', 0)
        self.card2 = self.init_card(self.frame, 2, 1, 'subtraction', 1)
        self.card3 = self.init_card(self.frame, 2, 2, 'multiplication', 2)
        self.card4 = self.init_card(self.frame, 2, 3, 'division', 3)

    def play_again(self):
        self.try_again_button.grid_remove()
        self.win_label.change_label('')
        self.parent.set_current_score(self.parent.get_starting_score())
        self.current_score.change_label(self.parent.get_current_score())
        self.reinit_card(self.card1, 'addition')
        self.reinit_card(self.card2, 'subtraction')
        self.reinit_card(self.card3, 'multiplication')
        self.reinit_card(self.card4, 'division')
        self.card1.enable()
        self.card2.enable()
        self.card3.enable()
        self.card4.enable()

    # Used on start and when pressing play-again
    def init_card(self, frame, row=0, column=0, card_type='addition', card_index=0):
        return CardButton(frame, (row, column), Card(card_type, card_index),
                          customizations={'on_click': self.on_click_card, 'style': 'custom.Primary.TButton'})

    def reinit_card(self, card, operation=None):
        card_class = card.get_card()
        card_class.reinit_card(operation)
        card.update_text()

    def on_click_card(self, card):
        print(card.get_card_text())
        current_score = self.parent.get_current_score()
        card_obj = card.get_card()
        card_value = card_obj['value']
        card_index = card_obj['index']
        if card.operator == '+':
            self.parent.set_current_score(round(current_score+card_value, 1))
        elif card.operator == '-':
            self.parent.set_current_score(round(current_score-card_value, 1))
        elif card.operator == '*':
            self.parent.set_current_score(round(current_score*card_value, 1))
        elif card.operator == '/':
            self.parent.set_current_score(round(current_score/card_value, 1))
        elif card.operator == 'round_up':
            self.parent.set_current_score(math.ceil(current_score))
        elif card.operator == 'round_down':
            self.parent.set_current_score(math.floor(current_score))

        if card_index == 0:
            self.reinit_card(self.card1)
        elif card_index == 1:
            self.reinit_card(self.card2)
        elif card_index == 2:
            self.reinit_card(self.card3)
        elif card_index == 3:
            self.reinit_card(self.card4)

        self.current_score.change_label(text=self.parent.get_current_score())

        if self.parent.game_over():
            print('You win')
            self.win_label.change_label('You win!')
            self.card1.disable()
            self.card2.disable()
            self.card3.disable()
            self.card4.disable()
            self.try_again_button.grid(row=0, column=3)


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
            self.value = 'Round up'
            self.operator = 'round_up'
        elif self.card_type == 'round_down':
            self.value = 'Round down'
            self.operator = 'round_down'
        else:
            print('Invalid card_type:', self.card_type)

    def get_card(self) -> dict:
        return {'value': self.value, 'index': self.index, 'operator': self.operator}

    def reinit_card(self, operation=None):
        if operation:
            self.card_type = operation
        else:
            self.card_type = choice(['addition', 'subtraction', 'multiplication',
                                    'division', 'round_up', 'round_down'])
        self.value = randint(self.min_value, self.max_value)
        self.init_value_and_operator()

        print('Card updated', self.get_card())


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
            'width': 12, 'height': 5, 'padx': 5,
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
        style = default_customizations['style']

        print("style:", style)

        self.card = card
        text = self.card.get_card_text()
        break_count = text.count('\n')

        for i in range(self.height - break_count):
            text += '\n'

        self.button = tb.Button(self.parent, text=text, width=width,
                                style=style,
                                command=self.on_click,
                                )
        self.button.grid(row=row, column=col, padx=padx)

    def on_click(self):
        self.binded_command(self.card)

    def disable(self):
        self.button.configure(state=DISABLED)
    def enable(self):
        self.button.configure(state=ACTIVE)

    def get_card(self):
        return self.card

    def update_text(self):
        text = self.card.get_card_text()
        break_count = text.count('\n')

        for i in range(self.height - break_count):
            text += '\n'

        self.button.configure(text=text)


class Label(tb.Frame):
    def __init__(self, parent, row_and_column: tuple, text: str, customizations=None):
        '''
        ttkbootstrap Label with customizations
        ### Parameters:
        - row_and_column: tuple with row and column values - (0, 0)
        - text: What is shown in the label
        - customizations: {'sticky': None, 'columnspan': 1, 'justify': 'left', 'font': ('Arial', 20)}
        '''
        super().__init__(parent)

        default_customizations = {'sticky': None,
                                  'columnspan': 1,
                                  'justify': 'left',
                                  'font': ('Arial', 20)}

        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        sticky = default_customizations['sticky']
        colspan = default_customizations['columnspan']
        justify = default_customizations['justify']
        font = default_customizations['font']

        row, col = row_and_column

        self.label = tb.Label(parent, text=text, justify=justify, font=font)
        self.label.grid(row=row, column=col, columnspan=colspan, sticky=sticky)

    def change_label(self, text: str):
        self.label.configure(text=text)


App(title='Card Game', size=(1000, 300))
