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

    def __init__(self, username, password, qr_code, increment_minute=10):
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
        if (increment_minute > 60) or (increment_minute < 1):
            logging.error(f"Invalid time increment: {increment_minute}.")
            raise Exception(f"Invalid time increment: {increment_minute}.")
        self.increment_minute = increment_minute
        self.max_time = increment_minute * 60
        self.timer_hit = False
        self.percentage = 0
        print(self.rh.securities_owned())


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
        dollar_amount = round(dollar_amount, 2)
        shares = float(dollar_amount) / float(self.quote['ask_price'])
        self.buy_quantity(ticker, shares)

    def buy_with_current_funds(self, ticker) -> None:
        """
        Places a market buy order for provided stock ticker using the remaining account balance.

        :param ticker: Stock ticker (symbol) to be purchased.
        :type ticker: str

        :return: None.
        """
        self.buy_dollar_amount(ticker, float(self.rh.get_account()['buying_power']))


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
        quantity = round(quantity, 2)
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
            float(self.account_info["buying_power"]) - (float(self.quote['ask_price']) * float(quantity))
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

    def get_timer_hit(self) -> bool:
        """
        Class getter for the timer_hit member.

        :return: True if timer needs restarted, false otherwise.
        :rtype: bool
        """
        return self.timer_hit


    def restart_timer(self) -> bool:
        """
        Restarts the timer used in the timer function.

        The indented use case is that once the timer has been reached this function can be called to reset it.
    
        :return: True if timer successfully restarted, false otherwise.
        :rtype: bool
        """
        if self.timer_hit:
            self.timer_hit = False
            return True
        else:
            logging.warning(f"Attempting to reset a timer that has yet to be set!")
            return False

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
        dollar_amount = round(dollar_amount, 2)
        shares = float(dollar_amount) / float(self.quote['ask_price'])
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
        quantity = round(quantity, 2)
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
        logging.info(f"Sale of {ticker} sucessful.")
        logging.info(f"Current buying power is {self.account_info['buying_power']}")

    def timer(self) -> int:
        """
        Timer that returns a percentage in the form of a decimal to which a time increment (set in initializer) has been met.
        
        E.g. if the time increment is set to 10 minutes and the time is currently 1:05 the timer will return 50. If the time
        was 1:07 the timer would return 70. If the time was 12:13 the timer would return 30.

        Once the timer has reached 100% the value will be locked until reset with the restart_timer function.
    
        :return: Percentage of elapsed time on the timer.
        :rtype: int
        """
        now = datetime.datetime.now()
        seconds_remaining = now.minute % self.increment_minute * 60 + now.second
        percentage = math.ceil(seconds_remaining / self.max_time * 100)
        if (percentage < 0):
            logging.error(f"Invalid percentage: {percentage}")
            return None
        if percentage < self.percentage:
            self.percentage = percentage
            self.timer_hit = True
            return 100
        self.percentage = percentage
        return self.percentage


if __name__ == "__main__":
    raise Exception("This module is not an entry point!")
