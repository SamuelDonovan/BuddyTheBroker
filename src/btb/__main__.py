#!/usr/bin/env python3

# From the Python Standard Library
import logging
import os
import time

# From keyring
import keyring

# From libcamera
from .libcamera import Camera

# From libdisplay
from .libdisplay import Display

# From libstocks
from .libstocks import Stocks

# From libtrading
from .libtrading import Trading


def main():
    # -------------------- #
    # -- Initialization -- #
    # -------------------- #
    
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s:%(name)s:%(filename)s:%(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )

    # Camera. Zero is the first camera available to the device.
    camera_device : int = 0

    # The resolution (veritical pixel count).
    resolution : int = 240

    # The frames per second.
    framerate : int = 10

    # Brightness (0-100%), defaults to 50%.
    brightness : int = 65 

    camera = Camera(
        camera_device,
        os.path.join(os.path.dirname(__file__), "libcamera/data/output.mp4"),
        resolution,
        framerate,
        brightness,
        os.path.join(
            os.path.dirname(__file__), "libcamera/data/haarcascade_frontalcatface.xml"
        ),
    )

    display = Display(enable_progress=True)

    # Number of minutes a stock will be available for trade.
    trading_increment : int = 10

    trading = Trading(
        keyring.get_password("robinhood", "username"),
        keyring.get_password("robinhood", "password"),
        keyring.get_password("robinhood", "qr_code"),
        trading_increment
    )

    # Index used to iterate over all stocks.
    index = 0

    # Get first stock to potentially be traded.
    stock = Stocks(index)

    # Display the first stock symbol.
    display.write(stock.symbol)

    # Counter used to determine the number of frames
    # Buddy has been detected in.
    buddy_present_count : int = 0
    buddy_present_threshold : int = 60

    # --------------- #
    # -- Main loop -- #
    # --------------- #

    while True:
        # If Buddy has been detected enough to exceed the threshold.
        if buddy_present_count > buddy_present_threshold:
            # Free up funds.
            # trading.sell_least_recently_purchased()
            # Buy, buy, buy!!
            trading.buy_with_current_funds(stock.symbol)
            buddy_present_count = 0
            # Reset the top bar showing the number of frames
            # remaining that Buddy must be detected for the purchase
            # to go through.  
            display.loading_bar(0, True)

        # If its time to get a new stock.
        if trading.get_timer_hit():
            trading.restart_timer()
            index += 1 % stock.size()
            stock = Stocks(index)
            # Update the display symbol.
            display.write(stock.symbol)
            # Restart counter for new stock.
            buddy_present_count = 0

        # Update the bottom display loading bar showing the amount of time left
        # for the current stock.
        display.loading_bar(trading.timer(), False)

        # Increment counter each time Buddy is seen by the camera.
        if camera.present():
            buddy_present_count += 1
            # Increment the top bar showing the number of frames
            # remaining that Buddy must be detected for the purchase
            # to go through.
            display.loading_bar(int(buddy_present_count/buddy_present_threshold*100), True)

if __name__ == "__main__":
    main()
