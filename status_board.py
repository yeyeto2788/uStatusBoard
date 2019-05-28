"""
Simple module to used with the uStatusBoard.

It uses four (4) WS2812B (aka Neopixels) connected
by default to pin 15 on the ESP8266

-------------------------------
|  _                          |
| |_| LED 0  #################|
|  _                          |
| |_| LED 1  #################|
|  _                          |
| |_| LED 2  #################|
|  _                          |
| |_| LED 3  #################|
-------------------------------
More info: https://github.com/yeyeto2788/uStatusBoard
"""
import machine
import neopixel


class StatusBoard:
    def __init__(self, pin=15, neopixels=4, brightness=255):
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.neopixels = neopixels
        self.neostrip = neopixel.Neopixel(self.pin, self.neopixels)
        self.brightness = brightness
        self.colors = {
            'nocolor': [0, 0, 0],
            'blue': [0, 0, 1],
            'green': [0, 1, 0],
            'cyan': [0, 1, 1],
            'red': [1, 0, 0],
            'magenta': [1, 0, 1],
            'yellow': [1, 1, 0],
            'white': [1, 1, 1],
        }
        self.clear_all()

    def _get_color_brightness(self, color):
        """
        Cycle through the colors and find the given key color and return the
        given color matching the brightness level.

        Args:
            color (str): Name of the color get the value from.

        Returns:
            List with color at a brightness level.
        """
        return [(c_value * self.brightness) for c_value in self.colors[color.lower()]]

    def set_pixel_color(self, led, color):
        """
        Set given color based on the brightness level on a given board LED.

        Args:
            led (int): Led position on the board.
            color (str): Name of the color.

        Returns:
            None.
        """
        self.neostrip[led] = self._get_color_brightness(color)
        self.neostrip.write()

    def clear_all(self):
        """
        Turn off all LEDs on the board.

        Returns:
            None.
        """
        for pixel in range(self.neopixels):
            self.neostrip[pixel] = (0, 0, 0)
        self.neostrip.write()

    def color_all(self, color):
        """
        Set given color based on the brightness level on all LEDs on the board.

        Args:
            color (str): Name of the color.

        Returns:
            None.
        """
        for pixel in range(self.neopixels):
            self.neostrip[pixel] = self._get_color_brightness(color)
        self.neostrip.write()
