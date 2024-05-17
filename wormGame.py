import threading
import ttkbootstrap as tb  # type: ignore
from ttkbootstrap.constants import NW, NE, N  # type: ignore
from helperClasses import KeyInputs, Label
from logging import debug, info
from random import choice
from tkinter import messagebox


class Game(tb.Frame):
    def __init__(self, parent) -> None:
        """
        # Game 2 window
        Window is hidden by default. Can be initialized by using show() and hidden by using hide()
        ## Description
        Simple worm game where the player moves using buttons or 'WASD' eating the * and growing size.
        Game ends when player collides with itself
        """
        self.parent = parent
        self.parent.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.highscore = self.parent.get_highscore('game2')
        self.starting_game_speed = 0.7  # Update rate - Lower is faster
        self.game_speed = self.starting_game_speed
        # How fast game speeds up over time - Lower is faster
        self.game_speed_multiplier = 0.99
        self.max_game_speed = 0.05

        self.current_highscore = 0

        self.board_height = 10
        self.board_width = 10

        self.keyinputs = KeyInputs(self.parent, self.on_wasd, wasd=True)

        self.frame_top_left = tb.Frame(self.parent, padding=0, width=0)
        self.frame_top_right = tb.Frame(self.parent, padding=10, width=10)
        self.frame = tb.Frame(self.parent, padding=0, width=0)

        self.back_button = tb.Button(
            self.frame_top_left, text='Quit', command=lambda: self.quit_game()
        )
        self.back_button.grid(row=0, column=0)

        self.play_again_button = tb.Button(
            self.frame_top_left, text='Play again', command=self.play_again
        )

        self.instructions_label = Label(
            self.frame_top_left,
            (0, 2),
            'Movement: WASD',
            {'visible': False, 'padding': 20},
        )

        self.highscore_header_label = Label(
            self.frame_top_right,
            (0, 0),
            'Highscore: ',
            {'visible': False, 'padding': '0 20'},
        )
        self.highscore_label = Label(
            self.frame_top_right, (0, 1), self.highscore, {'visible': False}
        )

        self.current_score_header_label = Label(
            self.frame_top_right,
            (1, 0),
            'Score: ',
            {'visible': False, 'padding': '0 20'},
        )
        self.current_score_label = Label(
            self.frame_top_right, (1, 1), self.current_highscore, {'visible': False}
        )
        self.current_movement_dir = 'RIGHT'
        self.previous_movement_dir = 'RIGHT'
        self.passed_time = 0.0
        self.t = None  # type: ignore
        self.food_position = (0, 8)
        self.worm_moved_since_previous_update = False

        self.board = self.init_board()

        self.worm = self.Worm(self, self.frame)

    def init_board(self) -> list:
        board = []
        for row in range(self.board_width):
            for column in range(self.board_height):
                column_label = Label(
                    self.frame,
                    row_and_column=(row, column),
                    text='_',
                    customizations={'padding': '1 -4'},
                )
                board.append(column_label)
        return board

    def on_closing(self) -> None:
        if self.t:
            self.t.cancel()
        if messagebox.askokcancel('Quit', 'Do you want to quit?'):
            self.parent.destroy()
        else:
            if self.t:
                self.update_frame()

    def reset_board(self) -> None:
        for label in self.board:
            label.change_label('_')

    def on_wasd(self, key):
        debug(f"Pressed key: '{key}'")

        if key == 'w':
            self.set_movement_direction('UP')
        elif key == 'a':
            self.set_movement_direction('LEFT')
        elif key == 's':
            self.set_movement_direction('DOWN')
        elif key == 'd':
            self.set_movement_direction('RIGHT')

    def spawn_food(self, test=False) -> None:
        if test:
            debug('Test spawn enabled, spawning to 5,0')
            for child in self.board:
                row, col = child.get_row_and_column()

                if row == 5 and col == 0:
                    child.change_label('*')
                    self.food_position = [5, 0]
                    break
            return

        free_spots = []
        occupied_spots = []

        # Occupied spots are the worms locations
        for worm in self.worm.get_worm():
            occupied_spots.append(worm.get_position())

        for child in self.board:
            row, col = child.get_row_and_column()
            if [row, col] not in occupied_spots:
                free_spots.append((row, col))

        choose_spot = choice(free_spots)

        for child in self.board:
            row, col = child.get_row_and_column()

            if row == choose_spot[0] and col == choose_spot[1]:
                debug(f'Spawning food: {choose_spot[0], choose_spot[1]}')
                child.change_label('*')
                self.food_position = [choose_spot[0], choose_spot[1]]
                break

        debug(f'FOOD POS:{self.food_position}')

    def set_movement_direction(self, direction: str) -> None:
        # Problems arise when keyinputs are ahead of the movement.
        is_valid_movement = self.check_valid_movement(direction)
        if not is_valid_movement or not self.worm_moved_since_previous_update:
            debug(f'Invalid movement:{self.current_movement_dir} -> {direction}')
        if (
            self.current_movement_dir != direction
            and is_valid_movement
            and self.worm_moved_since_previous_update
        ):
            self.previous_movement_dir = self.current_movement_dir
            self.current_movement_dir = direction
            self.worm_moved_since_previous_update = False

    def check_valid_movement(self, direction: str) -> bool:
        if direction == 'LEFT' and self.current_movement_dir == 'RIGHT':
            return False
        elif direction == 'RIGHT' and self.current_movement_dir == 'LEFT':
            return False
        elif direction == 'UP' and self.current_movement_dir == 'DOWN':
            return False
        elif direction == 'DOWN' and self.current_movement_dir == 'UP':
            return False
        else:
            return True

    # Exponential since update_frame also increases
    # Need to have another timer for linear increase or math out from current game_speed
    def increase_game_speed(self) -> None:
        if self.game_speed > self.max_game_speed:
            self.game_speed *= self.game_speed_multiplier

    def update_frame(self) -> None:
        self.t = threading.Timer(self.game_speed, self.update_frame)  # type: ignore
        self.t.start()  # type: ignore
        self.passed_time += self.game_speed
        info(f'Frame updated, passed time: {self.passed_time}s')
        self.worm.update_position(self.current_movement_dir, self.previous_movement_dir)
        self.game_over()
        self.increase_game_speed()

    def quit_game(self) -> None:
        self.t.cancel()  # type: ignore
        self.reset_board()
        self.worm.reset_worm()
        self.current_highscore_score = 0
        self.parent.change_window('main')

    def hide(self) -> None:
        self.frame.grid_remove()
        self.frame_top_left.grid_remove()
        self.frame_top_right.grid_remove()
        self.instructions_label.hidden()
        self.play_again_button.grid_remove()
        self.current_score_header_label.hidden()
        self.reset_current_highscore()
        self.current_score_label.hidden()
        self.highscore_header_label.hidden()
        self.highscore_label.hidden()

    def show(self) -> None:
        self.frame_top_left.grid(column=0, row=0, sticky=NW)
        self.frame_top_right.grid(column=1, row=0, sticky=NE)
        self.frame.grid(column=0, row=1, sticky=N)
        self.instructions_label.visible()
        self.current_score_header_label.visible()
        self.current_score_label.visible()
        self.highscore_header_label.visible()
        self.highscore_label.visible()
        self.update_frame()
        self.spawn_food(test=False)

    def play_again(self) -> None:
        info('Play again button pressed')
        self.play_again_button.grid_remove()
        self.reset_board()
        self.worm.reset_worm()
        self.reset_current_highscore()
        self.game_speed = self.starting_game_speed
        self.update_frame()
        self.spawn_food(test=False)

    def set_current_highscore(self) -> None:
        if self.current_highscore > self.highscore:
            self.highscore = self.current_highscore
            self.parent.set_highscore('game2', self.highscore)

    def reset_current_highscore(self) -> None:
        self.current_highscore = 0
        self.current_score_label.change_label(self.current_highscore)

    def update_current_highscore(self) -> None:
        self.current_highscore += 1
        self.current_score_label.change_label(self.current_highscore)

    def game_over(self) -> None:
        worms = self.worm.get_worm()
        first_worm = worms[0]
        first_worm_pos = first_worm.get_position()
        for worm in worms[1:]:
            if worm.get_position() == first_worm_pos:
                info('Game Over')
                self.play_again_button.grid(row=1, column=0, pady=5)
                self.t.cancel()

                if self.current_highscore > self.highscore:
                    self.set_current_highscore()
                    self.highscore = self.current_highscore
                    self.highscore_label.change_label(self.highscore)

    def food_eaten(self) -> None:
        self.update_current_highscore()
        for child in self.board:
            if child.get_text() == '*':
                debug('removing food ')
                child.change_label('_')
                break
        self.spawn_food()

    class Worm(tb.Frame):
        def __init__(self, root, parent, char='O') -> None:
            self.root = root
            self.char = char
            self.position = [0, 1]
            self.parent = parent
            self.worm = []
            self.init_worm()

        def get_worm(self) -> list:
            return self.worm

        def reset_worm(self) -> None:
            for worm in self.worm:
                worm.remove()
                del worm
            self.init_worm()

        def init_worm(self) -> None:
            self.worm.clear()
            self.position = [0, 1]
            self.worm.append(
                self.WormChild(
                    self.parent,
                    [0, 1],
                    char=self.char,
                    current_movement_dir=self.root.current_movement_dir,
                )
            )

        def eat_food(self) -> None:
            food_pos = self.root.food_position
            first_worm = self.worm[0]
            first_worm_pos = first_worm.get_position()
            if food_pos == first_worm_pos:
                debug('EAT FOOD')
                self.grow_worm()
                self.root.food_eaten()

        def grow_worm(self) -> None:
            last_worm = self.worm[-1]
            current_dir = last_worm.get_movement_direction()

            row_diff = 0
            col_diff = 0
            if current_dir == 'RIGHT':
                col_diff -= 1
            elif current_dir == 'LEFT':
                col_diff += 1
            elif current_dir == 'UP':
                row_diff += 1
            elif current_dir == 'DOWN':
                row_diff -= 1

            last_worm_pos = last_worm.get_position()
            row = row_diff + last_worm_pos[0]
            col = col_diff + last_worm_pos[1]
            new_worm = self.WormChild(self.parent, [row, col], 'O', current_dir)
            self.worm.append(new_worm)

        def update_position(self, direction: str, previous_direction: str) -> None:
            debug(f'Moved: {direction}, prev: {previous_direction}')

            first_worm = True
            prev_pos = [0, 1]
            for worm in self.worm:
                curr_pos = worm.get_position().copy()
                debug(f'CURR_POS: {curr_pos}')

                if first_worm:
                    prev_pos = worm.get_position()
                    if direction == 'LEFT':
                        if curr_pos[1] > 0:
                            curr_pos[1] -= 1
                        else:
                            curr_pos[1] = self.root.board_width - 1
                    if direction == 'RIGHT':
                        if curr_pos[1] < self.root.board_width - 1:
                            curr_pos[1] += 1
                        else:
                            curr_pos[1] = 0
                    if direction == 'UP':
                        if curr_pos[0] > 0:
                            curr_pos[0] -= 1
                        else:
                            curr_pos[0] = self.root.board_height - 1
                    if direction == 'DOWN':
                        if curr_pos[0] < self.root.board_height - 1:
                            curr_pos[0] += 1
                        else:
                            curr_pos[0] = 0
                else:
                    curr_pos = prev_pos
                    prev_pos = worm.get_position()

                worm.change_position(curr_pos)
                self.root.worm_moved_since_previous_update = True

                first_worm = False

                debug(f'Pos {worm}: {curr_pos}')

            self.eat_food()

        class WormChild:
            def __init__(
                self,
                parent,
                position: list,
                char: str,
                current_movement_dir: str,
            ) -> None:
                self.char = char
                self.position = position
                self.parent = parent
                self.worm_label = tb.Label(self.parent, text=self.char)
                self.worm_label.grid(row=position[0], column=position[1])
                self.movement_direction = current_movement_dir

            def remove(self):
                self.worm_label.grid_remove()

            def change_position(self, position: list) -> None:
                self.set_movement_direction(position)
                self.position = position
                self.worm_label.grid_configure(row=position[0], column=position[1])

            def get_position(self) -> list:
                return self.position

            def get_movement_direction(self) -> str:
                return self.movement_direction

            def set_movement_direction(self, position: list) -> None:
                if position[0] != self.position[0]:
                    if (position[0] - self.position[0]) > 0:
                        self.movement_direction = 'DOWN'
                    else:
                        self.movement_direction = 'UP'
                else:
                    if (position[1] - self.position[1]) > 0:
                        self.movement_direction = 'RIGHT'
                    else:
                        self.movement_direction = 'LEFT'
