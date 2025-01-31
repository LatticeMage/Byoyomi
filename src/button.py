# button.py

from PySide6.QtWidgets import QPushButton
import pyttsx3

class SpeechButton(QPushButton):
    def __init__(self, text="Say Something", parent=None):
        super().__init__(text, parent)
        self.clicked.connect(self.speak_text)
        self.engine = pyttsx3.init()

    def speak_text(self):
      self.engine.say("十九八七六五四三二一超時")
      self.engine.runAndWait()

    def set_text_to_speak(self, text):
      self.text_to_speak = text