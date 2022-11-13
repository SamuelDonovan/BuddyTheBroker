"""
.. module:: trading
   :platform: Unix, Windows
   :synopsis: Convenience wrapper for trading functionality.

.. moduleauthor:: Samuel Mehalko <samuel.mehalko@gmail.com>

:synopis: Convenience wrapper for trading functionality.
"""

# From the Python Standard Library
import datetime
import logging
import math
from typing import Dict

# From pyrh
from pyrh import Robinhood


class Trading:
    """
    Provides a simple stock trading API using the pyrh library. As such this library is only compatible with Robinhood accounts.

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
            logging.info(f"Signed in to Robinhood account {username}.")
        else:
            logging.error(f"Failed to sign in to Robinhood account {username}.")
            raise Exception(f"Failed to sign in to Robinhood account {username}.")
        account_info = self.rh.get_account()
        if (increment_minute > 60) or (increment_minute < 1):
            logging.error(f"Invalid time increment: {increment_minute}.")
            raise Exception(f"Invalid time increment: {increment_minute}.")
        self.increment_minute = increment_minute
        self.max_time = increment_minute * 60
        self.timer_hit = False
        self.percentage = 0

    def buy_dollar_amount(self, ticker, dollar_amount) -> None:
        """
        Places a market buy order for provided stock ticker given a dollar amount for the amount to buy.

        :param ticker: Stock ticker (symbol) to be purchased.
        :type ticker: str
        :param dollar_amount: The dollar amount used to calculated the number of shares to buy.
        :type dollar_amount: float

        :return: None.
        """
        self.quote = self.rh.get_quote(ticker)
        dollar_amount = self.round_decimals_down(dollar_amount)
        shares = float(dollar_amount) / float(self.quote["ask_price"])
        self.buy_quantity(ticker, shares)

    def buy_with_current_funds(self, ticker) -> None:
        """
        Places a market buy order for provided stock ticker using the remaining account balance.

        :param ticker: Stock ticker (symbol) to be purchased.
        :type ticker: str

        :return: None.
        """
        self.buy_dollar_amount(ticker, float(self.rh.get_account()["buying_power"]))

    def buy_quantity(self, ticker, quantity) -> None:
        """
        Places a market buy order for provided stock ticker given a quantity to buy.

        :param ticker: Stock ticker (symbol) to be purchased.
        :type ticker: str
        :param quantity: The amount of shares to be purchased.
        :type quantity: float

        :return: None.
        """
        self.account_info = self.rh.get_account()
        self.quote = self.rh.get_quote(ticker)
        quantity = self.round_decimals_down(quantity)
        logging.info(f"Buy triggered for {ticker}.")
        logging.info(f"Current ask price is {self.quote['ask_price']}.")
        logging.info(f"Quantity is {quantity}.")
        logging.info(f"Current buying power is {self.account_info['buying_power']}")
        logging.info(f"Cost is {(float(self.quote['ask_price']) * quantity)}.")
        logging.info(
            f"Buying power after purchase {float(self.account_info['buying_power']) - (float(self.quote['ask_price']) * float(quantity))}"
        )

        # Verify purchasing power sufficient for purchase.
        if 0 > (
            float(self.account_info["buying_power"])
            - (float(self.quote["ask_price"]) * float(quantity))
        ):
            logging.warning(f"Failed to purchase {ticker}, insufficient buying power!")
            return
        self.rh.place_market_buy_order(
            symbol=ticker,
            instrument_URL=self.rh.instrument(ticker)["url"],
            time_in_force="GFD",
            quantity=quantity,
        )
        self.account_info = self.rh.get_account()
        logging.info(f"Purchase of {ticker} successful.")
        logging.info(f"Remaining buying power is {self.account_info['buying_power']}")

    def get_least_recently_purchased(self) -> Dict[str, float]:
        """
        Returns Robinhood instrument ID and quantity of least recently purchased stock.

        :return: Dictionary containing Robinhood instrument ID and quantity of least recently purchased stock.
        :rtype: dict[str, float]
        """
        stocks_owned = pd.DataFrame.from_records(self.rh.securities_owned()["results"])
        if stocks_owned.empty:
            logging.error(
                "Attempting to find least recently purchased stock, but own none!"
            )
            raise Exception(
                "Attempting to find least recently purchased stock, but own none!"
            )
        stocks_owned["updated_at"] = pd.to_datetime(stocks_owned["updated_at"])
        stocks_owned = stocks_owned.sort_values(by=["updated_at"])
        stocks_owned = stocks_owned.reset_index()

        return {
            "instrument_id": stocks_owned["instrument_id"][0],
            "quantity": stocks_owned["quantity"][0],
        }

    def liquidity(self) -> int:
        """
        Returns the integer percentage of account liquidity.
        e.g. If the account is worth $100 and currently has a buying power of $10 then
        the liquidity is 10 (10%).

        :return: Integer percentage of account liquidity.
        :rtype: int
        """
        return round((float(self.rh.get_account()["buying_power"]) / float(self.rh.portfolios()["equity"])), 2)

    def round_decimals_down(self, number: float, decimals: int = 5) -> float:
        """
        Returns a value rounded down to a specific number of decimal places.

        :param number: Number to be rounded.
        :type number: float

        :param decimals: Number of decimal place at which to round down.
        :type decimals: int

        return: Round float.
        :rtype: float
        """
        if not isinstance(decimals, int):
            raise TypeError("decimal places must be an integer.")
        elif decimals < 0:
            raise ValueError("Decimal places has to be 0 or more.")
        elif decimals == 0:
            return math.floor(number)

        factor = 10**decimals
        return round(math.floor(number * factor) / factor, decimals)

    def sell_dollar_amount(self, ticker, dollar_amount) -> None:
        """
        Places a market sell order for provided stock ticker given a dollar amount for the amount to sell.

        :param ticker: Stock ticker (symbol) to be sold.
        :type ticker: str
        :param dollar_amount: The dollar amount used to calculated the number of shares to sell.
        :type dollar_amount: float

        :return: None.
        """
        self.quote = self.rh.get_quote(ticker)
        dollar_amount = self.round_decimals_down(dollar_amount)
        shares = float(dollar_amount) / float(self.quote["ask_price"])
        self.sell_quantity(ticker, shares)

    def sell_quantity(self, ticker, quantity) -> None:
        """
        Places a market sell order for provided stock ticker given a quantity to sell.

        :param ticker: Stock ticker (symbol) to be sold.
        :type ticker: str
        :param quantity: The amount of shares to be sold.
        :type quantity: float

        :return: None.
        """
        self.account_info = self.rh.get_account()
        self.quote = self.rh.get_quote(ticker)
        quantity = self.round_decimals_down(quantity)
        logging.info(f"Sell triggered for {ticker}.")
        logging.info(f"Current bid price is {self.quote['bid_price']}.")
        logging.info(f"Current buying power is {self.account_info['buying_power']}")
        logging.info(f"Quantity is {quantity}.")
        logging.info(f"Cost is {(float(self.quote['bid_price']) * quantity)}.")
        logging.info(
            f"Buying power after sell {float(self.account_info['buying_power']) + (float(self.quote['bid_price']) * float(quantity))}"
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
            quantity=quantity,
        )
        self.account_info = self.rh.get_account()
        logging.info(f"Sale of {ticker} successful.")
        logging.info(f"Current buying power is {self.account_info['buying_power']}")


if __name__ == "__main__":
    raise Exception("This module is not an entry point!")
