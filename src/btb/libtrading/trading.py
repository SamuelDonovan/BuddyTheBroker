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
        rh = Robinhood()
        if rh.login(
            username=username,
            password=password,
            qr_code=qr_code,
        ):
            logging.info(f"Signed in to robinhood account {username}.")
        else:
            logging.error(f"Failed to sign in to robinhood account {username}.")
            raise Exception(f"Failed to sign in to robinhood account {username}.")


if __name__ == "__main__":
    raise Exception("This module is not an entry point!")
