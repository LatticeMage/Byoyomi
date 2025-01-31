# main.py

import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QTimer, QSize
import mss
from PIL import Image

from button import SpeechButton


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Capture Example")
        self.setGeometry(100, 100, 200, 200)

        self.speech_button = SpeechButton("Say Hello", self)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.image_label.setMinimumSize(1, 1) # Ensure label has a minimal size initially

        layout = QVBoxLayout()
        layout.addWidget(self.speech_button)
        layout.addWidget(self.image_label)
        layout.setAlignment(self.speech_button, Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.capture_timer = QTimer(self)
        self.capture_timer.timeout.connect(self.capture_and_update)
        self.capture_timer.start(1000)

    def capture_and_update(self):
        """Captures the entire screen, resizes it to fit the QLabel's content area while maintaining aspect ratio, and updates the QLabel."""
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
            # Get the QLabel's content area dimensions
            label_rect = self.image_label.contentsRect()
            label_width = label_rect.width()
            label_height = label_rect.height()

            # Check if content area dimensions are valid
            if label_width <= 0 or label_height <= 0:
                return  # Skip if the label has no valid content size yet

            # Calculate the aspect ratio
            image_ratio = img.width / img.height if img.height else 1  # avoid div by zero
            label_ratio = label_width / label_height if label_height else 1  # avoid div by zero

            # Determine the target size while maintaining aspect ratio
            if image_ratio > label_ratio:
                # Image is wider, fit to width
                w = label_width
                h = int(label_width / image_ratio) if image_ratio else label_height
            else:
                # Image is taller or same ratio, fit to height
                h = label_height
                w = int(label_height * image_ratio) if image_ratio else label_width

            # Resize the image
            img = img.resize((w, h), Image.Resampling.LANCZOS)

            # Convert to QImage and update the QLabel
            q_img = QImage(img.tobytes(), img.size[0], img.size[1], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.image_label.setPixmap(pixmap)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())