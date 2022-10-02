#!/usr/bin/env python3

import os
from pandas import read_csv
from random import randrange
import logging

class Stocks():
    data_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/Russell1000Index.csv")
    if not os.path.exists(data_file):
        logging.error(f"Invalid file path: {data_file}")
    data = read_csv(data_file)

    def __init__(self, index = None):
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
        return self.__country

    @property
    def description(self):
        return self.__description

    @property
    def divdend(self):
        return self.__divdend

    @property
    def market_cap(self):
        return self.__market_cap

    @property
    def sector(self):
        return self.__sector

    @property
    def symbol(self):
        return self.__symbol

if __name__ == '__main__':
    raise Exception("This module is not an entry point!")
