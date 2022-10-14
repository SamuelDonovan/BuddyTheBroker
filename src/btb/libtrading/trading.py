"""
.. module:: trading
   :platform: Unix, Windows
   :synopsis: Convenience wrapper for trading functionality.

.. moduleauthor:: Samuel Mehalko <samuel.mehalko@gmail.com>

:synopis: Convenience wrapper for trading functionality.
"""

# From the Python Standard Library
import logging

# From pyrh
from pyrh import Robinhood


class Trading:
    """
    Provides a simple stock trading API using the pyrh library. As such this library is only compatiable with Robinhood accounts.

    :param username: Username of account to log into, in the form of an email.
    :type username: str
    :param password: password of account to log into.
    :type password: str
    :param qr_code: QR code of account to log into, needed to avoid full two step verification process for each login.
    :type qr_code: str
    """

    def __init__(self, username, password, qr_code):
        """
        Constructor method.
        """
        self.rh = Robinhood()
        if self.rh.login(
            username=username,
            password=password,
            qr_code=qr_code,
        ):
            logging.info(f"Signed in to robinhood account {username}.")
        else:
            logging.error(f"Failed to sign in to robinhood account {username}.")
            raise Exception(f"Failed to sign in to robinhood account {username}.")
        account_info = self.rh.get_account()

    def buy(self, ticker) -> None:
        """
        Places a market buy order of quantity one for provided stock ticker.

        :param ticker: Stock ticker (symbol) to be purchased.
        :type ticker: str

        :return: None.
        """
        self.account_info = self.rh.get_account()
        self.quote = self.rh.get_quote(ticker)
        logging.info(f"Buy triggered for {ticker}.")
        logging.info(f"Current ask price is {self.quote['ask_price']}.")
        logging.info(f"Current buying power is {self.account_info['buying_power']}")
        logging.info(
            f"Buying power after purchase {float(self.account_info['buying_power']) - float(self.quote['ask_price'])}"
        )

        # Verify purchasing power sufficent for purchase.
        if 0 > (
            float(self.account_info["buying_power"]) - float(self.quote["ask_price"])
        ):
            logging.warning(f"Failed to purchase {ticker}, insufficient buying power!")
            return
        self.rh.place_market_buy_order(
            symbol=ticker,
            instrument_URL=self.rh.instrument(ticker)["url"],
            time_in_force="GFD",
            quantity=1,
        )
        self.account_info = self.rh.get_account()
        logging.info(f"Purchase of {ticker} sucessful.")
        logging.info(f"Remaining buying power is {self.account_info['buying_power']}")

    def sell(self, ticker) -> None:
        """
        Places a market sell order of quantity one for provided stock ticker.

        :param ticker: Stock ticker (symbol) to be sold.
        :type ticker: str

        :return: None.
        """
        self.account_info = self.rh.get_account()
        self.quote = self.rh.get_quote(ticker)
        logging.info(f"Sell triggered for {ticker}.")
        logging.info(f"Current bid price is {self.quote['bid_price']}.")
        logging.info(f"Current buying power is {self.account_info['buying_power']}")
        logging.info(
            f"Buying power after sell {float(self.account_info['buying_power']) + float(self.quote['bid_price'])}"
        )

        # Verify stock is owned.
        stocks_owned = self.rh.securities_owned()
        stock_to_sell_instrument_url = self.rh.instrument(ticker)["url"]

        can_sell = False
        for stock in stocks_owned["results"]:
            if (
                stock_to_sell_instrument_url.strip("/").rsplit("/")[-1]
                == stock["url"].strip("/").rsplit("/")[-1]
            ):
                can_sell = True
                break

        # If owned sell.
        if not can_sell:
            logging.warning(f"Security {ticker} not owned! Cannot sell!")
            return
        else:
            logging.info(f"Security {ticker} found within securities owned.")
        self.rh.place_market_sell_order(
            symbol=ticker,
            instrument_URL=stock_to_sell_instrument_url,
            time_in_force="GFD",
            quantity=1,
        )
        self.account_info = self.rh.get_account()
        logging.info(f"Sale of {ticker} sucessful.")
        logging.info(f"Current buying power is {self.account_info['buying_power']}")


if __name__ == "__main__":
    raise Exception("This module is not an entry point!")
