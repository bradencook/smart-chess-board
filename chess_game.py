import chess
# import chess.engine
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
            self.initialize_engine(bot_level)

    def initialize_engine(self, bot_level):
        """Initialize the chess engine at the given level."""
        # Placeholder for chess engine initialization (e.g., Stockfish)
        print(f"Bot level {bot_level} initialized (engine setup required).")

    def play(self):
        self.setup()
        # this is the game loop
        print("ready")
        while not self.game.is_game_over():
            self.board.read_signals()
            self.update()
            self.render()
        self.handle_results(self.game.outcome())

    def update(self):
        if self.board.signals != self.board.prev_signals: # handle changes in piece position
            for i in range(len(self.board.signals)):
                current, prev = self.board.signals[i], self.board.prev_signals[i]
                if current != prev:
                    if current == 1: # piece picked up or moved
                        self.handle_piece_pickup(i)
                    else: # piece placed
                        self.handle_piece_placement(i)

    def handle_piece_pickup(self, idx):
        if idx in self.valid_moves: #capture
            return
        elif self.game.piece_at(idx) and self.game.turn == self.game.piece_at(idx).color and not self.cell_to_move: #valid
            self.cell_to_move = idx
            for move in self.game.legal_moves:
                if move.from_square == idx:
                    self.valid_moves.add(move.to_square)
        elif idx in self.misplaced: # replacing an invalid piece
            self.misplaced.remove(idx)
        else: # invalid
            self.misplaced.add(idx)

    def handle_piece_placement(self, idx):
        if idx in self.valid_moves: # make the move
            self.move(idx)
        elif self.cell_to_move == idx: # trying a different piece
            self.cell_to_move = None
            self.valid_moves.clear()
        elif idx in self.misplaced: # replacing an invalid piece
            self.misplaced.remove(idx)
        else: # invalid
            self.misplaced.add(idx)

    def handle_results(self, outcome):
        colors = []
        light = io_board.ORANGE
        dark = io_board.RED
        if outcome.winner == chess.WHITE:
            light = io_board.WHITE
            dark = io_board.YELLOW
        elif outcome.winner == chess.BLACK:
            light = io_board.CYAN
            dark = io_board.BLUE
        for cell in self.board.default_board:
            if cell == self.board.light:
                colors.append(light)
            else:
                colors.append(dark)
        self.board.set_board(colors)
        self.board.render()
        

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
        move = self.game.find_move(self.cell_to_move, to_square)
        turn = self.game.turn

        if self.game.is_castling(move):
            rook_from = None
            rook_to = None
            if self.game.is_kingside_castling(move):
                rook_from = 7 if turn == chess.WHITE else 63
                rook_to = 5 if turn == chess.WHITE else 61

            if self.game.is_queenside_castling(move):
                rook_from = 0 if turn == chess.WHITE else 56
                rook_to = 3 if turn == chess.WHITE else 59

            if rook_from in self.misplaced:
                self.misplaced.remove(rook_from)
            else:
                self.misplaced.add(rook_from)

            if rook_to in self.misplaced:
                self.misplaced.remove(rook_to)
            else:
                self.misplaced.add(rook_to)

        if self.game.is_en_passant(move): # remove pawn
            pawn = to_square - 8 if turn == chess.WHITE else to_square + 8
            if pawn in self.misplaced:
                self.misplaced.remove(pawn)
            else:
                self.misplaced.add(pawn)

        self.game.push(move)
        print(f"Move made: {self.game.peek()}")
        print(self.game)
        print()

        # reset some stuff
        self.cell_to_move = None
        self.valid_moves.clear()

    def setup(self):
        """Setup the board to the starting position."""
        self.board.read_signals()
        colors = [io_board.NONE] * 64
        while self.board.signals != self.start_pos:
            for i in range(16):
                if self.board.signals[i] != self.start_pos[i]:
                    colors[i] = io_board.YELLOW if self.board.default_board[i] == self.board.dark else io_board.WHITE
                else:
                    colors[i] = io_board.NONE
            for i in range(48, 64):
                if self.board.signals[i] != self.start_pos[i]:
                    colors[i] = io_board.BLUE if self.board.default_board[i] == self.board.dark else io_board.CYAN
                else:
                    colors[i] = io_board.NONE
            self.board.set_board(colors)
            self.board.render()
            self.board.read_signals()
        self.fade_in(self.board.default_board)

        
    def fade_in(self, board):
        brightness = 0
        increment = 2
        while brightness < 255:
            self.board.set_brightness(brightness)
            self.board.set_board(board)
            self.board.render()
            increment += 2
            brightness += increment 
        self.board.set_brightness(brightness)
        self.board.set_board(board)
        self.board.render()

    

if __name__ == "__main__":
    mode = ""
    game = None

    print("""cool ascii heading here""")

    print("""Select a game mode:
    (1) Multiplayer
    (2) Play an engine""")

    while mode not in ["1", "2"]:
        mode = input(">>> ").strip()

    if mode == "1":
        game = Chess_Game()
    else:
        level = 0
        print("Enter engine level (100 - 3000)")
        while level < 100 or level > 3000:
            try:
                level = int(input(">>> ").strip())
            except ValueError:
                print("Please enter a valid number between 100 and 3000.")
        game = Chess_Game(level)

    game.play()