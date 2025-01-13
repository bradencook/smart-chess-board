from talker import Talker

yellow = (255, 100, 0)
orange = (255, 50, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (140, 140, 140)
cyan = (0, 255, 255)

t = Talker()

default_board = []
prev_signals = []

for i in range(64):
    if i % 2 == 0:
        default_board.append(blue)
    else:
        default_board.append(white)
    prev_signals.append(1)

while True:
    # validate input
    t.send('read_signals()')
    signals = eval(t.receive())
    if type(signals) != list:
        print("Invalid signal received:\n", signals)
        continue

    if signals != prev_signals:
        # update game state
        for i in range(len(signals)):
            if signals[i] != prev_signals[i]:
                color = default_board[i]
                if signals[i] == 0:
                    color = green
                t.send(f'set_led_color({i}, {color})')

    prev_signals = signals