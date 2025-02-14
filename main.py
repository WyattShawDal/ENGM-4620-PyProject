from classes import Model, User, Camera

if __name__ == '__main__':
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