import sys
import logging
import numpy as np

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QStackedWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from controller_classes import SessionController, UserController
from random import shuffle
from stylesheet import light_mode_stylesheet, sunset_mode_stylesheet, dark_mode_stylesheet


# log info for testing; alternative to print() statement
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

style_mode = sunset_mode_stylesheet

class MainWindow(QMainWindow):
    """Functionalities of MainWindow:
        - Create screen widgets
        - Toggle between widgets
    
    Attributes: 
        _current_user (string): username of the current user
    """
    def __init__(self):
        super().__init__()
        logger.info("Entered MainWindow")

        self.setMinimumSize(800, 570)
        self.setWindowTitle("Sign Language Learner")

        self._current_user = None

        # initialize base class controllers
        self._session_controller = SessionController('Zoya_Letters_EP10.pkl')
        self._user_controller = UserController('our_users')

        # initialize all application screens
        self._login_scn = LoginPage(self)
        self._mainmenu_scn = MainMenu(self)
        self._lesson1_scn = Lesson1(self)

        # add application screens to stacked widget
        self._stacked_widget = QStackedWidget()
        self._stacked_widget.addWidget(self._login_scn)
        self._stacked_widget.addWidget(self._mainmenu_scn)
        self._stacked_widget.addWidget(self._lesson1_scn)
        self.setCentralWidget(self._stacked_widget)
        
        self._stacked_widget.setCurrentWidget(self._login_scn)

    def switch_to_screen(self, screen):
        self._stacked_widget.setCurrentWidget(screen)

"""Functionalities of LoginPage:
    - Have user sign up
    - TODO: have users saved to user can simply login
"""
class LoginPage(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ui = loadUi("loginpageGUI.ui", self)
        self.setStyleSheet(style_mode)
        self.signupButton.clicked.connect(self.sign_up)
        self.loginButton.clicked.connect(self.login)

    def sign_up(self):
        if self.usernameEdit.text() == "":
            QMessageBox(QMessageBox.NoIcon, "Error!", "No username specified!     ", QMessageBox.Ok).exec_()
            return
        self.parent._current_user = self.usernameEdit.text()
        while(self.parent._user_controller.create_user(self.parent._current_user, self.comboBox.currentText()) == None):
            QMessageBox(QMessageBox.NoIcon, "Error!", "That username is taken!     ", QMessageBox.Ok).exec_()
            return
        self.parent.switch_to_screen(self.parent._mainmenu_scn)
        logger.info("Sign up successful.")

    def login(self):
        name = self.loginusernameEdit.text()
        if name in self.parent._user_controller._active_users:
            self.parent._current_user = name
            logger.info(f"Logged in as: {name}")
            self.parent.switch_to_screen(self.parent._mainmenu_scn)
        else:
            QMessageBox(QMessageBox.NoIcon, "Error!", "Account does not exist!     ", QMessageBox.Ok).exec_()
            logger.info(f"User {name} does not exist.")

"""Functionalities of MainMenu:
    - Have user choose what lesson they want to try
    - For now only one lesson available
"""
class MainMenu(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi("mainmenuGUI.ui", self)
        self.setStyleSheet(style_mode)
        self.logoutButton.clicked.connect(self.logout)
        self.lesson1Button.clicked.connect(self.choose_lesson_1)

    def choose_lesson_1(self):
        logger.info("Lesson 1 selected.")
        self.parent.switch_to_screen(self.parent._lesson1_scn)
    
    def showEvent(self, event):
        # method run automatically when screen is shown inherited from QWidget->QDialog->ViewProfile
        super().showEvent(event)
        self.update_user_info()
    
    def update_user_info(self):
        try:
            self.usernameLabel.setText(self.parent._current_user)
            
            score = str(self.parent._user_controller._active_users[self.parent._current_user]._overall_score)
            logger.info("Found the score.")
            self.scoreLabel.setText(score)
            logger.info("Updated the score.")

            proficiency = self.parent._user_controller._active_users[self.parent._current_user]._proficiency
            logger.info("Found the proficiency.")
            self.proficiencyLabel.setText(proficiency)
            logger.info("Updated the proficiency.")
        except:
            logger.info("Error. No active user.")
    
    def logout(self):
        self.parent.switch_to_screen(self.parent._login_scn)
        logger.info("Logged out.")

"""Functionalities of Lesson1:
    - Cycle through all letters of the alphabet randomly
    - Check that user is doing it correctly and save their score
"""
class Lesson1(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi("lessonGUI.ui", self)
        self.setStyleSheet(style_mode)
        self.retakeButton.hide()
        self.retakeButton.clicked.connect(self.take_image)
        self.reset_lesson()
    
    def reset_lesson(self):
        self._score = []
        self._current_prompt = None
        self._pixmap = QPixmap()
        self._alphabet_generator = self.alphabet_generator()
        self.next_question()

    @staticmethod
    def alphabet_generator():
        alphabet = list('abcde')
        shuffle(alphabet)
        for letter in alphabet:
            yield letter

    def next_question(self):
        try:
            self.questionBox.setText("Please sign the letter below:")
            self._current_prompt = next(self._alphabet_generator)
            self.promptBox.setText(self._current_prompt)
            self.take_image()
        except StopIteration:
            self.display_score()
    
    def take_image(self):
        try:
            self.button.clicked.disconnect()
        except TypeError:
            pass
        self.button.setText("Take Picture")
        self.button.clicked.connect(self.check_image)
        self.retakeButton.hide()

    def check_image(self):
        try:
            self.button.clicked.disconnect()
        except TypeError:
            pass
        letter, probability = self.parent._session_controller.capture_and_predict()
        self._pixmap.load('new_image.png')
        self.image.setPixmap(self._pixmap)
        self.image.update()
        self.button.setText("Submit")
        self.button.clicked.connect(lambda: self.result(letter))
        self.retakeButton.show()

    def result(self, letter):
        self.retakeButton.hide()
        try:
            self.button.clicked.disconnect()
        except TypeError:
            pass
        if self._current_prompt == letter:
            self.promptBox.setText("Correct!")
            self._score.append(1)
        else: 
            self.promptBox.setText(f"Incorrect. Correct answer: {self._current_prompt}")
            self._score.append(0)
        self.questionBox.setText("Result:")
        self.button.setText("Next")
        self.button.clicked.connect(self.next_question)

    def display_score(self):
        try:
            self.button.clicked.disconnect()
        except TypeError:
            pass
        self.questionBox.setText("Lesson complete!")
        self.promptBox.setText(f"Final score: {np.sum(self._score)}/5")
        self.parent._user_controller.update_user(self.parent._current_user, self._score)
        self.button.setText("Finish")
        self.button.clicked.connect(self.return_to_choose_lesson)
    
    def return_to_choose_lesson(self):
        self.parent.switch_to_screen(self.parent._mainmenu_scn)
        self.reset_lesson()
        logger.info("Lesson 1 completed.")
        
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
app = QApplication(sys.argv)

window = MainWindow()
window.show()

try:
    sys.exit(app.exec())
except SystemExit:
    print("Exiting app.")