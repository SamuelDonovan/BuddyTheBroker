"""
.. module:: timer
   :platform: Unix, Windows
   :synopsis: Convenience wrapper for timer functionality.

.. moduleauthor:: Samuel Mehalko <samuel.mehalko@gmail.com>

:synopis: Convenience wrapper for timer functionality.
"""

# From the Python Standard Library
import datetime
import logging
import math


class Timer:
    """
    Provides a simple timer that will hit ever x modulo minutes.

    :param increment_minute: Number of minutes before timer hits.
    :type increment_minute: int
    """

    def __init__(self, increment_minute=1):
        """
        Constructor method.
        """
        self.increment_minute = increment_minute
        self.max_time = increment_minute * 60
        self.timer_hit = False
        self.percentage = 0

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
        if percentage < 0:
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
