from talker import Talker

YELLOW = (200, 200, 0)
ORANGE = (255, 50, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (140, 140, 140)
CYAN = (0, 255, 255)

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
            if i % 2 == 0:
                self.default_board.append(dark)
            else:
                self.default_board.append(light)
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
        # sets given array of cell values to the emph color
        if type(cells) == int:
            cells = [cells]
        for cell in cells:
            self.talker.send(f"set_led({cell}, {self.emph})")

    def restore(self, cells):
        pass

    def set_default(self, cells):
        # sets given array of cell values to their default color
        pass

    def set_board(self, board):
        # takes a whole array of color tuples to fill the board
        pass

    def set_cell(self, cell, color):
        # sets a specific cell a specific color tuple
        pass

    def render(self):
        self.talker.send("show()")

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
