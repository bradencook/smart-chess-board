import chess
import io_board
from io_board import IO_Board

class Chess_Game:
    def __init__(self, bot_level=None):
        self.board = IO_Board()
        self.game = chess.Board()
        self.start_pos = [0] * 16 + [1] * 32 + [0] * 16
        self.cell_to_move = None
        self.misplaced = set()
        self.valid_moves = set()

        if bot_level:
            # initialize engine
            pass

    def play(self):
        self.setup()
        # this is the game loop
        print("ready")
        while not self.game.is_game_over():
            # read input
            self.board.read_signals()
            # update game state
            self.update()
            # render
            self.render()
        print(self.game.outcome())

    def update(self):
        if self.board.signals != self.board.prev_signals: # handle changes in piece position
            for i in range(len(self.board.signals)):
                current, prev = self.board.signals[i], self.board.prev_signals[i]
                if current != prev:
                    if current == 1: # piece picked up or moved
                        if i in self.valid_moves: #capture
                            continue
                        elif self.game.piece_at(i) and self.game.turn == self.game.piece_at(i).color and not self.cell_to_move: #valid
                            self.cell_to_move = i
                            for move in self.game.legal_moves:
                                if move.from_square == i:
                                    self.valid_moves.add(move.to_square)
                        elif i in self.misplaced: # replacing an invalid piece
                            self.misplaced.remove(i)
                        else: # invalid
                            self.misplaced.add(i)
                    else: # piece placed
                        if i in self.valid_moves: # make the move
                            self.move(i)
                        elif self.cell_to_move == i: # trying a different piece
                            self.cell_to_move = None
                            self.valid_moves.clear()
                        elif i in self.misplaced: # replacing an invalid piece
                            self.misplaced.remove(i)
                        else: # invalid
                            self.misplaced.add(i)

    def render(self):
        # send updates to board
        self.board.set_board(self.board.default_board)
        if self.cell_to_move:
            self.board.highlight(self.cell_to_move)
        for cell in self.valid_moves:
            self.board.highlight(cell)
        for cell in self.misplaced:
            self.board.set_cell(cell, io_board.RED)
        self.board.render()

    def move(self, to_square):
        self.game.push(chess.Move(self.cell_to_move, to_square))
        print(self.game)
        self.cell_to_move = None
        self.valid_moves.clear()

    def setup(self):
        # setup
        self.board.read_signals()
        colors = [io_board.NONE] * 64
        while self.board.signals != self.start_pos:
            for i in range(16):
                if self.board.signals[i] != self.start_pos[i]:
                    if self.board.default_board[i] == self.board.dark:
                        colors[i] = io_board.YELLOW
                    else:
                        colors[i] = io_board.WHITE
                else:
                    colors[i] = io_board.NONE
            for i in range(48, 64):
                if self.board.signals[i] != self.start_pos[i]:
                    if self.board.default_board[i] == self.board.dark:
                        colors[i] = io_board.BLUE
                    else:
                        colors[i] = io_board.CYAN
                else:
                    colors[i] = io_board.NONE
            self.board.set_board(colors)
            self.board.render()
            self.board.read_signals()

        brightness = 0
        while brightness < 255:
            self.board.set_brightness(brightness)
            self.board.set_board(self.board.default_board)
            self.board.render()
            brightness += 5      
        
    

if __name__ == "__main__":
    mode = 0
    game = None

    print("""cool ascii heading here""")

    print("""Select a game mode:
    (1) Multiplayer
    (2) Play an engine""")

    while mode != "1" and mode != "2":
        mode = input(">>> ")
    
    if mode == "1":
        game = Chess_Game()
    else:
        level = 0
        print("Enter engine level (100 - 3000)")
        while level < 100 or level > 3000:
            level = int(input(">>> "))
        game = Chess_Game(level)
           
    game.play()