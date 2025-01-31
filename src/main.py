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
from PySide6.QtCore import Qt, QTimer
import mss
from PIL import Image

from button import SpeechButton


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Capture Example")
        self.setGeometry(100, 100, 800, 800)

        self.speech_button = SpeechButton("Say Hello", self)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(self.speech_button)
        layout.addWidget(self.image_label)
        layout.setAlignment(self.speech_button, Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.capture_timer = QTimer(self)
        self.capture_timer.timeout.connect(self.capture_and_update)
        self.capture_timer.start(100)


    def capture_and_update(self):
        """Captures the entire screen and updates the QLabel."""
        with mss.mss() as sct:
            sct_img = sct.grab(sct.monitors[0])
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            q_img = QImage(img.tobytes(), img.size[0], img.size[1], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())