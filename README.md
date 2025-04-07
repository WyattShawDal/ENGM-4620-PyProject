# ENGM-4620-PyProject
*Authors: Zoe Takacs & Wyatt Shaw*

A repository holding the contents of the Major Python Project

Computer Vision Sign Language Personal Trainer

The Project uses a custom trained Resnet34 Model to make infer the alphabetic sign being shown in an image with the goal of providing a practice environment in which users can learn the American Sign Language (ASL) alphabet. 

## For Users:

### Build Instructions:

1. Clone the repostory
2. Launch a [Virtual Environment](https://docs.python.org/3/library/venv.html)
3. Activate Virtual Environment [Name]/Scripts/activate
4. **from within venv**: `pip install -r requirements.txt`
5. Run: `py application.py` 

### How to use the application: 
1. Create an account by entering an unused username and specifying an anticipated proficiency level OR login by entering your username. 
2. Start a lesson by clicking 'Start Lesson'
3. View score by selecting a letter under 'Check Letter Score' in Settings and clicking 'Check Score'
4. Toggle the Theme by selecting a theme under 'Mode Selection' in Settings and clicking 'Set Mode'
5. Log out by clicking 'Log Out' in the top right hand corner

## For Developers

### How to develop PyQt5 Designer Code

1. Ensure requirements.txt has been installed
2. Open designer by calling **from within project folder**: `designer`
3. Develop GUI and save as .ui file to project folder
4. Convert to a python file: `python -m PyQt5.uic.pyuic -x filename.ui -o output_filename.py`
