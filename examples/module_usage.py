"""
Example script using all available method on the `status_board.StatusBoard`
for setting pixel colors and also it brightness.
"""
import time
from status_board import StatusBoard

# Modify the variable value below
# for delaying the time between action.
sleep_time = 0.5


def demo(board):
    """
    Function to use all methods on the `status_board.StatusBoard`

    Returns:
        None.
    """
    # Apply each color to all LEDs on the board.
    for color in board.colors.keys():
        print("Setting color '{}' to all LED".format(color))
        board.color_all(color)
        time.sleep(sleep_time)

    # Apply different colors to each LED on the board.
    print('Setting each pixel a different color.')
    board.set_pixel_color(0, 'blue')
    board.set_pixel_color(1, 'red')
    board.set_pixel_color(2, 'green')
    board.set_pixel_color(3, 'yellow')
    time.sleep(sleep_time)
    board.clear_all()

    # let's turn off all LEDs on the board
    board.clear_all()
    print()


def main():
    """
    Main logic of this script is on this functions which
    calls the demo function 3 times setting the brightness to
    different levels.

    Returns:
        None.
    """

    # Instantiate the StatusBoard object.
    board = StatusBoard()

    # Run the demo function which by default
    # it has the brightness level set to 255.
    demo(board)
    time.sleep(sleep_time)
    # Change brightness to 128.
    board.brightness = 128
    # Run demo again.
    demo(board)
    time.sleep(sleep_time)
    # Change again the brightness.
    board.brightness = 65
    # Another demo.
    demo(board)
    time.sleep(sleep_time)
    # Change again the brightness.
    board.brightness = 25
    # Last demo.
    demo(board)

    # Let's color the board with a random color
    # using the get_random_color which returns a seudo
    # random color.
    print("Setting random colors to each pixel.")
    board.set_pixel_random_color(0)
    board.set_pixel_random_color(1)
    board.set_pixel_random_color(2)
    board.set_pixel_random_color(3)
    time.sleep(sleep_time * 2)
    board.clear_all()

