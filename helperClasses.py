import ttkbootstrap as tb  # type: ignore
from ttkbootstrap.constants import DISABLED, ACTIVE  # type: ignore
from random import randint, choice
from logging import debug, info
from typing import Callable

class Label(tb.Frame):
    def __init__(
        self, parent, row_and_column: tuple, text: str, customizations=None
    ) -> None:
        """
        Ttkbootstrap Label with customizations
        ### Parameters:
        - row_and_column: tuple with row and column values - (0, 0)
        - text: What is shown in the label
        - customizations: {'sticky': None, 'columnspan': 1, 'justify': 'left', 'font': ('Arial', 20), 'padding': 0, 'visible': True}
        """
        super().__init__(parent)

        default_customizations = {
            'sticky': None,
            'columnspan': 1,
            'justify': 'left',
            'font': ('Arial', 20),
            'padding': 0,
            'visible': True,
        }

        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        self.sticky = default_customizations['sticky']
        self.colspan = default_customizations['columnspan']
        justify = default_customizations['justify']
        font = default_customizations['font']
        padding = default_customizations['padding']
        visible = default_customizations['visible']

        self.row, self.col = row_and_column

        self.label = tb.Label(
            parent, text=text, justify=justify, font=font, padding=padding
        )

        if visible:
            self.label.grid(
                row=self.row,
                column=self.col,
                columnspan=self.colspan,
                sticky=self.sticky,
            )

    def get_text(self) -> str:
        return self.label.cget('text')

    def get_row_and_column(self) -> tuple:
        return (self.row, self.col)

    def change_label(self, text: str) -> None:
        self.label.configure(text=text)

    def visible(self) -> None:
        self.label.grid(
            row=self.row, column=self.col, columnspan=self.colspan, sticky=self.sticky
        )

    def hidden(self) -> None:
        self.label.grid_remove()


class KeyInputs:
    def __init__(self, window, callback=lambda x: 0, wasd=True):
        """
        Registers keyinputs and sends a callback which has the pressed key char in lowercase
        - callback: currently only sends the character that is being pressed
            - TODO: make event like return type
        - on_wasd=True: Checks if any of 'w,a,s,d' keys are being pressed and sends a callback
        """
        self.window = window
        self.callback = callback
        if wasd:
            window.bind('<Key>', self.on_wasd)

    def on_wasd(self, event) -> None:
        if event.char in ['W', 'A', 'S', 'D', 'w', 'a', 's', 'd']:
            self.callback(event.char.lower())



class Card:
    def __init__(self, card_type: str, index: int, min_value=1, max_value=50):
        """
        # Card
        Has stored operation type, value and index. Used in CardButton
        ### Parameters:
        - card_type: 'addition', 'subtraction', 'multiplication', 'division', 'round_up', 'round_down'
        - index: Required identifier for updating this card, has to be number 0-3
        - min_value: minimum value that this card's value can get, default=1
        - max_value: maximum value that this card's value can get, default=50
        """
        self.card_type = card_type
        if self.card_type == 'multiplication' or self.card_type == 'division':
            self.value = randint(min_value, max_value // 2)
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
            self.card_type = choice(
                [
                    'addition',
                    'subtraction',
                    'multiplication',
                    'division',
                    'round_up',
                    'round_down',
                ]
            )
        if self.card_type == 'multiplication' or self.card_type == 'division':
            self.value = randint(self.min_value, self.max_value // 2)
        else:
            self.value = randint(self.min_value, self.max_value)
        self.init_value_and_operator()
        info('Card has been updated')
        debug(f'Card updated {self.get_card()}')


class CardButton(tb.Frame):
    def __init__(
        self, parent, row_and_column: tuple, card: Card, customizations: dict
    ) -> None:
        """
        # CardButton
        Button widget that has appearance of a card and uses Card's properties.
        ### Parameters:
        - parent: parent to which this widget belongs
        - row_and_column: as a tuple (row, column)
        - card: Instance of a Card class
        - customizations: default={'width': 12, 'height': 5, 'padx': 5,
                          'style': 'TButton',
                          'on_click': self.on_click, }
        """
        self.parent = parent

        default_customizations = {
            'width': 8,
            'height': 5,
            'padx': 8,
            'pady': 10,
            'style': 'TButton',
            'on_click': self.on_click,
        }
        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        self.binded_command: Callable[[Card], None] = default_customizations['on_click']  # type: ignore
        row, col = row_and_column
        width = default_customizations['width']
        self.height = default_customizations['height']
        padx = default_customizations['padx']
        pady = default_customizations['pady']
        style = default_customizations['style']

        self.card = card
        text = self.card.get_card_text()
        break_count = text.count('\n')

        for i in range((self.height - break_count) // 2):
            text += '\n'
            text = '\n' + text

        self.button = tb.Button(
            self.parent,
            text=text,
            width=width,
            bootstyle=style,
            command=self.on_click,
        )
        self.button.grid(row=row, column=col, padx=padx, pady=pady)

    def get_card(self) -> Card:
        return self.card

    def on_click(self) -> None:
        self.binded_command(self.card)

    def disable(self) -> None:
        self.button.configure(state=DISABLED)

    def enable(self) -> None:
        self.button.configure(state=ACTIVE)

    def update_text(self, style: str) -> None:
        text = self.card.get_card_text()
        break_count = text.count('\n')

        debug(f'breakcount: {break_count}')

        for i in range((self.height - break_count) // 2):
            text += '\n'
            text = '\n' + text

        if break_count > 0:
            text = text[:-1]

        self.button.configure(text=text, bootstyle=style)
        debug(f'Card style is now: {style}')


