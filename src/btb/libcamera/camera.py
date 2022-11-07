"""
.. module:: camera
   :platform: Unix, Windows
   :synopsis: Convenience wrapper for camera functionality.

.. moduleauthor:: Samuel Mehalko <samuel.mehalko@gmail.com>

:synopis: Convenience wrapper for camera functionality.
"""

# From the Python Standard Library
from datetime import datetime
import logging
import os

# From Open Computer Vision
import cv2

class Camera:
    """
    Camera module for computer vision with several variable options.

    :param input: Path to input if using a file. If using camera use 0.
    :type input: str
    :param output: Path to output file generated with image detection rectangle overlay.
    :type output: str
    :param resolution: Resolution to use for camera/ouput. (ex: 144, 240, 360, 720, 1080).
    :type resolution: int
    :param fps: Frames per second.
    :type fps: int
    :param brightness: Brightness as a whole number percentage. (ex 50, 100, 15).
    :type brightness: int
    :param detector: Cascade classifier detector xml file.
    :type detector: str
    """

    def __init__(self, input, output, resolution, fps, brightness, detector):
        self.cap = cv2.VideoCapture(input)
        if 0 == input:
            os.system("v4l2-ctl --set-ctrl=rotate=90")
        if resolution:
            if resolution not in [144, 240, 360, 480, 720, 1080]:
                logging.error(f"Invalid resolution selected: {resolution}")
                raise RuntimeError(f"Invalid resolution selected: {resolution}")
            self.resolution = resolution
            frame_width = int(resolution * 4 / 3)
            frame_height = int(resolution)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        else:
            frame_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            frame_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        logging.debug(
            f"Frame resolution set to {str(frame_height)}, {str(frame_width)}."
        )

        if fps:
            self.cap.set(cv2.CAP_PROP_FPS, fps)
        else:
            fps = self.cap.get(cv2.CAP_PROP_FPS)
        logging.debug(f"Frames per second set to {str(fps)}.")

        if brightness:
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, int(brightness))
        else:
            brightness = self.cap.get(cv2.CAP_PROP_BRIGHTNESS)
        logging.debug(f"Brightness set to {str(brightness)}%.")

        self.output = cv2.VideoWriter(
            os.path.join(os.path.dirname(__file__), output),
            cv2.VideoWriter_fourcc(*"mp4v"),
            int(fps),
            (int(frame_width), int(frame_height))
        )
        self.detector = cv2.CascadeClassifier(detector)

    def __del__(self) -> None:
        """
        Camera destructor. Releases the input and ouptut files.

        :return: None
        """
        self.output.release()
        self.cap.release()

    def coordinates(self):
        """
        Finds image of interest within a frame returns the coordinates.

        :return: Coordinates of the image of interest.
        """
        ret, frame = self.cap.read()
        if not ret:
            logging.error(f"Failure to open {input}.")
            raise RuntimeError(f"Failure to open {input}.")
        else:
            # adding filled rectangle on each frame
            rects = self.detector.detectMultiScale(frame)
            for (i, (x, y, w, h)) in enumerate(rects):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            font = cv2.FONT_HERSHEY_PLAIN
            color = (255, 255, 255)
            scale = 1
            thickness = 1
            origin = (10, self.resolution - 5)

            # Add timestamp.
            cv2.putText(frame, str(datetime.now()), origin,
                font, scale, color, thickness, cv2.LINE_AA)

            # writing the new frame in output
            self.output.write(frame)
            return rects

    def present(self) -> bool:
        """
        Determines if the image of interest is present on the current frame of the image.

        :return: True if a the image of interest was detected or not.
        :rtype: bool
        """
        if () != self.coordinates():
            logging.debug(f"Image detected at {datetime.now()}!")
            return True
        else:
            return False


if __name__ == "__main__":
    raise Exception("This module is not an entry point!")
