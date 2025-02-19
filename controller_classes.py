from base_classes import User, Model, Camera
from user_database import Database
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
#FIXME Need to change how we want to save the data, since we can't save type User to JSON
class UserController:
    def __init__(self, user_db: str):
        self._db = Database(user_db)
        self._active_users = None

    def load_user_database(self) -> dict:
        self._active_users = self._db.load_db()

    def create_user(self, name, proficiency):
        if not self._active_users:
            self.load_user_database()
        if name not in [user._name for user in self._active_users.values()]:
            new_user = User(name, proficiency)
            self._active_users[name] = new_user
            self.save_user_database()
        else:
            return Exception

    def delete_user(self, user):
        if user._name in self._active_users:
            self._active_users.pop(user._name)
            self.save_user_database()
        else:
            raise Exception("Cannot delete! User not found")

    def update_user(self, name, score):
        # need to update score before proficiency, as proficiency is based off score
        if name in self._active_users:
            self._active_users[name].update_score(score)
            self._active_users[name].update_proficiency()
            self.save_user_database()
        else:
            raise Exception("Cannot update! User not found")
    
    def get_user(self, user):
        return self._active_users.get(user._name)
    
    def save_user_database(self):
        if not self._active_users:
            raise Exception("No users to save.")
        user_db={}
        for user_name, user_data in self._active_users.items():
            user_db[user_name] = {
                "proficiency": user_data._proficiency
            }
        self._db.save_db(user_db)