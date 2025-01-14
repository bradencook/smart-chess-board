import chess
from talker import Talker

class Chess_Game:
    def __init__(self, bot_level=None):
        self.talker = Talker()
        if bot_level:
            # initialize engine
            pass

    def play(self):
        # setup
        pass
        # this is the game loop
        
    def check_board_ready(self):
        pass
    

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