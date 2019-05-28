import time
from status_board import StatusBoard

# Modify the variable value below
# for delaying the time between action.
sleep_time = 0.5

# Instantiate the StatusBoard object.
board = StatusBoard()

# Apply each color to all LEDs on the board.
for color in board.colors.keys():
    print("Setting color {} to all LED".format(color))
    board.color_all(color)
    time.sleep(sleep_time)

# Apply different colors to each LED on the board.
board.set_pixel_color(0, 'blue')
board.set_pixel_color(1, 'red')
board.set_pixel_color(2, 'green')
board.set_pixel_color(3, 'yellow')

# let's turn off all LEDs on the board
board.clear_all()
