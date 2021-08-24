import gc
import json
import os
import socket
import time

import machine

from status_board import StatusBoard

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pixels</title> </head>
    <body> <h1>ESP8266 Pixel values</h1>
        <table border="1"> <tr><th>Pixel</th><th>Value</th><th>RGB</th></tr> %s </table>
        <form action="/" method="get">
            <label for="pixel">Pixel number:</label>
            <input type="text" id="pixel" name="pixel"><br><br>
            <label for="value">Pixel value:</label>
            <input type="text" id="value" name="value"><br><br>
            <button type="submit">Change color</button>
        </form>
        <br><br><br>
        <table>
            <tr>
                <td>
                    <form action="/" method="get">
                        <button type="submit">Reload</button>
                    </form>
                </td>
                <td>
                    <form action="/">
                        <button type="submit" id="cl" name="cl" value="yes">Clear all</button>
                    </form>
                </td>
            </tr>
        </table>
        <br><br>
    </body>
</html>
"""

default_config = {0: [0, 0, 0], 1: [0, 0, 0], 2: [0, 0, 0], 3: [0, 0, 0]}

config_file = "config.json"
board = StatusBoard()
board.clear_all()
board.brightness = 16


def save_config(config):
    """Write configuration to a JSON file.

    Args:
        config (dict): Configuration used.
    """
    with open(config_file, "w") as js_file:
        json.dump(config, js_file)


def load_config():
    """Get configuration from JSON file.

    Returns:
        dict: Configuration loaded.
    """
    with open(config_file, "r") as js_file:
        try:
            data = json.load(js_file)
        except ValueError:
            save_config(default_config)
            machine.reset()
    return data


def colorize(count=1, sleep_time=25):
    """Show all colors in sequence.

    Args:
        count (int, optional): Number of loop to make. Defaults to 1.
        sleep_time (int, optional): Delay between pixel color. Defaults to 25.
    """
    for _ in range(count):
        colors = list(board.colors.keys())
        colors.remove("nocolor")

        for color in colors:
            for pixel in range(board.neopixels):
                board.set_pixel_color(pixel, color)
                time.sleep_ms(sleep_time)

    board.clear_all()


def hex_to_rgb(value):
    """Convert hexadecimal string to rgb tuple

    Args:
        value (str): Hexadecimal value to be converted

    Returns:
        tuple: (R,G,B)
    """
    if value.startswith("#"):
        value = value.lstrip("#")

    lv = len(value)
    return tuple(
        int(value[index : index + lv // 3], 16) for index in range(0, lv, lv // 3)
    )


def rgb_to_hex(rgb):
    """Convertion from (R,G,B) tuple into string

    Args:
        rgb (tuple): Tuple to be converted.

    Returns:
        str: Hexadecimal color.
    """
    return "#%02x%02x%02x" % rgb


def set_board_pixel_color(arguments, config):
    """Show a given color on a given pixel.

    Args:
        arguments (str): String from the request with all data.
        config (dict): Configuration used.
    """
    try:
        pixel = int(arguments[0])
        value = hex_to_rgb(arguments[1:].replace("&value=", ""))
        config[str(pixel)] = value
        save_config(config)
        board.set_pixel_raw_color(pixel, value)
    except ValueError:
        pass


def main():

    if config_file not in os.listdir():
        save_config(default_config)

    colorize(count=2)
    current_config = load_config()

    for pixel in current_config.keys():
        board.set_pixel_raw_color(int(pixel), tuple(current_config[pixel]))

    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)

    print("listening on", addr)

    while True:
        cl, addr = s.accept()
        print("connection on", addr)
        print("Free in: %d" % gc.mem_free())
        cl_file = cl.makefile("rwb", 0)

        while True:
            h = cl_file.readline()
            gotten_msg = b"GET /?pixel="
            clear = b"GET /?cl=yes"

            if gotten_msg in h:
                msg = h.decode("utf-8").split("/?pixel=")
                arguments = msg[1][:-11]
                set_board_pixel_color(arguments, current_config)

            elif clear in h:
                board.clear_all()
                for pixel in range(board.neopixels):
                    current_config[str(pixel)] = [0, 0, 0]
                save_config(default_config)

            if h == b"" or h == b"\r\n":
                break

        rows = list()

        for pixel in range(board.neopixels):
            pixel_value = current_config[str(pixel)]
            rows.append(
                "<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
                % (pixel, str(pixel_value), rgb_to_hex(tuple(pixel_value)))
            )

        response = html % "\n".join(rows)

        try:
            cl.sendall(response)

        except OSError as error:
            print("Error trying to send all information. %s" % error)
            pass

        finally:
            cl.close()

        print("Free out: %d" % gc.mem_free())


if __name__ == "__main__":
    main()
