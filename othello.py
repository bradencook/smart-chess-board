import io_board

DIRECTIONS = ['n', 'e', 's', 'w', 'ne', 'se', 'sw', 'nw']

class Othello:
    def __init__(self):
        self.io = io_board.IO_Board()
        self.board = []
        self.skip = False
        self.zero_turn = True
        self.valid = set()

        for i in range(64):
            self.board.append(self.Piece(None, i))
        
    def setup(self):
        self.board[27].side = 1
        self.board[28].side = 0
        self.board[35].side = 0
        self.board[36].side = 1

    def play(self):
        self.setup()
        while True:
            print(self)
            self.set_valid()
            print('valid moves: ', self.valid)
            self.render()
            move = None
            if self.valid:
                while move not in self.valid:
                    move = self.get_move()
            if move is not None:
                self.skip = False
                self.make_move(move)
            elif self.skip:
                break
            else:   
                self.skip = True
            self.zero_turn = not self.zero_turn
        print(self.get_winner())

    def get_winner(self):
        blue_cnt = 0
        green_cnt = 0
        for square in self.board:
            if square.side == 0:
                blue_cnt += 1
            if square.side == 0:
                green_cnt += 1
        if blue_cnt > green_cnt:
            return f"Blue wins! {blue_cnt}-{green_cnt}"
        elif blue_cnt > green_cnt:
            return f"Blue wins! {green_cnt}-{blue_cnt}"
        else:
            return f"It's a tie! {blue_cnt}-{green_cnt}"

    def get_move(self):
        self.io.read_signals()
        while self.io.signals == self.io.prev_signals:
            self.io.read_signals()
        for i in range(len(self.io.signals)):
            if self.io.signals[i] == 0:
                return i

    def render(self):
        board = []
        for i in range(len(self.board)):
            if self.board[i].side is not None:
                color = io_board.BLUE if self.board[i].side == 0 else io_board.GREEN
                board.append(color)
            else:
                board.append(io_board.NONE)
        self.io.set_board(board)
        for move in self.valid:
            color = (100, 100, 255) if self.zero_turn else (100, 255, 100)
            self.io.set_cell(move, color)
        self.io.render()

    def fade(self, flips):
        if self.zero_turn: # green to blue
            for i in range(0, 256, 5):
                for flip in flips:
                    self.io.set_cell(flip, (0, 255 - i, 0 + i))
                self.io.render()
        else: # blue to green
            for i in range(0, 256, 5):
                for flip in flips:
                    self.io.set_cell(flip, (0, 0 + i, 255 - i))
                self.io.render()

    def set_valid(self):
        for piece in self.board:
            if piece.side is None:
                for dir in DIRECTIONS:
                    flips = self.get_flips(piece, dir)
                    if flips:
                        self.valid.add(piece.loc)
                        break

    def get_flips(self, piece, dir):
        current = piece.neighbors[dir]
        if current is None:
            return
        current = self.board[piece.neighbors[dir]]
        if self.zero_turn and current.side == 1 or not self.zero_turn and current.side == 0:
            # traverse not turn until you hit turn
            next = self.get_flips_helper(current, dir)
            if next is not None:
                return [current.loc] + next

    def get_flips_helper(self, piece, dir):
        current = piece.neighbors[dir]
        if current is None:
            return
        current = self.board[piece.neighbors[dir]]
        if current.side is None:
            return
        if self.zero_turn and current.side == 0 or not self.zero_turn and current.side == 1:
            return []
        else:
            next = self.get_flips_helper(current, dir)
            if next is not None:
                return [current.loc] + next


    def make_move(self, move):
        flips = []
        for dir in DIRECTIONS:
            dir_flips = self.get_flips(self.board[move], dir)
            if dir_flips:
                flips += dir_flips
        print('flips: ', flips)
        self.board[move].side = 0 if self.zero_turn else 1
        self.valid = set()
        self.render()
        self.fade(flips)
        for loc in flips:
            self.board[loc].side = 0 if self.zero_turn else 1

        
    def __str__(self):
        out_str = ''
        for i in range(8):
            for piece in self.board[(7-i)*8:(7-i)*8+8]:
                if piece.side is None:
                    out_str += ' . '
                else:
                    out_str += ' ' + str(piece.side) + ' '
            out_str += '\n'
        return out_str
    
    class Piece:
        def __init__(self, side, loc):
            self.side = side
            self.loc = loc
            self.n = self.loc + 8 if self.loc // 8 < 7 else None
            self.e = self.loc + 1 if self.loc % 8 < 7 else None
            self.s = self.loc - 8 if self.loc // 8 > 0 else None
            self.w = self.loc - 1 if self.loc % 8 > 0 else None
            self.ne = self.loc + 9 if self.n is not None and self.e is not None else None
            self.se = self.loc - 7 if self.s is not None and self.e is not None else None
            self.sw = self.loc - 9 if self.s is not None and self.w is not None else None
            self.nw = self.loc + 7 if self.n is not None and self.w is not None else None
            self.neighbors = {
                'n': self.n, 
                'e': self.e,
                's': self.s, 
                'w': self.w, 
                'ne': self.ne,
                'se': self.se,
                'sw': self.sw,
                'nw': self.nw
            }
            

if __name__ == "__main__":
    game = Othello()
    game.play()