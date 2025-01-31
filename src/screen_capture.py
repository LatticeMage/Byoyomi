# screen_capture.py

import mss
from PIL import Image
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QSize
from typing import Tuple
import numpy as np

class ScreenCapture:
    def __init__(self):
        self.last_size = QSize(0, 0) # Initial size for check
        self.last_image_data = None
        

    def capture_and_resize(self, target_width: int, target_height: int) -> tuple[QPixmap | None, int] | tuple[None, 0]:
        """
        Captures the entire screen, resizes it to fit the specified dimensions while maintaining aspect ratio,
        and returns a QImage and pixel difference from the last capture.
        Returns (None, 0) if target dimensions are invalid
        """
        if target_width <= 0 or target_height <= 0:
            return None, 0

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
            
             # Convert to numpy array for easier comparison
            current_image_data = np.array(img, dtype=np.uint8).flatten()

            # Calculate pixel difference
            diff_count = 0
            if self.last_image_data is not None:
                diff_count = np.sum(self.last_image_data != current_image_data)
            
            self.last_image_data = current_image_data

            # Convert to QImage
            q_img = QImage(img.tobytes(), img.size[0], img.size[1], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)


            if self.last_size.width() != target_width or self.last_size.height() != target_height:
                self.last_size = QSize(target_width, target_height)
            
            return pixmap, diff_count