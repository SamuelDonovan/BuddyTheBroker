#!/usr/bin/env python3

# From the python standard library
import logging
import os
import sys

# From keyring
try:
    import keyring
except:
    logging.error("keyring import failed.")
    ImportError("Failed to import keyring packaged needed for log in info.")

# From stocks
from .stocks import Stocks

# # From pyrh
# pyrh_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pyrh')
# sys.path.append(pyrh_path)
# from pyrh import Robinhood


class BuddyTheBroker:
    def main():
        rh = Robinhood()
        robinhood_username = keyring.get_password("robinhood", "username")
        robinhood_password = keyring.get_password("robinhood", "password")
        robinhood_qr_code = keyring.get_password("robinhood", "qr_code")
        if rh.login(
            username=robinhood_username,
            password=robinhood_password,
            qr_code=robinhood_qr_code,
        ):
            logging.info(f"Signed in to robinhood account {robinhood_username}.")
        else:
            logging.error(
                f"Failed to sign in to robinhood account {robinhood_username}. Please verify account username, password, and qr_code are set with the keyring module."
            )
            raise Exception

        stock = Stocks()
        logging.info(f"Stock symbol: {stock.symbol}")
        logging.info(f"Stock description: {stock.description}")

        inst = rh.instruments("AAPL")
        logging.info(f"Stock instrument: {inst}")

        # rh.place_limit_buy_order(instrument_URL=None, symbol="AAPL", time_in_force="GFD", price=1.00, quantity=1)


if __name__ == "__main__":
    raise Exception("This module is not an entry point!")
