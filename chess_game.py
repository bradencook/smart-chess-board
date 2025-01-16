import chess
import chess.engine
import random
import io_board
from io_board import IO_Board

class Chess_Game:
    def __init__(self, bot_level=None, engine_white=False, engine_black=False):
        self.io = IO_Board()
        self.board = chess.Board()
        self.start_pos = [0] * 16 + [1] * 32 + [0] * 16
        self.cell_to_move = None
        self.misplaced = set()
        self.valid_moves = set()
        self.engine_white = engine_white
        self.engine_black = engine_black
        self.engine = None
        self.suggested_move = None

        if bot_level is not None:
            self.initialize_engine(bot_level)

    def initialize_engine(self, bot_level):
        """Initialize the chess engine at the given level."""
        self.engine = chess.engine.SimpleEngine.popen_uci("/Users/bradencook/Documents/smart-chess-board/stockfish/stockfish-macos-m1-apple-silicon")
        self.engine.configure({"Skill Level": bot_level})

    def play(self):
        self.setup()
        # this is the game loop
        print("ready")
        while not self.board.is_game_over():
            self.io.read_signals()
            self.update()
            self.render()
        self.handle_results(self.board.outcome())

    def update(self):
        if not self.suggested_move:
            if (self.board.turn == chess.WHITE and self.engine_white) or (self.board.turn == chess.BLACK and self.engine_black):
                self.suggested_move = self.engine.play(self.board, chess.engine.Limit(time=0.1)).move
        if self.io.signals != self.io.prev_signals: # handle changes in piece position
            for i in range(len(self.io.signals)):
                current, prev = self.io.signals[i], self.io.prev_signals[i]
                if current != prev:
                    if current == 1: # piece picked up or moved
                        self.handle_piece_pickup(i)
                    else: # piece placed
                        self.handle_piece_placement(i)

    def handle_piece_pickup(self, idx):
        if idx in self.valid_moves: #capture
            return
        elif self.board.piece_at(idx) and self.board.turn == self.board.piece_at(idx).color and not self.cell_to_move: #valid
            self.cell_to_move = idx
            for move in self.board.legal_moves:
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
        for cell in self.io.default_board:
            if cell == self.io.light:
                colors.append(light)
            else:
                colors.append(dark)
        self.io.set_board(colors)
        self.io.render()
        

    def render(self):
        # send updates to board
        self.io.set_board(self.io.default_board)
        if self.cell_to_move:
            self.io.highlight(self.cell_to_move)
        for cell in self.valid_moves:
            self.io.highlight(cell)
        if self.board.is_check():
            self.io.set_cell(self.board.king(self.board.turn), io_board.PINK)
        if self.suggested_move:
            self.io.set_cell(self.suggested_move.from_square, io_board.ORANGE)
            self.io.set_cell(self.suggested_move.to_square, io_board.ORANGE)
        for cell in self.misplaced:
            self.io.set_cell(cell, io_board.RED)
        self.io.render()

    def move(self, to_square):
        move = self.board.find_move(self.cell_to_move, to_square)
        turn = self.board.turn

        # if self.board.is_castling(move):
        #     rook_from = None
        #     rook_to = None
        #     if self.board.is_kingside_castling(move):
        #         rook_from = 7 if turn == chess.WHITE else 63
        #         rook_to = 5 if turn == chess.WHITE else 61

        #     if self.board.is_queenside_castling(move):
        #         rook_from = 0 if turn == chess.WHITE else 56
        #         rook_to = 3 if turn == chess.WHITE else 59

        #     if rook_from in self.misplaced:
        #         self.misplaced.remove(rook_from)
        #     else:
        #         self.misplaced.add(rook_from)

        #     if rook_to in self.misplaced:
        #         self.misplaced.remove(rook_to)
        #     else:
        #         self.misplaced.add(rook_to)

        # if self.board.is_en_passant(move): # remove pawn
        #     pawn = to_square - 8 if turn == chess.WHITE else to_square + 8
        #     if pawn in self.misplaced:
        #         self.misplaced.remove(pawn)
        #     else:
        #         self.misplaced.add(pawn)


        self.board.push(move)
        print(f"Move made: {self.board.peek()}")
        print(self.board)
        print()

        # reset error handling
        self.misplaced.clear()
        io_pieces = set()
        for i in range(len(self.io.signals)):
            if self.io.signals[i] == 0 and self.board.piece_at(i) is None: 
                self.misplaced.add(i)
            elif self.io.signals[i] == 1 and self.board.piece_at(i):
                self.misplaced.add(i)
        

        # reset some other stuff
        self.suggested_move = None
        self.cell_to_move = None
        self.valid_moves.clear()

    def setup(self):
        """Setup the board to the starting position."""
        self.io.read_signals()
        colors = [io_board.NONE] * 64
        while self.io.signals != self.start_pos:
            for i in range(16):
                if self.io.signals[i] != self.start_pos[i]:
                    colors[i] = io_board.YELLOW if self.io.default_board[i] == self.io.dark else io_board.WHITE
                else:
                    colors[i] = io_board.NONE
            for i in range(48, 64):
                if self.io.signals[i] != self.start_pos[i]:
                    colors[i] = io_board.BLUE if self.io.default_board[i] == self.io.dark else io_board.CYAN
                else:
                    colors[i] = io_board.NONE
            self.io.set_board(colors)
            self.io.render()
            self.io.read_signals()
        self.fade_in(self.io.default_board)

        
    def fade_in(self, board):
        brightness = 0
        increment = 2
        while brightness < 255:
            self.io.set_brightness(brightness)
            self.io.set_board(board)
            self.io.render()
            increment += 2
            brightness += increment 
        self.io.set_brightness(brightness)
        self.io.set_board(board)
        self.io.render()

    

if __name__ == "__main__":
    import random

    mode = ""
    game = None

    print('''
     ,gggg,                                          
   ,88"""Y8b, ,dPYb,                                 
  d8"     `Y8 IP'`Yb                                 
 d8'   8b  d8 I8  8I                                 
,8I    "Y88P' I8  8'                                 
I8'           I8 dPgg,    ,ggg,     ,g,       ,g,    
d8            I8dP" "8I  i8" "8i   ,8'8,     ,8'8,   
Y8,           I8P    I8  I8, ,8I  ,8'  Yb   ,8'  Yb  
`Yba,,_____, ,d8     I8, `YbadP' ,8'_   8) ,8'_   8) 
  `"Y8888888 88P     `Y8888P"Y888P' "YY8P8PP' "YY8P8P

''')

    print("""Select a game mode:
    (1) Multiplayer
    (2) Chess Engine""")

    while mode not in ["1", "2"]:
        mode = input(">>> ").strip()

    if mode == "1":
        game = Chess_Game()
    else:
        level = -1
        print("Enter engine level (0 - 20):")
        while level < 0 or level > 20:
            try:
                level = int(input(">>> ").strip())
            except ValueError:
                print("Please enter a valid number between 0 and 20.")

        engine_side = ""
        print("Choose engine's side:")
        print("(1) White")
        print("(2) Black")
        print("(3) Random")
        print("(4) Both")

        while engine_side not in ["1", "2", "3", "4"]:
            engine_side = input(">>> ").strip()

        if engine_side == "3":
            engine_side = random.choice(["1", "2"])
            if engine_side == "1":
                print("Engine will play as White")
            else:
                print("Engine will play as Black")

        # Translate input into side options
        if engine_side == "1":
            engine_plays_white = True
            engine_plays_black = False
        elif engine_side == "2":
            engine_plays_white = False
            engine_plays_black = True
        elif engine_side == "4":
            engine_plays_white = True
            engine_plays_black = True

        # Pass the engine level and side information to the game
        game = Chess_Game(level, engine_plays_white, engine_plays_black)

    game.play()
