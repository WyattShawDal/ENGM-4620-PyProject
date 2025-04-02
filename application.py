'''File name: application.py
Contributers: Zoe Takacs and Wyatt Shaw
Info: Main application and screen classes
'''
import sys
import logging
import numpy as np

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QStackedWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from controller_classes import SessionController, UserController
from random import shuffle
from stylesheet import Light, Sunset, Dark

# log info for testing; alternative to print() statement
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    '''Functionalities of MainWindow:
        - Create screen widgets
        - Toggle between widgets
    
    Attributes: 
        _current_user (string): username of the current user
        _session_controller (SessionController): sets up Camera and Model
        _user_controller (UserController): sets up user database
        _login_scn (LoginPage): initializes the login page
        _mainmenu_scn (MainMenu): initializes the main menu page
        _lesson1_scn (Lesson1): initializes the first lesson page
        _stacked_widget (QStackedWidget): stores the applicatin pages
    '''
    def __init__(self):
        super().__init__()
        logger.info("Entered MainWindow")

        self.setMinimumSize(800, 570)
        self.setWindowTitle("Sign Language Learner")

        self._current_user = None

        # initialize base class controllers
        self._session_controller = SessionController('Zoya_Letters_EP10.pkl')
        self._user_controller = UserController('user_database')

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
    
    def set_style(self, style):
        logger.info(f"Changed theme to: {style}")
        if style == 'Light':
            new_theme = Light
        elif style == 'Dark':
            new_theme = Dark
        elif style == 'Sunset':
            new_theme = Sunset
        else:
            logger.info(f'Theme {style} is not available.')
            return
        self._login_scn.setStyleSheet(new_theme)
        self._mainmenu_scn.setStyleSheet(new_theme)
        self._lesson1_scn.setStyleSheet(new_theme)

    def switch_to_screen(self, screen):
        # change page that is visible
        self._stacked_widget.setCurrentWidget(screen)


class LoginPage(QMainWindow):
    '''Functionalities of LoginPage:
    - Have user sign up or login

    Attributes:
    - ui: loads the GUI features and theme
    '''
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ui = loadUi("loginpageGUI.ui", self)
        self.signupButton.clicked.connect(self.sign_up)
        self.loginButton.clicked.connect(self.login)

    def showEvent(self, event):
        # method run automatically when screen is shown inherited from QWidget->QDialog->ViewProfile
        super().showEvent(event)
        self.usernameEdit.setText("")
        self.loginusernameEdit.setText("")

    def sign_up(self):
        # get client username
        if self.usernameEdit.text() == "":
            QMessageBox(QMessageBox.NoIcon, "Error!", "No username specified!     ", QMessageBox.Ok).exec_()
            return
        self.parent._current_user = self.usernameEdit.text()

        # ensure valid username entry
        while(self.parent._user_controller.create_user(self.parent._current_user, self.comboBox.currentText()) == None):
            QMessageBox(QMessageBox.NoIcon, "Error!", "That username is taken!     ", QMessageBox.Ok).exec_()
            return
        self.parent.switch_to_screen(self.parent._mainmenu_scn)
        logger.info("Sign up successful.")

    def login(self):
        # get client username
        name = self.loginusernameEdit.text()

        # ensure user exists in database
        if name in self.parent._user_controller._active_users:
            self.parent._current_user = name
            logger.info(f"Logged in as: {name}")
            self.parent.switch_to_screen(self.parent._mainmenu_scn)
        else:
            QMessageBox(QMessageBox.NoIcon, "Error!", "Account does not exist!     ", QMessageBox.Ok).exec_()
            logger.info(f"User {name} does not exist.")

class MainMenu(QDialog):
    '''Functionalities of MainMenu:
    - Have user choose what lesson they want to try
    - For now only one lesson available
    '''
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi("mainmenuGUI.ui", self)
        self.logoutButton.clicked.connect(self.logout)
        self.checkscoreButton.clicked.connect(self.check_score)
        self.setmodeButton.clicked.connect(self.change_theme)
        self.lesson1Button.clicked.connect(self.choose_lesson_1)

    def showEvent(self, event):
        # method run automatically when screen is shown inherited from QWidget->QDialog->ViewProfile
        super().showEvent(event)
        self.update_user_info()

    def choose_lesson_1(self):
        logger.info("Lesson 1 selected.")
        self.parent.switch_to_screen(self.parent._lesson1_scn)
    
    def update_user_info(self):
        try:
            # update user info on settings page upon login/signup
            self.usernameLabel.setText(self.parent._current_user)
            
            score = str(round(self.parent._user_controller._active_users[self.parent._current_user]._overall_score, 2))
            logger.info("Found the score.")
            self.scoreLabel.setText(f"{score}%")
            logger.info("Updated the score.")

            proficiency = self.parent._user_controller._active_users[self.parent._current_user]._proficiency
            logger.info("Found the proficiency.")
            self.proficiencyLabel.setText(proficiency)
            logger.info("Updated the proficiency.")

            self.letterselectComboBox.setCurrentIndex(0)
            self.letterscoreProgressBar.setValue(0)
            logger.info("Updated the letter score checker.")
        except:
            logger.info("Error. No active user.")

    def change_theme(self):
        # change style sheet to new selected theme
        self.parent.set_style(self.modeComboBox.currentText())

    def check_score(self):
        # fetch the score of the selected letter
        letter = self.letterselectComboBox.currentText()
        index = ord(letter) - ord('a')
        result = self.parent._user_controller._active_users[self.parent._current_user]._p_let_scores[index]
        self.letterscoreProgressBar.setValue(int(result))
        logger.info(f'Score {letter} = {result}')
    
    def logout(self):
        self.parent.switch_to_screen(self.parent._login_scn)
        logger.info("Logged out.")


class Lesson1(QDialog):
    '''Functionalities of Lesson1:
    - Cycle through letters of the alphabet randomly
    - Check that user is doing it correctly and save their score
    '''
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi("lessonGUI.ui", self)
        self.retakeButton.hide()
        self.retakeButton.clicked.connect(self.take_image)
        self.reset_lesson()
    
    def reset_lesson(self):
        # reset general variables an image placeholder when lesson is restarted
        self._score = []
        self._current_prompt = None
        self._pixmap = QPixmap()
        self._pixmap.load('default_img.png')
        self.image.setPixmap(self._pixmap)
        self.image.update()
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
            # prompt the user with a letter and move to take image
            self.questionBox.setText("Please sign the letter below:")
            self._current_prompt = next(self._alphabet_generator)
            self.promptBox.setText(self._current_prompt)
            self.take_image()
        except StopIteration:
            # if generator is depleted then the lesson is over
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
        try:
            # get letter prediction
            letter, _ = self.parent._session_controller.capture_and_predict()
        except:
            QMessageBox(QMessageBox.NoIcon, "Error!", "Camera not accessible!     ", QMessageBox.Ok).exec_()
            self.take_image()
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
        # if image is accepted then check result and update score accordingly 
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
        # upon lesson completion, display users lesson score
        self.questionBox.setText("Lesson complete!")
        self.promptBox.setText(f"Final score: {np.sum(self._score)}/5")
        self.parent._user_controller.update_user(self.parent._current_user, self._score)
        self.button.setText("Finish")
        self.button.clicked.connect(self.return_to_choose_lesson)
    
    def return_to_choose_lesson(self):
        self.parent.switch_to_screen(self.parent._mainmenu_scn)
        self.reset_lesson()
        logger.info("Lesson 1 completed.")
        
# Set up application as a QApplication
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
app = QApplication(sys.argv)

# Ensure of application is visible
window = MainWindow()
window.show()

# Launch application
try:
    sys.exit(app.exec())
except SystemExit:
    print("Exiting app.")