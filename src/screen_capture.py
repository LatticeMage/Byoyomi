# screen_capture.py

import mss
from PIL import Image
from PySide6.QtGui import QImage
from PySide6.QtCore import QSize
from typing import Tuple

class ScreenCapture:
    def __init__(self):
        self.last_size = QSize(0, 0) # Initial size for check
        

    def capture_and_resize(self, target_width: int, target_height: int) -> QImage | None:
        """
        Captures the entire screen, resizes it to fit the specified dimensions while maintaining aspect ratio,
        and returns a QImage.
        Returns None if target dimensions are invalid
        """
        if target_width <= 0 or target_height <= 0:
            return None
        if self.last_size.width() == target_width and self.last_size.height() == target_height:
            return None # size no change

        with mss.mss() as sct:
            monitor = sct.monitors[0]
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            # Calculate the aspect ratio
            image_ratio = img.width / img.height if img.height else 1
            target_ratio = target_width / target_height if target_height else 1

            # Determine the target size while maintaining aspect ratio
            if image_ratio > target_ratio:
                w = target_width
                h = int(target_width / image_ratio)
            else:
                h = target_height
                w = int(target_height * image_ratio)

            # Resize the image
            img = img.resize((w, h), Image.Resampling.LANCZOS)

            # Convert to QImage
            q_img = QImage(img.tobytes(), img.size[0], img.size[1], QImage.Format_RGB888)
            self.last_size = QSize(target_width, target_height)
            return q_img