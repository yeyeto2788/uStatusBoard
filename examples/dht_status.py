import dht
import time
import machine

from status_board import StatusBoard

# Modify the variable value below
# for delaying the time between readings.
sleep_time = 5
# Minimum temperature accepted
min_temp = 16
# Maximum temperature accepted
max_temp = 25
# Minimum humidity condition
min_hum = 30
# Maximum humidity condition
max_hum = 50


def main():
    board = StatusBoard()
    dht_sensor = dht.DHT11(machine.Pin(13))

    while True:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        # If temperature is between min and max temp it is all good (green)
        if min_temp < temperature < max_temp:
            board.set_pixel_color(0, 'green')
        # If temperature is higher than max temp it is hot (red)
        elif temperature < max_temp:
            board.set_pixel_color(0, 'red')
        # If temperature is lower than min temp it is cold (blue)
        else:
            board.set_pixel_color(0, 'blue')

        # If humidity is between min and max it is all good (green)
        if min_hum < humidity < max_hum:
            board.set_pixel_color(2, 'green')
        # If humidity is higher than max it bad for us and potentially
        # fuel for growth of harmful bacteria (red) and if it's lower
        # we can get our eyes dry.
        else:
            board.set_pixel_color(2, 'red')

        # Whit the statement above we don't do readings too often.
        time.sleep(sleep_time)
