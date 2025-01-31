# main.py

import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from screen_capture import ScreenCapture  # Import the new class
from button import SpeechButton


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Capture Example")
        self.setGeometry(100, 100, 200, 200)

        self.speech_button = SpeechButton("Say Hello", self)
        self.screen_capture = ScreenCapture()  # Instance of ScreenCapture class

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.image_label.setMinimumSize(1, 1)  # Ensure label has a minimal size initially

        layout = QVBoxLayout()
        layout.addWidget(self.speech_button)
        layout.addWidget(self.image_label)
        layout.setAlignment(self.speech_button, Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.capture_timer = QTimer(self)
        self.capture_timer.timeout.connect(self.update_frame)
        self.capture_timer.start(1000)

    def update_frame(self):
        """
        Gets the new image and if a new image is returned updates the image on screen
        """
        label_rect = self.image_label.contentsRect()
        label_width = label_rect.width()
        label_height = label_rect.height()
        
        if label_width <= 0 or label_height <= 0:
           return # can not generate a screen capture if label is to small
        
        q_img = self.screen_capture.capture_and_resize(label_width, label_height)
        
        if q_img:
            pixmap = QPixmap.fromImage(q_img)
            self.image_label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())