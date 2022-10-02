#!/usr/bin/env python3

import os
from pandas import read_csv
from random import randrange
import logging


class Stocks:
    """
    Provides stock data for a selected stock from the top 1000 measured by market capitial.

    :param index: Index for selected stock into the list of stocks sorted by market capitalization. If not specified a random index will be selected. defaults to None.
    :type index: int, optional
    """

    data_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "data/Russell1000Index.csv"
    )
    if not os.path.exists(data_file):
        logging.error(f"Invalid file path: {data_file}")
    data = read_csv(data_file)

    def __init__(self, index=None):
        """
        Constructor method.
        """
        MAX_INDEX = 999
        if MAX_INDEX < index:
            logging.error(f"Invalid passed index: {index}")
            raise ValueError(f"Invalid passed index: {index}")
        elif None != index:
            self.index = index
        else:
            self.index = randrange(MAX_INDEX)
        logging.debug(f"Stock index selected: {self.index}")
        self.__country = self.data.Country[self.index]
        self.__description = self.data.Description[self.index]
        self.__divdend = self.data.DividendYield[self.index]
        self.__market_cap = self.data.MarketCap[self.index]
        self.__sector = self.data.GICSSector[self.index]
        self.__symbol = self.data.Symbol[self.index]

    @property
    def country(self):
        """
        Returns the contry of the selected stock.
        For this data set all stocks are U.S. stocks.

        :return: Country.
        """
        return self.__country

    @property
    def description(self):
        """
        Returns a short description of the selected stock.
        :return: Stock description.
        """
        return self.__description

    @property
    def divdend(self):
        """
        Returns the dividend yield of the selected stock.
        A dividend is a distribution of a portion of a company's earnings, decided by the board of directors, paid to a class of its shareholders.

        :return: Dividend yield.
        """
        return self.__divdend

    @property
    def market_cap(self):
        """
        Returns the market capitalization of the selected stock.
        Market capitalization is the total dollar value of all outstanding shares of a company at the current market price.

        :return: Market capitalization.
        """
        return self.__market_cap

    @property
    def sector(self):
        """
        The sector of the selected stock.
        The market sector is a part of the economy, usually broader than an industry. Two industries may form part of one market sector.
        The eleven sectors are:
        1. Communication services
        2. Consumer discretionary
        3. Consumer staples
        4. Energy
        5. Financials
        6. Healthcare
        7. Industrials
        8. Information technology
        9. Materials
        10. Real estate
        11. Utilities

        :return: Sector.
        """
        return self.__sector

    @property
    def symbol(self):
        """
        The symbol (ticker) of the selected stock.
        A stock symbol is a unique series of letters assigned to a security for trading purposes. 
        e.g. AAPL for the computer company Apple.

        :return: Symbol.
        """
        return self.__symbol


if __name__ == "__main__":
    raise Exception("This module is not an entry point!")
