import ttkbootstrap as tb  # type: ignore
from ttkbootstrap.constants import DISABLED, ACTIVE, CENTER, NW, NE, N  # type: ignore
from random import randint, choice
import math
import logging
from logging import debug, info, error
import threading
import json
from typing import Callable


class App(tb.Window):
    def __init__(
        self, title: str, size: tuple, theme="darkly", logging_level=logging.INFO
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
            format="%(asctime)s %(levelname)s: %(message)s",
            datefmt="%I:%M:%S",
            level=logging_level,
        )
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])
        self.highscores = self.get_highscores()

        self.style.configure("TButton", font=("Helvetica", 18))
        self.main = Main(self)
        self.game1 = Game1(self)
        self.game2 = Game2(self)
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

    def get_current_highscore(self) -> int:
        return self.current_highscore

    def set_highscore(self, game: str, value: int) -> None:
        try:
            self.highscores[game] = value
            with open("highscores.json", "w") as f:
                debug(f"Writing to json: {self.highscores}")
                json.dump(self.highscores, f)
        except Exception as e:
            error(e)
            pass

    def change_window(self, window: str) -> None:
        self.main.hide()
        self.game1.hide()
        self.game2.hide()
        if window == "game1":
            self.game1.show()
        elif window == "game2":
            self.game2.show()
        elif window == "main":
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
            "Game Arcade",
            customizations={
                "font": ("Helvetica", 24),
                "justify": CENTER,
                "columnspan": 3,
                "padding": 20,
            },
        )

        self.game1_button = tb.Button(
            self.frame,
            text="Game 1",
            padding=5,
            command=lambda: self.on_click_game_button("game1"),
        )
        self.game2_button = tb.Button(
            self.frame,
            text="Game 2",
            padding=5,
            command=lambda: self.on_click_game_button("game2"),
        )
        self.game1_button.grid(row=1, column=0, padx=20, pady=20)
        self.game2_button.grid(row=1, column=1, padx=20, pady=20)

    def on_click_game_button(self, game: str) -> None:
        debug(f"onclick game_button: {game}")
        self.parent.change_window(game)

    def hide(self) -> None:
        debug("Hide main window")
        self.frame.grid_remove()
        self.header.grid_remove()

    def show(self) -> None:
        debug("Show main window")
        self.frame.grid(column=0, row=0)
        self.header.grid(column=0, row=0)


class Game1(tb.Frame):
    def __init__(
        self, parent, starting_score=100, target_score=0, max_highscore=100
    ) -> None:
        """
        # Game 1 window
        Window is hidden by default. Can be initialized by using show() and hidden by using hide()
        ## Description
        'Goal', 'Current Score' and 'You win' labels are on first row.
        'Try again' button appears when game is over.
        Buttons 1-4 are on second row in a form of a card.
        """
        self.parent = parent

        self.target_score = target_score
        self.starting_score = starting_score
        self.current_score = starting_score
        self.highscore = self.parent.get_highscore("game1")
        self.max_highscore = max_highscore
        self.current_highscore = self.max_highscore

        self.frame_top_left = tb.Frame(self.parent, padding=0, width=0)
        self.frame_top_right = tb.Frame(self.parent, padding=0, width=0)
        self.frame = tb.Frame(self.parent, padding=0, width=2)
        self.frame_cards = tb.Frame(self.parent, padding=0, width=2)

        self.back_button = tb.Button(
            self.frame_top_left, text="Quit", command=lambda: self.quit_game()
        )
        self.back_button.grid(row=0, column=0)

        self.current_highscore_label = Label(
            self.frame_top_left,
            (0, 1),
            f"Current score: {self.current_highscore}",
            {"font": ("Arial", 14)},
        )
        self.highscore_label = Label(
            self.frame_top_right,
            (0, 0),
            f"Highscore: {self.highscore}",
            {"font": ("Arial", 14)},
        )

        self.win_label = Label(self.frame, (0, 0), "")
        self.goal_label = Label(self.frame, (1, 1), f"Goal: {self.target_score}")
        self.try_again_button = tb.Button(
            self.frame, text="Play again", command=self.play_again
        )
        self.current_score_label = Label(
            self.frame, (2, 1), f"Current: {self.current_score}"
        )
        self.card1 = self.init_card(self.frame_cards, 3, 0, "addition", 0)
        self.card2 = self.init_card(self.frame_cards, 3, 1, "subtraction", 1)
        self.card3 = self.init_card(self.frame_cards, 3, 2, "multiplication", 2)
        self.card4 = self.init_card(self.frame_cards, 3, 3, "division", 3)

    def get_card_style(self, card_type: str) -> str:
        if card_type == "multiplication" or card_type == "division":
            return "custom.Success.TButton"
        elif card_type == "round_up" or card_type == "round_down":
            return "custom.Info.TButton"
        else:
            return "custom.Primary.TButton"

    def init_card(self, frame, row=0, column=0, card_type="addition", card_index=0):
        return CardButton(
            frame,
            (row, column),
            Card(card_type, card_index),
            customizations={
                "on_click": self.on_click_card,
                "style": self.get_card_style(card_type),
            },
        )

    def game_over(self) -> bool:
        return self.target_score == self.current_score

    def quit_game(self) -> None:
        self.reset_game()
        self.parent.change_window("main")

    def reset_game(self) -> None:
        info("Reset game")
        self.current_highscore = self.max_highscore
        self.current_score = self.starting_score
        self.reinit_card(self.card1, "addition")
        self.reinit_card(self.card2, "subtraction")
        self.reinit_card(self.card3, "multiplication")
        self.reinit_card(self.card4, "division")

        self.try_again_button.grid_remove()
        self.win_label.change_label("")
        self.enable_cards()
        self.current_highscore_label.change_label(self.current_highscore)
        self.current_score_label.change_label(self.current_score)


    def hide(self) -> None:
        self.frame.grid_remove()
        self.frame_cards.grid_remove()
        self.frame_top_left.grid_remove()
        self.frame_top_right.grid_remove()

    def show(self) -> None:
        self.frame_top_left.grid(column=0, row=0, sticky=NW)
        self.frame_top_right.grid(column=0, row=0, sticky=NE)
        self.frame.grid(column=0, row=1, sticky=N)
        self.frame_cards.grid(column=0, row=2, sticky=N)

    def play_again(self) -> None:
        info("Play again button pressed")
        self.try_again_button.grid_remove()
        self.win_label.change_label("")
        self.set_current_score(self.starting_score)
        self.reset_current_highscore()
        self.current_highscore_label.change_label(self.current_highscore)
        self.current_score_label.change_label(self.current_score)
        self.reinit_card(self.card1, "addition")
        self.reinit_card(self.card2, "subtraction")
        self.reinit_card(self.card3, "multiplication")
        self.reinit_card(self.card4, "division")
        self.enable_cards()

    def set_current_highscore(self, value: int) -> None:
        if self.current_highscore > self.highscore:
            self.highscore = self.current_highscore
            self.parent.set_highscore("game1", self.highscore)

    def reset_current_highscore(self) -> None:
        self.current_highscore = self.max_highscore

    def disable_cards(self) -> None:
        info("All cards disabled")
        self.card1.disable()
        self.card2.disable()
        self.card3.disable()
        self.card4.disable()

    def enable_cards(self) -> None:
        info("All cards enabled")
        self.card1.enable()
        self.card2.enable()
        self.card3.enable()
        self.card4.enable()

    # Used when clicking card and 'play again'

    def set_current_score(self, value: int) -> None:
        starting_score = self.starting_score
        if value > starting_score:
            self.current_score = starting_score
        elif value < starting_score * -1:
            self.current_score = starting_score * -1
        else:
            self.current_score = value

    def reinit_card(self, card, operation=None) -> None:
        info("Reiniting card")
        card_class = card.get_card()
        debug(f"Reiniting card: {card_class}")
        card_class.reinit_card(operation)
        card.update_text(self.get_card_style(card_class.card_type))

    def update_current_highscore(self) -> None:
        if self.current_highscore > 0:
            self.current_highscore -= 1

    def on_click_card(self, card) -> None:
        info("Clicked card")
        debug(f"Clicked: {card.get_card_text()}")
        current_score = self.current_score
        card_obj = card.get_card()
        card_value = card_obj["value"]
        card_index = card_obj["index"]
        if card.operator == "+":
            debug(
                f"Addition -> round(current_score+card_value, 1) = {round(current_score+card_value, 1)}"
            )
            self.set_current_score(round(current_score + card_value, 1))
        elif card.operator == "-":
            debug(
                f"Subtraction -> round(current_score+card_value, 1) = {round(current_score-card_value, 1)}"
            )
            self.set_current_score(round(current_score - card_value, 1))
        elif card.operator == "*":
            debug(
                f"Multiplication -> round(current_score*card_value, 1) = {round(current_score*card_value, 1)}"
            )
            self.set_current_score(round(current_score * card_value, 1))
        elif card.operator == "/":
            debug(
                f"Division -> round(current_score/card_value, 1) = {round(current_score/card_value, 1)}"
            )
            self.set_current_score(round(current_score / card_value, 1))
        elif card.operator == "round_up":
            debug(f"Round up -> math.ceil(current_score) = {math.ceil(current_score)}")
            self.set_current_score(math.ceil(current_score))
        elif card.operator == "round_down":
            debug(
                f"Round down -> math.floor(current_score) = {math.floor(current_score)}"
            )
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
            text=f"Score: {self.current_highscore}"
        )
        debug(f"Current score is now: {self.current_score}")

        if self.game_over():
            info("Game ended")
            self.win_label.change_label("You win!")
            self.disable_cards()
            self.try_again_button.grid(row=0, column=4)
            if self.current_highscore > self.highscore:
                self.parent.set_highscore("game1", self.current_highscore)
                self.highscore_label.change_label(
                    f"Highscore: {self.current_highscore}"
                )


# TODO:
# - When growing the location is wrong sometimes:
#   - must watch the previous worm-part movement direction istead of the first worm-part


class Game2(tb.Frame):
    def __init__(self, parent) -> None:
        """
        # Game 2 window
        Window is hidden by default. Can be initialized by using show() and hidden by using hide()
        ## Description
        Simple worm game where the player moves using buttons or 'WASD' eating the * and growing size.
        Game ends when player collides with itself
        """
        self.parent = parent
        self.highscore = self.parent.get_highscore("game1")

        self.frame_top_left = tb.Frame(self.parent, padding=0, width=0)
        self.frame_top_right = tb.Frame(self.parent, padding=10, width=10)
        self.frame = tb.Frame(self.parent, padding=0, width=0)

        self.back_button = tb.Button(
            self.frame_top_left, text="Quit", command=lambda: self.quit_game()
        )
        self.back_button.grid(row=0, column=0)

        self.go_right_button = tb.Button(
            self.frame_top_right,
            text="Move Right",
            command=lambda: self.set_movement_direction("RIGHT"),
        )

        self.go_left_button = tb.Button(
            self.frame_top_right,
            text="Move Left",
            command=lambda: self.set_movement_direction("LEFT"),
        )
        self.go_left_button.grid(row=0, column=0)
        self.go_right_button.grid(row=0, column=1)

        self.go_up_button = tb.Button(
            self.frame_top_right,
            text="Move Up",
            command=lambda: self.set_movement_direction("UP"),
        )

        self.go_down_button = tb.Button(
            self.frame_top_right,
            text="Move Down",
            command=lambda: self.set_movement_direction("DOWN"),
        )
        self.go_up_button.grid(row=1, column=0, pady=5)
        self.go_down_button.grid(row=1, column=1, pady=5)

        self.current_movement_dir = "RIGHT"
        self.passed_time = 0.0
        self.t = None  # type: ignore
        self.food_position = (0, 8)

        # Init board -> make function
        self.board = []
        for row in range(10):
            for column in range(10):
                column_label = Label(
                    self.frame,
                    row_and_column=(row, column),
                    text="_",
                    customizations={"padding": "1 -4"},
                )
                self.board.append(column_label)

        self.worm = self.Worm(self, self.frame)

    def spawn_food(self, test=False) -> None:
        if test:
            debug("Test spawn enabled, spawning to 5,0")
            for child in self.board:
                row, col = child.get_row_and_column()

                if row == 5 and col == 0:
                    child.change_label("*")
                    self.food_position = (5, 0)
                    break
            return
        free_spots = []
        for child in self.board:
            spot_char = child.get_text()
            if spot_char == "_":
                row, col = child.get_row_and_column()
                free_spots.append((row, col))
            else:
                debug(f"Not a free spot: {child.get_row_and_column()}")

        choose_spot = choice(free_spots)

        for child in self.board:
            row, col = child.get_row_and_column()

            if row == choose_spot[0] and col == choose_spot[1]:
                debug(
                    "Spawning food: ",
                )
                child.change_label("*")
                self.food_position = (choose_spot[0], choose_spot[1])
                break

        debug(f"FOOD POS:{self.food_position}")

    def set_movement_direction(self, direction: str) -> None:
        self.current_movement_dir = direction

    def update_frame(self) -> None:
        self.t = threading.Timer(0.8, self.update_frame)  # type: ignore
        self.t.start()  # type: ignore
        self.passed_time += 0.8
        info(f"Frame updated, passed time: {self.passed_time}s")
        self.worm.update_position(self.current_movement_dir)

    def quit_game(self) -> None:
        self.t.cancel()  # type: ignore
        self.parent.change_window("main")

    def hide(self) -> None:
        self.frame.grid_remove()
        self.frame_top_left.grid_remove()
        self.frame_top_right.grid_remove()

    def show(self) -> None:
        self.frame_top_left.grid(column=0, row=0, sticky=NW)
        self.frame_top_right.grid(column=1, row=0, sticky=NE)
        self.frame.grid(column=0, row=1, sticky=N)
        self.update_frame()
        self.spawn_food(test=False)

    def play_again(self) -> None:
        info("Play again button pressed")

    def set_current_highscore(self, value: int):
        if self.current_highscore > self.highscore:
            self.highscore = self.current_highscore
            self.parent.set_highscore("game1", self.highscore)

    def reset_current_highscore(self) -> None:
        self.current_highscore = self.max_highscore

    def update_current_highscore(self) -> None:
        if self.current_highscore > 0:
            self.current_highscore -= 1

    # TODO:
    # Implement this
    def game_over(self) -> None:
        pass

    def food_eaten(self) -> None:
        for child in self.board:
            row, col = child.get_row_and_column()
            if child.get_text() == "*":
                debug(
                    "removing food ",
                )
                child.change_label("_")
                break
        self.spawn_food()

    class Worm(tb.Frame):
        def __init__(self, root, parent, length=1, char="O") -> None:
            self.root = root
            self.length = length
            self.char = char
            self.position = [[0, 1]]
            self.parent = parent
            self.worm1 = tb.Label(self.parent, text=self.char)
            self.worm1.grid(row=0, column=1)

            self.worm2 = tb.Label(self.parent, text=self.char)
            self.worm3 = tb.Label(self.parent, text=self.char)
            self.worm4 = tb.Label(self.parent, text=self.char)
            self.worm5 = tb.Label(self.parent, text=self.char)
            self.worm6 = tb.Label(self.parent, text=self.char)

        def eat_food(self) -> None:
            food_pos = self.root.food_position

            if food_pos == (self.position[0][0], self.position[0][1]):
                debug("EAT FOOD")
                self.root.food_eaten()
                self.add_length()
                self.grow_worm()

        def grow_worm(self) -> None:
            current_dir = self.root.current_movement_dir
            row_diff = 0
            col_diff = 0
            if current_dir == "RIGHT":
                col_diff -= 1
            elif current_dir == "LEFT":
                col_diff += 1
            elif current_dir == "UP":
                row_diff += 1
            elif current_dir == "DOWN":
                row_diff -= 1

            if self.length == 2:
                row = row_diff + self.position[0][0]
                col = col_diff + self.position[0][1]
                self.position.append([row, col])
                self.worm2.grid(row=row, column=col)
            elif self.length == 3:
                row = row_diff + self.position[1][0]
                col = col_diff + self.position[1][1]
                self.position.append([row, col])
                self.worm3.grid(row=row, column=col)
            elif self.length == 4:
                row = row_diff + self.position[2][0]
                col = col_diff + self.position[2][1]
                self.position.append([row, col])
                self.worm4.grid(row=row, column=col)
            elif self.length == 5:
                row = row_diff + self.position[3][0]
                col = col_diff + self.position[3][1]
                self.position.append([row, col])
                self.worm5.grid(row=row, column=col)
            elif self.length == 6:
                row = row_diff + self.position[4][0]
                col = col_diff + self.position[4][1]
                self.position.append([row, col])
                self.worm6.grid(row=row, column=col)

        def add_length(self) -> None:
            self.length += 1

        def update_position(self, direction: str) -> None:
            debug(f"Moved: {direction}")
            curr_worm = 0
            old_pos_row = 0
            old_pos_col = 0
            for pos in self.position:
                temp_row = pos[0]
                temp_col = pos[1]
                if curr_worm == 0:
                    if direction == "LEFT" and pos[1] > 0:
                        pos[1] -= 1
                    if direction == "RIGHT" and pos[1] < 9:
                        pos[1] += 1
                    if direction == "UP" and pos[0] > 0:
                        pos[0] -= 1
                    if direction == "DOWN" and pos[0] < 9:
                        pos[0] += 1
                else:
                    pos[0] = old_pos_row
                    pos[1] = old_pos_col

                debug(f"Pos {curr_worm}: {pos}")
                if curr_worm == 0:
                    self.worm1.grid_configure(row=pos[0], column=pos[1])
                if curr_worm == 1:
                    self.worm2.grid_configure(row=old_pos_row, column=old_pos_col)
                if curr_worm == 2:
                    self.worm3.grid_configure(row=old_pos_row, column=old_pos_col)
                if curr_worm == 3:
                    self.worm4.grid_configure(row=old_pos_row, column=old_pos_col)
                if curr_worm == 4:
                    self.worm5.grid_configure(row=old_pos_row, column=old_pos_col)
                if curr_worm == 5:
                    self.worm6.grid_configure(row=old_pos_row, column=old_pos_col)

                old_pos_row = temp_row
                old_pos_col = temp_col

                curr_worm += 1

            self.eat_food()


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
        if self.card_type == "multiplication" or self.card_type == "division":
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
        return f"{self.operator}{self.value}"

    def init_value_and_operator(self):
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
            self.value = "Round\nup"
            self.operator = "round_up"
        elif self.card_type == "round_down":
            self.value = "Round\ndown"
            self.operator = "round_down"
        else:
            debug("Invalid card_type:", self.card_type)

    def get_card(self) -> dict:
        return {"value": self.value, "index": self.index, "operator": self.operator}

    def reinit_card(self, operation=None):
        if operation:
            self.card_type = operation
        else:
            self.card_type = choice(
                [
                    "addition",
                    "subtraction",
                    "multiplication",
                    "division",
                    "round_up",
                    "round_down",
                ]
            )
        if self.card_type == "multiplication" or self.card_type == "division":
            self.value = randint(self.min_value, self.max_value // 2)
        else:
            self.value = randint(self.min_value, self.max_value)
        self.init_value_and_operator()
        info("Card has been updated")
        debug(f"Card updated {self.get_card()}")


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
            "width": 8,
            "height": 5,
            "padx": 8,
            "pady": 10,
            "style": "TButton",
            "on_click": self.on_click,
        }
        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        self.binded_command: Callable[[Card], None] = default_customizations["on_click"]  # type: ignore
        row, col = row_and_column
        width = default_customizations["width"]
        self.height = default_customizations["height"]
        padx = default_customizations["padx"]
        pady = default_customizations["pady"]
        style = default_customizations["style"]

        self.card = card
        text = self.card.get_card_text()
        break_count = text.count("\n")

        for i in range((self.height - break_count) // 2):
            text += "\n"
            text = "\n" + text

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
        break_count = text.count("\n")

        debug(f"breakcount: {break_count}")

        for i in range((self.height - break_count) // 2):
            text += "\n"
            text = "\n" + text

        if break_count > 0:
            text = text[:-1]

        self.button.configure(text=text, bootstyle=style)
        debug(f"Card style is now: {style}")


class Label(tb.Frame):
    def __init__(
        self, parent, row_and_column: tuple, text: str, customizations=None
    ) -> None:
        """
        Ttkbootstrap Label with customizations
        ### Parameters:
        - row_and_column: tuple with row and column values - (0, 0)
        - text: What is shown in the label
        - customizations: {'sticky': None, 'columnspan': 1, 'justify': 'left', 'font': ('Arial', 20), 'padding': 0}
        """
        super().__init__(parent)

        default_customizations = {
            "sticky": None,
            "columnspan": 1,
            "justify": "left",
            "font": ("Arial", 20),
            "padding": 0,
        }

        if customizations is not None:
            for key, value in customizations.items():
                default_customizations[key] = value

        sticky = default_customizations["sticky"]
        colspan = default_customizations["columnspan"]
        justify = default_customizations["justify"]
        font = default_customizations["font"]
        padding = default_customizations["padding"]

        self.row, self.col = row_and_column

        self.label = tb.Label(
            parent, text=text, justify=justify, font=font, padding=padding
        )

        self.label.grid(
            row=self.row, column=self.col, columnspan=colspan, sticky=sticky
        )

    def get_text(self) -> str:
        return self.label.cget("text")

    def get_row_and_column(self) -> tuple:
        return (self.row, self.col)

    def change_label(self, text: str) -> None:
        self.label.configure(text=text)


App(
    title="Awesome Card Game v0.3",
    theme="superhero",
    size=(600, 650),
    logging_level=logging.DEBUG,
)
