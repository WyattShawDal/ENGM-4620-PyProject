'''File name: base_classes.py
Contributers: Zoe Takacs and Wyatt Shaw
Info: Model, User, and Camera class definition
'''
from fastai.vision.all import *
import cv2
import platform

# proficiency levels in points
MIN_LEVEL = 35.0
MED_LEVEL = 60.0
MAX_LEVEL = 85.0

# Path the file path classification when running on Windows, default is Linux
if platform.system() == 'Windows':
    import pathlib
    original_posix_path = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath

class Model:
    '''Functionalities of the Model class: 
        - load the model 
        - make predictions on single images

    Attributes: 
        _loaded_model: holds the model prediction weights and neural network algorithm
    '''
    def __init__(self, model_fpath):
        try:
            self._loaded_model = load_learner(model_fpath)
        except Exception as e:
            print(f"Error! Model could not be loaded. Error {e}")
            print(model_fpath)
    
    def make_prediction(self, img_path):
        '''Predicts what letter is depicted in the image provided to the function

        Args: 
            img_path (string): hold the relative local path to the image to be processed

        Returns:
            predicted_letter (string): upper letter identified in the image
            probability (list of ints): index corresponds to letter in the alphabet; value represents confidence on scale of 0.0 to 1.0
        '''
        try:
            img = PILImage.create(img_path)
            img = img.resize((192, 192))
            predicted_letter, _, probability = self._loaded_model.predict(img)
            return predicted_letter, probability
        except:
            print("Error! Cannot open image.")

class User:
    '''Functionalities for the User class: 
        - create/edit/view a profile
        - keep track of their scores on various trials
        - display their progress over time

    FUTURE DEVELOPMENT NOTE: could have different levels of user which have access to different prompt sets or types of services;
    this could allow us to implement inheritance

    Attributes: 
        _name (string): username
        _proficiency (string): quantized level user is on
        _score_history (int): last (up to) 50 scores for a specific letter stored as 0=incorrect or 1=correct
        _w_let_scores (int): weighted letter scores
        _p_let_scores (float): letter scores on a scale of 0-100 (%)
        _overall_score (float): equally weighted average of letter scores
    '''
    def __init__(self, name, proficiency):
        self._name = name
        self._proficiency = proficiency
        self._score_history = [[] for x in range(26)]
        self._w_let_scores = [0 for x in range(26)]
        self._p_let_scores = [0 for x in range(26)]
        self._overall_score = 0.0

    def display_profile(self): 
        return ("User: ", self._name, "\nProficiency: ", self._proficiency)

    def update_profile(self): # eventually not needed
        new_name = input("Enter new profile name or * to cancel: ")
        setattr(self, '_name', new_name) and (result:= (f"New name: {self._name}")) if new_name != '*' else (result:= ("Cancelled."))
        return result
    
    def check_score(self):
        return self._score

    def update_proficiency(self):
        if self._overall_score < MIN_LEVEL:
            self._proficiency = "Beginner"
        elif self._overall_score < MED_LEVEL:
            self._proficiency = "Intermediate"
        elif self._overall_score < MAX_LEVEL:
            self._proficiency = "Advanced"
        else:
            self._proficiency = "Signed Language Sensei"
    
    def check_proficiency(self):
        return self._proficiency

class Camera:
    '''Functionalities of the camera class:
    - to take a picture and save it in a cache
    - to open/view an image
    
    Attributes:
        _camera: allows access to camera
        _new_image_path (string): name of new image file
    '''
    def __init__(self):
        try: 
            self._camera = cv2.VideoCapture(0)
        except: 
            print("Error! Camera cannot be opened")
        self._new_image_path = None

    def take_image(self):
        # captures image from camera and assigns path to Camera instance
        result, image = self._camera.read()
        if result:
            img_path = "new_image.png" 
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
