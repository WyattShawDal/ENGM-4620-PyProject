# ENGM-4620-PyProject
*Authors: Zoe Takacs & Wyatt Shaw*

A repository holding the contents of the Major Python Project

Computer Vision Sign Language practice tool

## Build Instructions:

1. Clone the repostory
2. Launch a [Virtual Environment](https://docs.python.org/3/library/venv.html)
3. **from within venv**: `pip install -r requirements.txt`
4. Run: `py main.py` (for now)

## How to develop PyQt5 Designer Code

1. Ensure requirements.txt has been installed
2. Open designer by calling **from within project folder**: `designer`
3. Develop GUI and save as .ui file to project folder
4. Convert to a python file: `python -m PyQt5.uic.pyuic -x filename.ui -o output_filename.py`

## Current TODO List

1. Implement load_user_database() in controller_classes.py
2. Implement save_profile() in base_classes.py
3. Add button to Lesson1 class that allows user to retake picture before submitting it
4. Create new screen class to view and edit profile data using the user_controller() and add class as a StackedWidget to MainWindow class
5. Add check for when access to camera is blocked
6. Add login option, once user storing/loading has be implemented
7. Verify there is proper Error catching implemented everywhere