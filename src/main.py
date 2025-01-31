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
from screen_capture import ScreenCapture
from button import SpeechButton
import threading
from pynput import mouse
from state import GameState

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Capture Example")
        self.setGeometry(100, 100, 200, 200)

        self.speech_button = SpeechButton("Say Hello", self)
        self.screen_capture = ScreenCapture()
        self.game_state = GameState()  # Get the GameState instance

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.image_label.setMinimumSize(1, 1)

        layout = QVBoxLayout()
        layout.addWidget(self.speech_button)
        layout.addWidget(self.image_label)
        layout.setAlignment(self.speech_button, Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.capture_timer = QTimer(self)
        self.capture_timer.timeout.connect(self.update_frame)
        self.capture_timer.start(1000) # Capture every 1 second

        # Start the mouse click listener thread
        self.mouse_listener_thread = threading.Thread(target=self.start_mouse_listener, daemon=True)
        self.mouse_listener_thread.start()
        
        self.diff_label = QLabel("Diff: 0", self)
        layout.addWidget(self.diff_label)
        self.diff_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

    def update_frame(self):
        label_rect = self.image_label.contentsRect()
        label_width = label_rect.width()
        label_height = label_rect.height()

        if label_width <= 0 or label_height <= 0:
            return
        
        pixmap, diff_count = self.screen_capture.capture_and_resize(label_width, label_height)
        
        if pixmap:
            self.image_label.setPixmap(pixmap)
        
        self.diff_label.setText(f"Diff: {diff_count}")

    def start_mouse_listener(self):
        """Starts the mouse listener thread using pynput."""
        def on_click(x, y, button, pressed):
            if pressed: # Capture only on click down
                if self.game_state.get_state() == "Human Playing":
                    print("Switch to AI Playing")
                    self.game_state.set_state("AI Playing")

        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())