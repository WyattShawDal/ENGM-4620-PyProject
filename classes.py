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
    def __init__(self, model_file_path):
        self._loaded_model = load_learner(Path('.')/model_file_path)
    
    def make_prediction(self, img):
        prediction = self._loaded_model.predict(img)
        return prediction

"""Functionalities for the User class: 
    - create/edit/view a profile
    - keep track of their scores on various trials
    - display their progress over time

    NOTE: could have different levels of user which have access to different prompt sets or types of services;
    this could allow us to implement inheritance
"""
class User:
    def __init__(self, name, proficiency):
        self._name = name
        self._proficiency = proficiency
        self._score = 0

    def display_profile(self):
        print("User: ", self._name, "\nProficiency: ", self._proficiency)

    def update_profile(self):
        new_name = input("Enter new profile name or * to cancel: ")
        #TODO: Figure out why the print statement is not working
        (setattr(self, '_name', new_name) and print(f"New name: {self._name}")) if new_name != '*' else print("Cancelled.")
    
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
        #save user data and scores to JSON db
        pass

"""Functionalities of the camera class:
    - to take a picture and save it in a cache
    - to open/view an image
"""
class Camera:
    def __init__(self):
        self._camera = VideoCapture(0)
        self._new_image = {"img_path": None, "img_tensor": None}
        pass

    def take_image(self):
        result, image = self._camera.read()
        if result:
            img_path = "new_image.png" #NOTE: could make this a global or passed variable
            imwrite(img_path, image)
            self._new_image["img_path"] = img_path
            print(f"Image saved as {img_path}")
        else:
            print("Image not captured.")

    def open_image(self, img_path=None): #NOTE: is this a necessary function? Could just create tensor upon image capture
        if img_path != None:
            return PILImage.opn(img_path)
        else:
            self._new_image["img_tensor"] = PILImage.opn(img_path)

    def view_image(self, img=None, wid=192, len=192):
        if img != None:
            img.to_thumb(wid, len)
        else:
            self._new_image["img_tensor"].to_thumb(wid, len)

"""To add (maybe): 
    - prompt class: facilitates generation of questions, flipping through questions, and redoing failed questions
    - application class: facilitates window generation and sets up GUI
"""