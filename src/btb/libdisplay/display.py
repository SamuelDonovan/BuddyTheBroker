"""
.. module:: display
   :platform: Unix, Windows
   :synopsis: A simple display API.

.. moduleauthor:: Samuel Mehalko <samuel.mehalko@gmail.com>

:synopis: A simple display API used to display short strings.
"""

# From the Python Standard Library
import datetime
import logging
from tkinter import ttk
import tkinter as tk
import math
import os


class Display:
    """
    Provides display to write strings to.

    :param bg_color: Screen background color, defaults to red
    :type bg_color: str, optional
    :param fg_color: Screen foreground color, defaults to green
    :type fg_color: str, optional
    :param font: String font, defaults to System 80
    :type font: str, optional
    """

    def __init__(
        self, bg_color="red", fg_color="green", font="System 80", enable_progress=False
    ):
        """
        Constructor method.
        """
        os.environ["DISPLAY"] = ":0"
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.font = font
        self.enable_progress = enable_progress
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=self.bg_color)
        self.display_text = tk.StringVar()

        self.__pb_size = 700

        self.label = tk.Label(
            self.root,
            textvariable=self.display_text,
            font=self.font,
            justify=tk.CENTER,
            bg=self.bg_color,
            fg=self.fg_color,
        )
        self.label.pack(expand=True)

        if self.enable_progress:
            self.pb = ttk.Progressbar(
                self.root,
                orient="horizontal",
                mode="determinate",
                length=self.__pb_size,
            )
            self.pb.pack(side=tk.BOTTOM)

        logging.info(
            f"Creating display object, background: {bg_color}, forground: {fg_color}, font: {font}"
        )

    def write(self, text) -> None:
        """
        Writes string to the screen.

        :param text: Text to write to the screen
        :type text: str

        :return: None
        """
        if str != type(text):
            logging.error(f"Invalid text to display: {text} - Must be of type str.")
            raise TypeError(f"Invalid text to display: {text} - Must be of type str.")
        self.display_text.set(text.upper())
        self.label.pack(expand=True)
        self.root.update()
        logging.info(f"Writing text: {text}")

    def loading_bar(self, progress) -> None:
        """
        Writes string to the screen.

        :param progress: Percentage, in the form of a number spanning zero to one hundred, to set the progress bar to.
        :type progress: int

        :return: None
        """
        if not self.enable_progress:
            logging.warning(
                f"This Display object does not support progress bars. Please enable the use of progress bars during construction."
            )
            return
        if None == progress:
            logging.error(f"Invalid progress percentage: {progress}")
            raise TypeError(f"Invalid progress percentage: {progress}")
        self.pb["value"] = progress

    def __time_mod(self, increment_minute=1):
        if (increment_minute > 60) or (increment_minute < 1):
            logging.error(f"Invalid time increment: {increment_minute}")
            return None
        max_time = increment_minute * 60
        now = datetime.datetime.now()
        seconds_remaining = now.minute % increment_minute * 60 + now.second
        percentage = math.ceil(seconds_remaining / max_time * 100)
        if (percentage > 100) or (percentage < 0):
            logging.error(f"Invalid percentage: {percentage}")
            return None
        return percentage


if __name__ == "__main__":
    raise Exception("This module is not an entry point!")
