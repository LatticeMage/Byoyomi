# main.py
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QTimer
from screen_capture import ScreenCapture
from button import SpeechButton
import threading
import time
from pynput import mouse
from state import GameState

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Capture Example")
        self.setGeometry(100, 100, 200, 100) # smaller window

        self.speech_button = SpeechButton("Start Turn", self)
        self.screen_capture = ScreenCapture()
        self.game_state = GameState("AI Playing")  # Initialize with AI playing first
        self.diff_threshold = 200
        self.diff_delay = 2  # Delay before diff monitoring
        self.last_ai_play_time = 0
        self.ai_waiting_for_diff = False

        layout = QVBoxLayout()
        layout.addWidget(self.speech_button)
        layout.setAlignment(self.speech_button, Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)
        
        self.diff_label = QLabel("Diff: 0", self)
        self.status_label = QLabel("Status: AI Playing", self)
        layout.addWidget(self.diff_label)
        layout.addWidget(self.status_label)
        self.diff_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        
        self.capture_timer = QTimer(self)
        self.capture_timer.timeout.connect(self.update_frame)
        self.capture_timer.start(1000) # Capture every 1 second
        
        # Start the mouse click listener thread
        self.mouse_listener_thread = threading.Thread(target=self.start_mouse_listener, daemon=True)
        self.mouse_listener_thread.start()


    def update_frame(self):
        diff_count = self.screen_capture.capture_and_calculate_diff()
        self.diff_label.setText(f"Diff: {diff_count}")
        self.status_label.setText(f"Status: {self.game_state.get_state()}")

        if self.game_state.get_state() == "AI Playing":
           self._check_ai_turn(diff_count)
        


    def _check_ai_turn(self, diff_count):
      current_time = time.time()
      if not self.ai_waiting_for_diff:
        self.ai_waiting_for_diff = True
        self.last_ai_play_time = current_time

      elif current_time - self.last_ai_play_time > self.diff_delay:
        if diff_count > self.diff_threshold:
            print("AI Turn End, Start Human Count Down")
            self.ai_waiting_for_diff = False
            self.game_state.set_state("Human Playing")
            self.speech_button.start_countdown()
           

    def start_mouse_listener(self):
        """Starts the mouse listener thread using pynput."""
        def on_click(x, y, button, pressed):
            if pressed: # Capture only on click down
                if self.game_state.get_state() == "Human Playing":
                   print("Switch to AI Playing")
                   self.speech_button.stop_countdown()
                   self.game_state.set_state("AI Playing")
                elif self.game_state.get_state() == "AI Playing":
                   print("AI already Playing")
                    

        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())