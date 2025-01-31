# button.py

from PySide6.QtWidgets import QPushButton
import pyttsx3
import threading
import time

from state import GameState

class SpeechButton(QPushButton):
    def __init__(self, text="Say Something", parent=None):
        super().__init__(text, parent)
        self.clicked.connect(self.start_countdown)
        self.engine = pyttsx3.init()
        self.countdown_thread = None
        self.is_counting = False
        self.game_state = GameState()

    def start_countdown(self):
        if self.game_state.get_state() != "Human Playing":
             return
        
        if self.is_counting:
            self.stop_countdown() # Stop if button is press again while counting.

        self.is_counting = True  # Set the flag to true again
        self.countdown_thread = threading.Thread(target=self._countdown_speech)
        self.countdown_thread.start()

    def _countdown_speech(self):
      countdown_numbers = ["九", "八", "七", "六", "五", "四", "三", "二", "一"]
      start_time = time.time()
      for i, number in enumerate(countdown_numbers):
        if not self.is_counting or self.game_state.get_state() != "Human Playing":
            return

        expected_time = start_time + i + 1
        self.engine.say(number)
        self.engine.runAndWait()
        time_to_wait = expected_time - time.time()
        if time_to_wait > 0:
           time.sleep(time_to_wait)

      if self.is_counting and self.game_state.get_state() == "Human Playing":
        self.engine.say("超時")
        self.engine.runAndWait()
      self.is_counting = False

    def stop_countdown(self):
        self.is_counting = False
        if self.countdown_thread and self.countdown_thread.is_alive():
            self.countdown_thread.join()
        self.countdown_thread = None


    def set_text_to_speak(self, text):
        self.text_to_speak = text