from fastai.vision.all import *
import cv2

# proficiency levels in points
MIN_LEVEL = 10
MED_LEVEL = 20
MAX_LEVEL = 30

"""Functionalities of the Model class: 
    - load the model 
    - make predictions on single images
"""
class Model:
    def __init__(self, model_fpath):
        try:
            self._loaded_model = load_learner(Path('.')/model_fpath)
        except:
            print("Error! Model could not be loaded.")
    
    def make_prediction(self, img_path):
        try:
            img = PILImage.create(img_path)
            img = img.resize((192, 192))
            predicted_letter, _, probability = self._loaded_model.predict(img)
            return predicted_letter, probability
        except:
            print("Error! Cannot open image.")

"""Functionalities for the User class: 
    - create/edit/view a profile
    - keep track of their scores on various trials
    - display their progress over time

    NOTE: could have different levels of user which have access to different prompt sets or types of services;
    this could allow us to implement inheritance
"""
class User:
    _num_users = 0
    def __init__(self, name, proficiency):
        self._name = name
        self._proficiency = proficiency
        self._score = 0

    def display_profile(self): # eventually make an Application class that can display and edit profile info
        return ("User: ", self._name, "\nProficiency: ", self._proficiency)

    def update_profile(self): # eventually not needed
        new_name = input("Enter new profile name or * to cancel: ")
        setattr(self, '_name', new_name) and (result:= (f"New name: {self._name}")) if new_name != '*' else (result:= ("Cancelled."))
        return result
    
    def update_score(self, new_score):
        self._score += new_score

    def check_score(self):
        return self._score

    def update_proficiency(self):
        if self._score < MIN_LEVEL:
            self._proficiency = "Beginner"
        elif self._score < MED_LEVEL:
            self._proficiency = "Intermediate"
        elif self._score < MAX_LEVEL:
            self._proficiency = "Advanced"
        else:
            self._proficiency = "Signed Language Sensei"
    
    def check_proficiency(self):
        return self._proficiency

    def save_profile(self):
        #TODO: save user data and scores to JSON db
        pass

"""Functionalities of the camera class:
    - to take a picture and save it in a cache
    - to open/view an image
"""
class Camera:
    def __init__(self):
        try: 
            self._camera = cv2.VideoCapture(0)
        except: 
            print("Error! Camera cannot be opened")
        self._new_image_path = None

    def take_image(self):
        result, image = self._camera.read()
        if result:
            img_path = "new_image.png" #NOTE: could make this a global or passed variable
            image = cv2.resize(image, (192, 192))
            cv2.imwrite(img_path, image)
            self._new_image_path = img_path
            return (f"Image saved as {img_path}")
        else:
            return ("Image not captured.")

    def view_image(self, img_path=None, wid=192, len=192): # probably not needed long term
        image = cv2.imread(img_path if img_path != None else self._new_image_path)
        cv2.imshow("Image Window", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
