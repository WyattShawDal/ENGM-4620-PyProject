from base_classes import User, Model, Camera
from user_database import PickleDatabase
import logging
import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
"""Functionalities of this class:
    - Initializes the camera and model objects
    - Makes connections between the camera, model, user classes
"""
class SessionController:
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
            return letter, probability
        else:
            return None, None

"""Functionalities of this class:
    - Create, manage, save, and load user database
"""
class UserController:
    def __init__(self, user_db: str):
        self._db = PickleDatabase(user_db)
        self._active_users = self._db.load_db()

    def load_user_database(self) -> dict: #NOTE not used, but could be for later other database loading purposes
        self._active_users = self._db.load_db()

    def create_user(self, name, proficiency):
        if name not in self._active_users:
            new_user = User(name, proficiency)
            self._active_users[name] = new_user
            self.save_user_database()
            for user in self._active_users:
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
        
    def update_score(self, user, new_scores, alpha=0.5, max_storage=50):
        # append latest result to score history for each letter
        for i, result in enumerate(new_scores):
            user._score_history[i].append(result)
            # ensure only latest 50 attempts are being stored
            if len(user._score_history[i]) > max_storage:
                user._score_history[i] = user._score_history[i][-max_storage:]

        # calculate the new weighted and percent score for each letter
        for i, _ in enumerate(user._w_let_scores):
            score, weighted_sum = 0, 0
            for j, result in enumerate(reversed(user._score_history[i])):
                weight = (1-alpha) ** j
                score += weight * (1 if result else -1)
                weighted_sum += weight
            user._w_let_scores[i] = score / weighted_sum
            print(f"Letter weighted scores: {user._w_let_scores[i]}")
            user._p_let_scores[i] = ((score + 1) / 2) * 100
            print(f"Letter percentage scores: {user._p_let_scores[i]}")
        
        # calculate the overall user score
        user._overall_score = np.mean(user._p_let_scores)
        print(f"Overall score: {user._overall_score}")

    def update_user(self, name, new_scores):
        # need to update score before proficiency, as proficiency is based off score
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