from fastai.vision.all import *
import cv2

# proficiency levels in points
MIN_LEVEL = 35.0
MED_LEVEL = 60.0
MAX_LEVEL = 85.0

class Model:
    """Functionalities of the Model class: 
        - load the model 
        - make predictions on single images

    Attributes: 
        model_fpath (string): hold the relative local path to the model.pkl file
    """
    def __init__(self, model_fpath):
        try:
            self._loaded_model = load_learner(Path('.')/model_fpath)
        except:
            print("Error! Model could not be loaded.")
    
    def make_prediction(self, img_path):
        """Makes prediction on letter is represented in the image provided.

        Args: 
            img_path (string): hold the relative local path to the image to be processed

        Returns:
            predicted_letter (string): upper letter identified in the image
            probability (list of ints): index corresponds to letter in the alphabet; value represents confidence on scale of 0.0 to 1.0
        """
        try:
            img = PILImage.create(img_path)
            img = img.resize((192, 192))
            predicted_letter, _, probability = self._loaded_model.predict(img)
            return predicted_letter, probability
        except:
            print("Error! Cannot open image.")

class User:
    """Functionalities for the User class: 
        - create/edit/view a profile
        - keep track of their scores on various trials
        - display their progress over time

    NOTE: could have different levels of user which have access to different prompt sets or types of services;
    this could allow us to implement inheritance

    Attributes: 
        _name (string): username
        _proficiency (string): quantized level user is on
        _score (int): number of points user has accumulated
    """
    def __init__(self, name, proficiency):
        self._name = name
        self._proficiency = proficiency
        self._score_history = [[] for x in range(26)]
        self._w_let_scores = [None for x in range(26)]
        self._p_let_scores = [None for x in range(26)]
        self._overall_score = 0.0

    def display_profile(self): # eventually make an Application class that can display and edit profile info
        """Return the content of a users profile
        """
        return ("User: ", self._name, "\nProficiency: ", self._proficiency)

    def update_profile(self): # eventually not needed
        """For terminal use: to enter a new username
        """
        new_name = input("Enter new profile name or * to cancel: ")
        setattr(self, '_name', new_name) and (result:= (f"New name: {self._name}")) if new_name != '*' else (result:= ("Cancelled."))
        return result
    
    def check_score(self):
        """Retireve user's current score
        """
        return self._score

    def update_proficiency(self):
        """Update the users proficiency level to match their score
        """
        if self._overall_score < MIN_LEVEL:
            self._proficiency = "Beginner"
        elif self._overall_score < MED_LEVEL:
            self._proficiency = "Intermediate"
        elif self._overall_score < MAX_LEVEL:
            self._proficiency = "Advanced"
        else:
            self._proficiency = "Signed Language Sensei"
    
    def check_proficiency(self):
        """Retrieve the proficiency of the user
        """
        return self._proficiency

class Camera:
    """Functionalities of the camera class:
    - to take a picture and save it in a cache
    - to open/view an image
    
    Attributes:
        _camera (cam): creates access to camera
        _new_image_path (string): name of new image file
    """
    def __init__(self):
        try: 
            self._camera = cv2.VideoCapture(0)
        except: 
            print("Error! Camera cannot be opened")
        self._new_image_path = None

    def take_image(self):
        """Captures image from camera and assigns path to Camera instance
        """
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
        """Displays specified image in a new window
        """
        image = cv2.imread(img_path if img_path != None else self._new_image_path)
        cv2.imshow("Image Window", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
