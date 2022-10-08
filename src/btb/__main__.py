#!/usr/bin/env python3

# From the Python Standard Library
import logging
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
    # Initialization
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s:%(name)s:%(filename)s:%(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )

    camera = Camera()

    display = Display(enable_progress=True)

    trading = Trading(
        keyring.get_password("robinhood", "username"),
        keyring.get_password("robinhood", "password"),
        keyring.get_password("robinhood", "qr_code"),
    )

    # Main loop
    count = 0
    while True:
        stock = Stocks(count)
        display.write(stock.symbol)
        display.loading_bar(count * 5 % 100)
        count += 1
        time.sleep(1)


if __name__ == "__main__":
    main()
