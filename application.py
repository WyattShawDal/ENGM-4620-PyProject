import sys
import logging

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QStackedWidget
from PyQt5.QtGui import QPalette, QColor, QPixmap

from base_classes import User
from user_database import Database
from controller_classes import SessionController, UserController
from random import shuffle



# log info for testing; alternative to print() statement
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Functionalities of MainWindow:
        - Create screen widgets
        - Toggle between widgets
    
    Attributes: 
        _current_user (string): username of the current user
        _
    """
    def __init__(self):
        super().__init__()
        logger.info("Entered MainWindow")

        self.setMinimumSize(750, 500)
        self.setWindowTitle("Sign Language Learner")

        self._current_user = None

        self._main_menu_scn = MainMenu(self)
        self._choose_lesson_scn = ChooseLesson(self)
        self._lesson1_scn = Lesson1(self)
        self._session_controller = SessionController()
        self._user_controller = UserController("our_users")

        self._stacked_widget = QStackedWidget()
        self._stacked_widget.addWidget(self._main_menu_scn)
        self._stacked_widget.addWidget(self._choose_lesson_scn)
        self._stacked_widget.addWidget(self._lesson1_scn)

        self.setCentralWidget(self._stacked_widget)
        self._stacked_widget.setCurrentWidget(self._main_menu_scn)

    def switch_to_screen(self, screen):
        self._stacked_widget.setCurrentWidget(screen)

"""Functionalities of MainMenu:
    - Have user sign up
    - TODO: have users saved to user can simply login
"""
class MainMenu(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi("mainmenuGUI.ui", self)
        self.signupButton.clicked.connect(self.sign_up)

    def sign_up(self):
        self.parent._current_user = self.usernameEdit.text()
        self.parent._user_controller.create_user(self.parent._current_user, self.comboBox.currentText())        
        self.parent.switch_to_screen(self.parent._choose_lesson_scn)

"""Functionalities of ChooseLesson:
    - Have user choose what lesson they want to try
    - For now only one lesson available
"""
class ChooseLesson(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi("chooselessonGUI.ui", self)
        self.lesson1Button.clicked.connect(self.choose_lesson_1)

    def choose_lesson_1(self):
        self.parent.switch_to_screen(self.parent._lesson1_scn)

"""Functionalities of Lesson1:
    - Cycle through all letters of the alphabet randomly
    - Check that user is doing it correctly and save their score
"""
class Lesson1(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi("lessonGUI.ui", self)
        self.reset_lesson()
    
    def reset_lesson(self):
        self._score = 0
        self._current_prompt = None
        self._pixmap = QPixmap()
        self._alphabet_generator = self.alphabet_generator()
        self.next_question()

    @staticmethod
    def alphabet_generator():
        alphabet = list('abcdefghijklmnopqrstuvwxyz')
        shuffle(alphabet)
        for letter in alphabet:
            yield letter

    def next_question(self):
        try:
            try:
                self.button.clicked.disconnect()
            except TypeError:
                pass
            self.questionBox.setText("Please sign the letter below:")
            self._current_prompt = next(self._alphabet_generator)
            self.promptBox.setText(self._current_prompt)
            self.button.setText("Take Picture")
            self.button.clicked.connect(self.result)
        except StopIteration:
            self.display_score()

    def result(self):
        try:
            self.button.clicked.disconnect()
        except TypeError:
            pass
        letter, probability = self.parent._session_controller.capture_and_predict()
        self._pixmap.load('new_image.png')
        self.image.setPixmap(self._pixmap)
        self.image.update()
        if self._current_prompt == letter:
            self.promptBox.setText("Correct!")
            self._score += 1
        else: 
            self.promptBox.setText(f"Incorrect. Correct answer: {letter}")
        self.questionBox.setText("Result:")
        self.promptBox.setText("Insert result here.")
        self.button.setText("Next")
        self.button.clicked.connect(self.next_question)

    def display_score(self):
        try:
            self.button.clicked.disconnect()
        except TypeError:
            pass
        self.questionBox.setText("Lesson complete!")
        self.promptBox.setText(f"Final score: {self._score}/26")
        self.parent._user_controller.update_user(self.parent._current_user, self._score)
        self.button.setText("Finish")
        self.button.clicked.connect(self.return_to_choose_lesson)
    
    def return_to_choose_lesson(self):
        self.parent.switch_to_screen(self.parent._choose_lesson_scn)
        self.reset_lesson()

# Set the palette of the window, not sure if needed rn or if .ui files can take care of this
app = QApplication(sys.argv)
dark_palette = QPalette()
dark_palette.setColor(QPalette.Window, QColor(60, 70, 95))
dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
dark_palette.setColor(QPalette.Base, QColor(60, 70, 95))
dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
dark_palette.setColor(QPalette.Button, QColor(100, 140, 190))
dark_palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
app.setPalette(dark_palette)

window = MainWindow()
window.show()

try:
    sys.exit(app.exec())
except SystemExit:
    print("Exiting app.")