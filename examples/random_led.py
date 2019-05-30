"""
Example script to set a random color on a random pixel each time
the button is pressed.

In this script we are using a button connected to GPIO 0 on one end
and the other end is connected to GND.
"""
import time
import urandom
import machine

from status_board import StatusBoard

board = StatusBoard()


def change_random_led(pin):
    """
    Callback function that will be called every time
    the button is pressed.

    Args:
        pin: `machine.Pin` object.

    Returns:
        None.
    """
    time.sleep_ms(100)
    pixel = urandom.getrandbits(2)
    board.set_pixel_random_color(pixel)


button = machine.Pin(0, machine.Pin.IN)
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=change_random_led)
