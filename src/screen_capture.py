# screen_capture.py

import mss
from PIL import Image
from typing import Tuple
import numpy as np

class ScreenCapture:
    def __init__(self):
        self.last_image_data = None

    def capture_and_calculate_diff(self) -> int:
        """
        Captures the entire screen and calculates pixel difference from the last capture.
        """

        with mss.mss() as sct:
            monitor = sct.monitors[0]
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
             # Convert to numpy array for easier comparison
            current_image_data = np.array(img, dtype=np.uint8).flatten()

            # Calculate pixel difference
            diff_count = 0
            if self.last_image_data is not None:
                diff_count = np.sum(self.last_image_data != current_image_data)
            
            self.last_image_data = current_image_data
            
            return diff_count