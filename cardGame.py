import math
from logging import debug, info
import ttkbootstrap as tb  # type: ignore
from helperClasses import Label, Card, CardButton
from ttkbootstrap.constants import NW, NE, N  # type: ignore


class Game(tb.Frame):
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
        self.highscore = self.parent.get_highscore('game1')
        self.max_highscore = max_highscore
        self.current_highscore = self.max_highscore

        self.frame_top_left = tb.Frame(self.parent, padding=0, width=0)
        self.frame_top_right = tb.Frame(self.parent, padding=0, width=0)
        self.frame = tb.Frame(self.parent, padding=0, width=2)
        self.frame_cards = tb.Frame(self.parent, padding=0, width=2)

        self.back_button = tb.Button(
            self.frame_top_left, text='Quit', command=lambda: self.quit_game()
        )
        self.back_button.grid(row=0, column=0)

        self.current_highscore_label = Label(
            self.frame_top_left,
            (0, 1),
            f'Current score: {self.current_highscore}',
            {'font': ('Arial', 14)},
        )
        self.highscore_label = Label(
            self.frame_top_right,
            (0, 0),
            f'Highscore: {self.highscore}',
            {'font': ('Arial', 14)},
        )

        self.win_label = Label(self.frame, (0, 0), '')
        self.goal_label = Label(self.frame, (1, 1), f'Goal: {self.target_score}')
        self.try_again_button = tb.Button(
            self.frame, text='Play again', command=self.play_again
        )
        self.current_score_label = Label(
            self.frame, (2, 1), f'Current: {self.current_score}'
        )
        self.card1 = self.init_card(self.frame_cards, 3, 0, 'addition', 0)
        self.card2 = self.init_card(self.frame_cards, 3, 1, 'subtraction', 1)
        self.card3 = self.init_card(self.frame_cards, 3, 2, 'multiplication', 2)
        self.card4 = self.init_card(self.frame_cards, 3, 3, 'division', 3)

    def get_card_style(self, card_type: str) -> str:
        if card_type == 'multiplication' or card_type == 'division':
            return 'custom.Success.TButton'
        elif card_type == 'round_up' or card_type == 'round_down':
            return 'custom.Info.TButton'
        else:
            return 'custom.Primary.TButton'

    def init_card(
        self,
        frame,
        row=0,
        column=0,
        card_type='addition',
        card_index=0,
    ) -> CardButton:
        return CardButton(
            frame,
            (row, column),
            Card(card_type, card_index),
            customizations={
                'on_click': self.on_click_card,
                'style': self.get_card_style(card_type),
            },
        )

    def game_over(self) -> bool:
        return self.target_score == self.current_score

    def quit_game(self) -> None:
        self.reset_game()
        self.parent.change_window('main')

    def reset_game(self) -> None:
        info('Reset game')
        self.current_highscore = self.max_highscore
        self.current_score = self.starting_score
        self.reinit_card(self.card1, 'addition')
        self.reinit_card(self.card2, 'subtraction')
        self.reinit_card(self.card3, 'multiplication')
        self.reinit_card(self.card4, 'division')

        self.try_again_button.grid_remove()
        self.win_label.change_label('')
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
        info('Play again button pressed')
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

    def set_current_highscore(self) -> None:
        if self.current_highscore > self.highscore:
            self.highscore = self.current_highscore
            self.parent.set_highscore('game1', self.highscore)

    def reset_current_highscore(self) -> None:
        self.current_highscore = self.max_highscore

    def disable_cards(self) -> None:
        info('All cards disabled')
        self.card1.disable()
        self.card2.disable()
        self.card3.disable()
        self.card4.disable()

    def enable_cards(self) -> None:
        info('All cards enabled')
        self.card1.enable()
        self.card2.enable()
        self.card3.enable()
        self.card4.enable()

    def set_current_score(self, value: int) -> None:
        """
        Max/Min score is starting_score & -starting_score
        """
        starting_score = self.starting_score

        if value > starting_score:
            self.current_score = starting_score
        elif value < starting_score * -1:
            self.current_score = starting_score * -1
        else:
            self.current_score = value

    def reinit_card(self, card, operation=None) -> None:
        info('Reiniting card')
        card_class = card.get_card()
        debug(f'Reiniting card: {card_class}')
        card_class.reinit_card(operation)
        card.update_text(self.get_card_style(card_class.card_type))

    def update_current_highscore(self) -> None:
        if self.current_highscore > 0:
            self.current_highscore -= 1

    def on_click_card(self, card) -> None:
        info('Clicked card')
        debug(f'Clicked: {card.get_card_text()}')
        current_score = self.current_score
        card_obj = card.get_card()
        card_value = card_obj['value']
        card_index = card_obj['index']

        # Do calculation based on the card's operation
        if card.operator == '+':
            debug(
                f'Addition -> round(current_score+card_value, 1) = {
                    round(current_score+card_value, 1)}'
            )
            self.set_current_score(round(current_score + card_value, 1))
        elif card.operator == '-':
            debug(
                f'Subtraction -> round(current_score+card_value, 1) = {
                    round(current_score-card_value, 1)}'
            )
            self.set_current_score(round(current_score - card_value, 1))
        elif card.operator == '*':
            debug(
                f'Multiplication -> round(current_score*card_value, 1) = {
                    round(current_score*card_value, 1)}'
            )
            self.set_current_score(round(current_score * card_value, 1))
        elif card.operator == '/':
            debug(
                f'Division -> round(current_score/card_value, 1) = {
                    round(current_score/card_value, 1)}'
            )
            self.set_current_score(round(current_score / card_value, 1))
        elif card.operator == 'round_up':
            debug(f'Round up -> math.ceil(current_score) = {math.ceil(current_score)}')
            self.set_current_score(math.ceil(current_score))
        elif card.operator == 'round_down':
            debug(
                f'Round down -> math.floor(current_score) = {
                    math.floor(current_score)}'
            )
            self.set_current_score(math.floor(current_score))

        # Reset the card that was pressed
        if card_index == 0:
            self.reinit_card(self.card1)
            debug(f'Card 1 is now: {self.card1.get_card().get_card_text()}')
        elif card_index == 1:
            self.reinit_card(self.card2)
            debug(f'Card 2 is now: {self.card2.get_card().get_card_text()}')
        elif card_index == 2:
            self.reinit_card(self.card3)
            debug(f'Card 3 is now: {self.card3.get_card().get_card_text()}')
        elif card_index == 3:
            self.reinit_card(self.card4)
            debug(f'Card 4 is now: {self.card4.get_card().get_card_text()}')

        self.update_current_highscore()
        self.current_score_label.change_label(text=self.current_score)
        self.current_highscore_label.change_label(
            text=f'Score: {self.current_highscore}'
        )
        debug(f'Current score is now: {self.current_score}')

        if self.game_over():
            info('Game ended')
            self.win_label.change_label('You win!')
            self.disable_cards()
            self.try_again_button.grid(row=0, column=4)
            if self.current_highscore > self.highscore:
                self.parent.set_highscore('game1', self.current_highscore)
                self.highscore_label.change_label(
                    f'Highscore: {self.current_highscore}'
                )
