from base_classes import User, Model, Camera
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
    def __init__(self, user_db=None):
        self._active_users = {}
        if user_db != None:
            self.load_user_database(user_db)

    def load_user_database(self, user_db=None):
        if user_db != None:
            #TODO: check for user database file and load saved user profiles
            pass

    def create_user(self, name, proficiency):
        if name not in [user._name for user in self._active_users.values()]:
            new_user = User(name, proficiency)
            self._active_users[name] = new_user
        else:
            return Exception

    def delete_user(self, user):
        if user._name in self._active_users:
            self._active_users.pop(user._name)
        else:
            raise Exception("Cannot delete! User not found")

    def update_user(self, name, score):
        # need to update score before proficiency, as proficiency is based off score
        if name in self._active_users:
            self._active_users[name].update_score(score)
            self._active_users[name].update_proficiency()
        else:
            raise Exception("Cannot update! User not found")
    
    def get_user(self, user):
        return self._active_users.get(user._name)
    
    def save_user_database(self):
        if not self._active_users:
            raise Exception("No users to save.")
        for user in self._active_users.values():
            user.save_profile()