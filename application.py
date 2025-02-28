import sys
import logging
import numpy as np

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QStackedWidget, QMessageBox
from PyQt5.QtGui import QPalette, QColor, QPixmap

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
    """
    def __init__(self):
        super().__init__()
        logger.info("Entered MainWindow")

        self.setMinimumSize(750, 650)
        self.setWindowTitle("Sign Language Learner")

        self._current_user = None

        # initialize base class controllers
        self._session_controller = SessionController()
        self._user_controller = UserController("our_users")

        # initialize all application screens
        self._main_menu_scn = LoginPage(self)
        self._choose_lesson_scn = MainMenu(self)
        self._lesson1_scn = Lesson1(self)
        self._profile_scn = ViewProfile(self)

        # add application screens to stacked widget
        self._stacked_widget = QStackedWidget()
        self._stacked_widget.addWidget(self._main_menu_scn)
        self._stacked_widget.addWidget(self._choose_lesson_scn)
        self._stacked_widget.addWidget(self._lesson1_scn)
        self._stacked_widget.addWidget(self._profile_scn)
        self.setCentralWidget(self._stacked_widget)
        
        self._stacked_widget.setCurrentWidget(self._main_menu_scn)

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
        loadUi("loginpageGUI.ui", self)
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
        self.parent.switch_to_screen(self.parent._choose_lesson_scn)
        logger.info("Sign up successful.")

    def login(self):
        name = self.loginusernameEdit.text()
        if name in self.parent._user_controller._active_users:
            self.parent._current_user = name
            logger.info(f"Logged in as: {name}")
            self.parent.switch_to_screen(self.parent._choose_lesson_scn)
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
        self.lesson1Button.clicked.connect(self.choose_lesson_1)
        self.profileButton.clicked.connect(self.choose_view_profile)

    def choose_lesson_1(self):
        logger.info("Lesson 1 selected.")
        self.parent.switch_to_screen(self.parent._lesson1_scn)
    
    def choose_view_profile(self):
        logger.info("Entering profile view.")
        self.parent.switch_to_screen(self.parent._profile_scn)

"""Functionalities of Lesson1:
    - Cycle through all letters of the alphabet randomly
    - Check that user is doing it correctly and save their score
"""
class Lesson1(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi("lessonGUI.ui", self)
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
        alphabet = list('abcdefghijklmnopqrstuvwxyz')
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
            self.promptBox.setText(f"Incorrect. Correct answer: {letter}")
            self._score.append(0)
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
        self.promptBox.setText(f"Final score: {np.sum(self._score)}/26")
        self.parent._user_controller.update_user(self.parent._current_user, self._score)
        self.button.setText("Finish")
        self.button.clicked.connect(self.return_to_choose_lesson)
    
    def return_to_choose_lesson(self):
        self.parent.switch_to_screen(self.parent._choose_lesson_scn)
        self.reset_lesson()
        logger.info("Lesson 1 completed.")

"""Functionalities of ViewProfile:
    - Displays the user's name, overall score, and proficiency level
    - Updates each time the screen is accessed
"""
class ViewProfile(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi("profileviewGUI.ui", self)
        self.returnButton.clicked.connect(self.exit_profile_view)

    def showEvent(self, event):
        # method run automatically when screen is shown inherited from QWidget->QDialog->ViewProfile
        super().showEvent(event)
        self.update_user_info()
    
    def update_user_info(self):
        try:
            self.usernameslotLabel.setText(self.parent._current_user)
            
            score = str(self.parent._user_controller._active_users[self.parent._current_user]._overall_score)
            logger.info("Found the score.")
            self.scoreslotLabel.setText(score)
            logger.info("Updated the score.")

            proficiency = self.parent._user_controller._active_users[self.parent._current_user]._proficiency
            logger.info("Found the proficiency.")
            self.proficiencyslotLabel.setText(proficiency)
            logger.info("Updated the proficiency.")
        except:
            logger.info("Error. No active user.") 

    def exit_profile_view(self):
        self.parent.switch_to_screen(self.parent._choose_lesson_scn)
        logger.info("Exiting profile view.")
        
# Set the palette of the window, not sure if needed rn or if .ui files can take care of this
app = QApplication(sys.argv)
dark_palette = QPalette()
dark_palette.setColor(QPalette.Window, QColor(60, 70, 95))
dark_palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
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