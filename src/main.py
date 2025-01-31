import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import pyttsx3

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text to Speech Example")
        self.setGeometry(100, 100, 300, 200)

        self.button = QPushButton("Say Hello", self)
        self.button.clicked.connect(self.say_hello)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.engine = pyttsx3.init()

    def say_hello(self):
        self.engine.say("十九八七六五四三二一超時")
        self.engine.runAndWait()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())