from talker import Talker
from time import sleep

YELLOW = (200, 200, 80)
ORANGE = (255, 50, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (140, 140, 140)
CYAN = (0, 255, 255)
NONE = (0, 0, 0)
PINK = (255, 100, 100)

# cells are numbered from bottom to top with a1 and a2 being 0 and 1 and g7 and g8 being 62 and 63

class IO_Board:
    def __init__(self, light=WHITE, dark=BLUE, emph=GREEN):
        self.talker = Talker()
        self.default_board = []
        self.signals = []
        self.prev_signals = []
        self.light = light
        self.dark = dark
        self.emph = emph

        for i in range(64):
            if (i // 8) % 2 == 0: # even rows
                if i % 2 == 0:
                    self.default_board.append(dark)
                else:
                    self.default_board.append(light)
            else: # odd rows
                if i % 2 == 0:
                    self.default_board.append(light)
                else:
                    self.default_board.append(dark)

            self.signals.append(1)

    def read_signals(self):
        # validate input
        self.prev_signals = self.signals
        self.talker.send('read_signals()')
        signals = eval(self.talker.receive())
        if type(signals) != list:
            print("Invalid signal received:\n", signals)
            return
        self.signals = signals

    def highlight(self, cells):
        # sets given value or array of cell values to the emph color
        if type(cells) == int:
            cells = [cells]
        for cell in cells:
            self.talker.send(f"set_led({cell}, {self.emph})")

    def set_default(self, cells):
        # sets given value or array of cell values to their default color
        if type(cells) == int:
            cells = [cells]
        for cell in cells:
            self.talker.send(f"set_led({cell}, {self.default_board[i]})")

    def set_board(self, board):
        # takes a whole array of color tuples to fill the board
        self.talker.send(f"set_board({board})")

    def set_cell(self, cell, color):
        # sets a specific cell a specific color tuple
        self.talker.send(f"set_led({cell}, {color})")

    def render(self):
        # show led updates
        self.talker.send("show()")
        sleep(0.05) # give the board time to process the request

    def set_brightness(self, brightness):
        # set the brighness 0 - 255
        self.talker.send(f"set_brightness({brightness})")

if __name__ == "__main__":
    board = IO_Board()
    while True:
        board.read_signals()

        if board.signals != board.prev_signals:
            # update board cells
            for i in range(len(board.signals)):
                if board.signals[i] != board.prev_signals[i]: # check for change
                    if board.signals[i] == 0: # piece present
                        board.highlight(i)
                    else:
                        board.restore(i)
        board.render()
