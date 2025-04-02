'''File name: controller_classes.py
Contributers: Zoe Takacs and Wyatt Shaw
Info: SessionController and UserController class definition
'''
from base_classes import User, Model, Camera
from user_database import PickleDatabase
import logging
import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)

class SessionController:
    '''Functionalities of this class:
    - Initializes the camera and model objects
    - Makes connections between the camera, model, user classes

    Attributes:
    _camera (Camera): allows camera access
    _model (Model): allows access to model
    '''
    def __init__(self, model_fpath=None):
        self._camera = Camera()
        if model_fpath != None:
            self._model = Model(model_fpath)
        else:
            self._model = None

    def capture_and_predict(self):
        self._camera.take_image()
        if self._model != None:
            letter, probability = self._model.make_prediction(self._camera._new_image_path)
            logger.info(f'Predicted letter {letter}')
            return letter, probability
        else:
            return None, None

class UserController:
    '''Functionalities of this class:
    - Create, manage, save, and load user database

    Attributes:
    _db (PickleDatabase): user information database, stores User objects
    _active_users: dictionary of active user profiles from database
    '''
    def __init__(self, user_db: str):
        self._db = PickleDatabase(user_db)
        self._active_users = self._db.load_db()

    def load_user_database(self) -> dict: #NOTE not used, but could be for later other database loading purposes
        self._active_users = self._db.load_db()

    def create_user(self, name, proficiency):
        # ensure user does not already exist and save user to database
        if name not in self._active_users:
            new_user = User(name, proficiency)
            self._active_users[name] = new_user
            # save database right away
            self.save_user_database()
            for user in self._active_users: #for debugging
                print(f"User: {user}")
            return new_user
        else:
            logger.error("Error! User already exists.")
            return None

    def delete_user(self, user):
        if user._name in self._active_users:
            self._active_users.pop(user._name)
            self.save_user_database()
        else:
            raise Exception("Cannot delete! User not found")
        
    def update_score(self, user, new_scores, alpha=0.2, max_storage=50):
        # append latest result to score history for each letter
        for letter, result in enumerate(new_scores):
            user._score_history[letter].append(result)
            # ensure only latest 50 attempts are being stored
            if len(user._score_history[letter]) > max_storage:
                user._score_history[letter] = user._score_history[letter][-max_storage:]

        # calculate the new weighted and percent score for each letter
        for letter, _ in enumerate(user._w_let_scores):
            score, weighted_sum = 0, 0
            for j, result in enumerate(reversed(user._score_history[letter])):
                # weight decays as j increases
                weight = (1-alpha) ** j 
                score += weight * (1 if result else -1)
                weighted_sum += weight

            # weighted sum is zero when there is no history for a letter yet, so we need to prevent division by zero
            if weighted_sum > 0:
                # weighted scores are from -1 to 1 while percent scores are from 0 to 100
                user._w_let_scores[letter] = score / weighted_sum
                user._p_let_scores[letter] = ((user._w_let_scores[letter] + 1) / 2) * 100
            else:
                # Default values when there's no score history for a letter yet
                user._w_let_scores[letter] = 0  
                user._p_let_scores[letter] = 0  
        
        # calculate the overall user score as equally weighted average of letter scores
        user._overall_score = np.mean(user._p_let_scores)

    def update_user(self, name, new_scores):
        # update score before proficiency, as proficiency is based off score
        if name in self._active_users:
            self.update_score(self._active_users[name], new_scores)
            self._active_users[name].update_proficiency()
            self.save_user_database()
        else:
            raise Exception("Cannot update! User not found")
    
    def get_user(self, user):
        return self._active_users.get(user._name)
    
    def save_user_database(self):
        if not self._active_users:
            raise Exception("No users to save.")
        self._db.save_db(self._active_users)