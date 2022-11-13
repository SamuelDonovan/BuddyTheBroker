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

# From libtimer
from .libtimer import Timer

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
    camera_device: int = 0

    # The resolution (veritical pixel count).
    resolution: int = 240

    # The frames per second.
    framerate: int = 10

    # Brightness (0-100%), defaults to 50%.
    brightness: int = 65

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
    trading_increment: int = 1

    timer = Timer(trading_increment)

    trading = Trading(
        keyring.get_password("robinhood", "username"),
        keyring.get_password("robinhood", "password"),
        keyring.get_password("robinhood", "qr_code"),
    )

    # Index used to iterate over all stocks.
    index = 0

    # Get first stock to potentially be traded.
    stock = Stocks(index)

    # Display the first stock symbol.
    display.write(stock.symbol)

    # Counter used to determine the number of frames
    # Buddy has been detected in.
    buddy_present_count: int = 0
    buddy_present_threshold: int = 60

    # For this project holding keeping ten stocks
    # in rotation seems like a good round numeber
    stocks_to_hold: int = 10

    # --------------- #
    # -- Main loop -- #
    # --------------- #

    while True:
        # If Buddy has been detected enough to exceed the threshold.
        if buddy_present_count > buddy_present_threshold:
            # Free up funds. The Robinhood API seems to keep track
            # of their "instrument ID" for the securities owned by
            # an account rather than the direct ticker. This
            # "instrument ID" needs converted back to a stock
            # ticker (symbol) to make use of the wrapper functions
            # within the Trading class.
            if (1 / stocks_to_hold) > trading.liquidity():
                LRP = trading.get_least_recently_purchased()
                LRP_ticker = stock.find_ticker_by_instrument_id(LRP["instrument_id"])
                trading.sell_quantity(LRP_ticker, LRP["quantity"])

            # Buy, buy, buy!!
            trading.buy_with_current_funds(stock.symbol)
            buddy_present_count = 0
            # Reset the top bar showing the number of frames
            # remaining that Buddy must be detected for the purchase
            # to go through.
            display.loading_bar(0, True)

        # If its time to get a new stock.
        if timer.get_timer_hit():
            timer.restart_timer()
            index += 1 % stock.size()
            stock = Stocks(index)
            # Update the display symbol.
            display.write(stock.symbol)
            # Restart counter for new stock.
            buddy_present_count = 0

        # Update the bottom display loading bar showing the amount of time left
        # for the current stock.
        display.loading_bar(timer.timer(), False)

        # Increment counter each time Buddy is seen by the camera.
        if camera.present():
            buddy_present_count += 1
            # Increment the top bar showing the number of frames
            # remaining that Buddy must be detected for the purchase
            # to go through.
            display.loading_bar(
                int(buddy_present_count / buddy_present_threshold * 100), True
            )


if __name__ == "__main__":
    main()
