# Game Arcade created with Tkinter

Learning classes and tkinter GUI. The game arcade contains two games; Card game and a classic Worm game.

## Branches

### v0.1

Game that has 4 cards (buttons) and the goal is to get the target score 0. Each card gets one of the following operation -,+,*,/ and a value between (-50)-(-1) or 1-50. When card is used, the card gets new value and operation. Some balances are being places such as division that leads straigth to 0 is being discarded but nothing too special. You can just win the game by spamming one card.

#### Todo for v0.2
- Highscore and storing the highscore
- Balances to * and / operations.

---

### v0.2

- Added highscore and storing the highscore.
- Made some balances to * and / operations (is now between 1-25)
- General fixes and stylings

#### Todo for v0.3
- Styled cards depending on what the opeartion is
- Main window for other games ("Game Arcade") where you can choose a game
- New game (Worm game) with movement using buttons and keybindings

---

### v0.3

- Added main window where you can choose a game to play
- Added worm game
    - does not have ending yet
    - does not have scoring or moving with keys

#### Todo for v0.4

- Game end mechanic (Moves to wall or through itself)
- highscore and storing this highscore
- ~~maybe sounds~~ later versions
- ~~styling could be better~~ later versions
- Rework worm grow to be dynamic (maybe class implementation)
- fix small bugs found in the game.py TODO sections

---

### v0.4

- Changed default formatter to ruff

#### Game1

- Now resets the game when quitting

#### Game 2

- Added game ending mechanic to  (by colliding itself)
- Added moving through end borders
- Added invalid movement check ex. right->left, up->down

#### TODO for v0.5:

- ~~Plan for general stylings~~ - First functionalities then stylings

##### Game 2

- Movement using WASD or arrow keys
- 'Try again' button and End game events
- Speed increases over time or when eating 
- Visual clarity when growing the worm

---

### v0.5

- Added KeyInputs class to read keyinputs from tkinter

#### Game 2

**Added**:
- WASD movement
- Scoring system (integrated the same system used in Game 1)
- Game now resets after hitting 'Quit'
- Visual Clarity is now good enough since the game is faster
- Game speed now increases exponentially over time
- Play again button

**Fixed**:
- Food spawning inside the worm

#### TODO for v0.6:

**Game 2 - Nice to have**
- Game options:
    - Linear gamespeed, speed rate grow, starting speed
    - Borders
    - Multiple foods spawns
    - Foods that reduce speed or size

**Game 3 - Ideas & plannings**:

Games:

- Sidescroller
    - One button game, or can add/decrease speed with left+right
- Mario
    - this generally needs graphics in order to look good
- Mouse location based game
    - Keep the mouse away from the monsters
- pacman
    - similar enough to worm game with added mechanics
- asteroid
    - Might need better handling of the frameupdates

Applications:

- paint (interesting to code atleast)
- weather app (has requests, handling data)

---

### v0.6

- Cleaned up v0.5 prints and comments
- Separated Games and Tkinter custom classes to their own files
- Discovered: can't get mouse location based games work using binding `<Enter>`, instead need to use buttons.

**Added**
- Game3/App template
- On closing event - Confirmation on quit
    - (Worm game throwed errors because the threading was not stopped before exiting)


