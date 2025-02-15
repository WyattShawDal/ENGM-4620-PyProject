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