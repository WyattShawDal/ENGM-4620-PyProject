'''File name: main.py
Contributers: Zoe Takacs and Wyatt Shaw
Info: Used to test different base classes
Note: NOT used to run application
'''
import os
from base_classes import Model, User, Camera

if __name__ == '__main__':
    if os.getenv("TEST_MODE") == "1":
        # test user class methods
        print("USER TEST MODE:")
        name, proficiency = input("Enter a name and proficiency level: ").split()
        user1 = User(name, proficiency)
        user1.display_profile()
        user1.update_profile()
        user1.display_profile()
        user1.update_score(35)
        print("score: ", user1.check_score())
        user1.update_proficiency()
        print("proficiency: ", user1.check_proficiency())
        user1.display_profile()
    elif os.getenv("TEST_MODE") == "2":
        # test camera class methods
        print("CAMERA TEST MODE:")
        camera = Camera()
        camera.take_image()
        camera.view_image()
    else:
        print("NO TEST VARIABLE FOUND IN ENVIRONMENT")