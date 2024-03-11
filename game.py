from tkinter import filedialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from random import randint, choice
import math


class App(tb.Window):
    def __init__(self, title, size, theme='darkly', target_score=0, starting_score=100):
        '''
        # Main window
        ### Parameters:
        - title: Title of the app
        - size: x and y dimensions of the window. This is also the minimum size
        - playlist: array of objects ex. [{"name": "song_name", "filepath": "path/to/file.mp3"}]
        - theme: your custom theme or one of the above:\n
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


        self.main = Main(self)
        self.mainloop()

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
        '''
        self.parent = parent
        default_button_width = 30

        self.frame = tb.Frame(self.parent, padding=8, width=2)
        self.frame.grid(column=0, row=0, sticky=N)

        self.win_label = Label(self.frame, (0, 0), "")
        Label(self.frame, (1, 0), f"Goal: {self.parent.get_target_score()}")
        self.try_again_button = tb.Button(self.frame, text="Play again", command=self.play_again)
        self.current_score = Label(self.frame, (1, 1), f"Current: {
                                    self.parent.get_current_score()}")
        self.card1 = self.init_card(self.frame, 2, 0, "addition", 0)
        self.card2 = self.init_card(self.frame, 2, 1, "subtraction",1)
        self.card3 = self.init_card(self.frame, 2, 2, "multiplication",2)
        self.card4 = self.init_card(self.frame, 2, 3, "division",3)

    def play_again(self):
        self.try_again_button.grid_remove()
        self.win_label.change_label("")
        self.parent.set_current_score(self.parent.get_starting_score())
        self.current_score.change_label(self.parent.get_current_score())
        self.card1 = self.init_card(self.frame, 2, 0, "addition", 0)
        self.card2 = self.init_card(self.frame, 2, 1, "subtraction",1)
        self.card3 = self.init_card(self.frame, 2, 2, "multiplication",2)
        self.card4 = self.init_card(self.frame, 2, 3, "division",3)

    def init_card(self, frame, row=0, column=0, card_type="addition", card_index=0):
        return CardButton(frame, (row, column), Card(card_type, card_index), customizations={'on_click': self.on_click_card})

    def on_click_card(self, card):
        print(card.get_card_text())
        current_score = self.parent.get_current_score()
        card_obj = card.get_card()
        card_value = card_obj['value']
        card_index = card_obj['index']
        if card.operator == "+":
            self.parent.set_current_score(round(current_score+card_value, 1))
        elif card.operator == "-":
            self.parent.set_current_score(round(current_score-card_value, 1))
        elif card.operator == "*":
            self.parent.set_current_score(round(current_score*card_value, 1))
        elif card.operator == "/":
                self.parent.set_current_score(round(current_score/card_value, 1))
        elif card.operator == "round_up":
            self.parent.set_current_score(math.ceil(current_score))
        elif card.operator == "round_down":
            self.parent.set_current_score(math.floor(current_score))      

        # TODO:
        # - instead of creating cards, just change the cards info.
        operation = choice(["addition", "subtraction", "multiplication", "division", "round_up", "round_down"])
        if card_index == 0:
            self.card1 = self.init_card(self.frame, 2, 0, operation, 0)
        elif card_index == 1:
            self.card2 = self.init_card(self.frame, 2, 1, operation, 1)
        elif card_index == 2:
            self.card3 = self.init_card(self.frame, 2, 2, operation, 2)
        elif card_index == 3:
            self.card4 = self.init_card(self.frame, 2, 3, operation, 3)

        self.current_score.change_label(text=self.parent.get_current_score())

        if self.parent.game_over():
            print("You win")
            self.win_label.change_label("You win!")
            self.card1.disable()
            self.card2.disable()
            self.card3.disable()
            self.card4.disable()
            self.try_again_button.grid(row=0, column=3)
            # DO LABEL changes

        


class Card():
    def __init__(self, card_type: str, index=None, min_value=1, max_value=50):
        self.card_type = card_type
        self.value = randint(min_value, max_value)
        self.index = index
        self.operator = None

        if self.card_type == "addition":
            self.operator = "+"
        elif self.card_type == "subtraction":
            self.operator = "-"
        elif self.card_type == "multiplication":
            self.value *= choice([-1, 1])
            self.operator = "*"
        elif self.card_type == "division":
            self.value *= choice([-1, 1])
            self.operator = "/"
        elif self.card_type == "round_up":
            self.value = "Round up"
            self.operator = "round_up"
        elif self.card_type == "round_down":
            self.value = "Round down"
            self.operator = "round_down"
        else:
            print("Invalid card_type:", self.card_type)

    def get_card_text(self):
        if len(self.operator) > 1:
            return self.value
        return f"{self.operator}{self.value}"

    def get_card(self) -> dict:
        return {'value': self.value, 'index': self.index, 'operator': self.operator}

class CardButton(tb.Frame):
    def __init__(self, parent, row_and_column: tuple, card: Card, customizations={}):
        '''
        '''
        super().__init__(parent)

        self.parent = parent

        default_customizations = {
            'on_click': self.on_click, "width": 20, "height": 10, "padx": 10}
        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value
        self.binded_command = default_customizations['on_click']
        row, col = row_and_column
        width = default_customizations['width']
        height = default_customizations['height']
        padx = default_customizations['padx']
        self.card = card
        text = self.card.get_card_text()
        break_count = text.count("\n")

        for i in range(height - break_count):
            text += "\n"

        self.button = tb.Button(parent, text=text, command=self.on_click, width=20)
        self.button.grid(row=row, column=col, padx=padx)

    def on_click(self):
        self.binded_command(self.card)

    def disable(self):
        self.button.configure(state=DISABLED)



class ImageWithImport(tb.Frame):
    def __init__(self, parent, row_and_column: tuple, image_path: str, image_dimensions=(150, 150), button_text='Lisää kuva', customizations={}):
        '''
        Uses tkinter Label to show the image and\n
        has button on top to load image from disk.
        '''
        super().__init__(parent)
        default_customizations = {}

        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        row, col = row_and_column
        load_image = Image.open(image_path)
        load_image = load_image.resize(image_dimensions)
        image = ImageTk.PhotoImage(load_image)

        import_picture_button = tb.Button(
            parent, text=button_text, command=lambda: self.open_image(image_dimensions))
        import_picture_button.grid(column=col, row=row)
        self.picture_field = tb.Label(parent, image=image)
        self.picture_field.image = image
        self.picture_field.grid(column=col, row=row+1, rowspan=3,
                                sticky=N)

    def open_image(self, image_dimensions: tuple):
        file_path = filedialog.askopenfilename(
            filetypes=[('Image files', '*.png;*.jpg;*.jpeg')])
        if file_path:
            load_image = Image.open(file_path)
            load_image = load_image.resize(image_dimensions)
            image = ImageTk.PhotoImage(load_image)

            self.picture_field.configure(image=image)
            self.picture_field.image = image


class Select(tb.Frame):
    def __init__(self, parent, row_and_column: tuple, values: tuple | list, placeholder: str, customizations=None):
        '''
        Uses tkinter Combobox and has on_select binding available\n
        in customizations that returns the selected value

        ### Parameters:
        - values: list or tuple of options that can be selected
        - placeholder: Text shown when nothing is selected
        - customizations: {'width': 100, 'sticky': W, 'state': 'readonly', 'pady': 5, 'on_select': self.bind_function}
        '''
        super().__init__(parent)
        default_customizations = {'width': 100,
                                  'sticky': W,
                                  'state': 'readonly',
                                  'pady': 5,
                                  'on_select': self.bind_function}

        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        state = default_customizations['state']
        width = default_customizations['width']
        pady = default_customizations['pady']
        sticky = default_customizations['sticky']
        self.binded_command = default_customizations['on_select']
        row, col = row_and_column

        self.select = tb.Combobox(parent,
                                  values=values,
                                  state=state,
                                  width=width)

        self.select.set(placeholder)
        self.select.bind('<<ComboboxSelected>>', self.on_select)
        self.select.grid(row=row, column=col, sticky=sticky, pady=pady)

    def on_select(self, e):
        selected_value = self.select.get()
        self.binded_command(selected_value)

    def bind_function(self, e):
        pass


class EntryWithLabel(tb.Frame):
    def __init__(self, parent, row_and_column: tuple, label_text: str, entry_variable=None, side_by_side=False, validate=None, customizations=None):
        '''
        ttkbootsrap Entry and Label combo.\n
        Can be positioned either label ontop or side by side

        ### Parameters:
        - label_text: What is shown in the label
        - entry_variable: Binding variable for Entry
        - side_by_side: If True then Label is shown on left side and on the same row as the Entry
        - validate: 'number'
            - 'number': Only allows numbers to be inserted to the Entry
        - customizations: {'entry-width': 30, 'label-padding': 10}
        '''

        super().__init__(parent)
        default_customizations = {'entry-width': 30,
                                  'label-padding': 10}

        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        row, col = row_and_column
        label_padding = default_customizations['label-padding']
        entry_width = default_customizations['entry-width']

        if side_by_side:
            entry_row = row
            entry_col = col + 1
        else:
            entry_row = row + 1
            entry_col = col

        label = tb.Label(parent, text=label_text, padding=label_padding)
        entry = tb.Entry(parent, textvariable=entry_variable,
                         width=entry_width)
        if validate == 'number':
            validatecommand = (self.register(self.validate_digit), '%P')
            entry.config(validate='key', validatecommand=validatecommand)

        label.grid(row=row, column=col, sticky='E')
        entry.grid(row=entry_row, column=entry_col)

    def validate_digit(self, new_text):
        if new_text.isdigit():
            return True
        elif new_text == '':
            return True
        else:
            return False


class Label(tb.Frame):
    def __init__(self, parent, row_and_column: tuple, text: str, customizations=None):
        '''
        ttkbootstrap Label with customizations
        ### Parameters:
        - row_and_column: tuple with row and column values - (0, 0)
        - text: What is shown in the label
        - customizations: {'sticky': None, 'columnspan': 1, 'justify': 'left', 'font': ("Arial", 20)}
        '''
        super().__init__(parent)

        default_customizations = {'sticky': None,
                                  'columnspan': 1,
                                  'justify': 'left',
                                  'font': ("Arial", 20)}

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


App(title='Card Game', size=(700, 300))
