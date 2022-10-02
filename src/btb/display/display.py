#!/usr/bin/env python3

import datetime
import logging
from tkinter import ttk
import tkinter as tk
import math
import os


class Display:
    def __init__(
        self, bg_color="red", fg_color="green", font="System 80", bar_length="800"
    ):
        os.environ["DISPLAY"] = ":0"
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.font = font
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=self.bg_color)
        self.label = tk.Label(
            self.root,
            text="Starting...",
            font=self.font,
            justify=tk.CENTER,
            bg=self.bg_color,
            fg=self.fg_color,
        )
        self.label.pack(expand=True)

        # self.pb = ttk.Progressbar(
        #     self.root,
        #     orient='horizontal',
        #     mode='determinate',
        #     length=bar_length
        # )
        # self.pb.pack(side = tk.BOTTOM, pady=100)

        logging.info(
            f"Creating display object, background: {bg_color}, forground: {fg_color}, font: {font}"
        )

    def write(self, text_in):
        self.label.destroy()
        self.label = tk.Label(
            self.root,
            text=text_in.upper(),
            font=self.font,
            justify=tk.CENTER,
            bg=self.bg_color,
            fg=self.fg_color,
        )
        self.label.pack(expand=True)
        self.root.update()
        logging.info(f"Writing text: {text_in}")

    def loading_bar(self, progress):
        if None == progress:
            logging.error(f"Invalid progress percentage: {progress}")
            return ERROR
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

    def update(self, text_in=None):
        if None != text_in:
            self.write(text_in)
        # self.loading_bar(self.__time_mod())
        self.root.update()
