#!/usr/bin/env python3

# from .stocks import BuddyTheBroker
from .stocks import Stocks
from .display import Display
import logging
import time

def main():
    # Initialization
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(name)s:%(filename)s:%(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    display = Display()
    
    # Main loop
    count = 0
    while True:
        stock = Stocks(count)
        display.update(stock.symbol)
        count+=1
        time.sleep(1)

if __name__ == '__main__':
    main()
