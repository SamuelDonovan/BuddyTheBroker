"""
.. module:: display
   :platform: Unix, Windows
   :synopsis: A simple display API.

.. moduleauthor:: Samuel Mehalko <samuel.mehalko@gmail.com>

:synopis: A simple display API used to display short strings.
"""

# From the Python Standard Library
import logging
from tkinter import ttk
import tkinter as tk
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
        self,
        bg_color="grey55",
        fg_color="blue",
        font="System 80",
        enable_progress=False,
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

        if self.enable_progress:
            # Make the top progress bar (tpb).
            self.tpb = ttk.Progressbar(
                self.root,
                orient="horizontal",
                mode="determinate",
                length=self.__pb_size,
            )
            self.tpb.pack(side=tk.TOP)

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
            # Make the bottom progress bar (bpb).
            self.bpb = ttk.Progressbar(
                self.root,
                orient="horizontal",
                mode="determinate",
                length=self.__pb_size,
            )
            self.bpb.pack(side=tk.BOTTOM)

        logging.info(
            f"Creating display object, background: {bg_color}, forground: {fg_color}, font: {font}"
        )
        self.current_text = "Starting"
        self.current_progress = 0

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
        # Exit function early if no value is added.
        if text == self.current_text:
            return None
        self.current_text = text
        self.display_text.set(text.upper())
        self.label.pack(expand=True)
        self.root.update()
        logging.info(f"Writing text: {text}")

    def loading_bar(self, progress, bar) -> None:
        """
        Writes string to the screen.

        :param progress: Percentage, in the form of a number spanning zero to one hundred, to set the progress bar to.
        :type progress: int

        :param bar: True to update the top bar, false to update the bottom bar.
        :type bar: bool

        :return: None
        """
        # Exit function early if no value is added.
        if progress == self.current_progress:
            return None
        self.current_progress = progress
        if not self.enable_progress:
            logging.warning(
                f"This Display object does not support progress bars. Please enable the use of progress bars during construction."
            )
            return
        if None == progress:
            logging.error(f"Invalid progress percentage: {progress}")
            raise TypeError(f"Invalid progress percentage: {progress}")
        if bar:
            self.tpb["value"] = progress
        else:
            self.bpb["value"] = progress
        self.root.update()


if __name__ == "__main__":
    raise Exception("This module is not an entry point!")
