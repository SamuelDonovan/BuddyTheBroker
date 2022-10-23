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
    # Initialization
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s:%(name)s:%(filename)s:%(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )

    camera = Camera(
        # 0,
        os.path.join(os.path.dirname(__file__), "libcamera/data/randomCatVideo.mkv"),
        os.path.join(os.path.dirname(__file__), "libcamera/data/randomCatVideoOutput.mp4"),
        # 240,
        None, #240,
        # 10,
        None, #10,
        os.path.join(
            os.path.dirname(__file__), "libcamera/data/haarcascade_frontalcatface.xml"
        ),
    )

    for i in range(500):
        camera.coordinates()

    display = Display(enable_progress=True)

    # trading = Trading(
    #     keyring.get_password("robinhood", "username"),
    #     keyring.get_password("robinhood", "password"),
    #     keyring.get_password("robinhood", "qr_code"),
    # )

    # # Currently testing trading ability.
    # # trading.buy("UMC")
    # # trading.sell("UMC")

    # Main loop
    count = 0
    if False:
        stock = Stocks(count)
        display.write(stock.symbol)
        display.loading_bar(count * 5 % 100)
        count += 1
        time.sleep(1)


if __name__ == "__main__":
    main()
