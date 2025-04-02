'''File name: user_database.py
Contributers: Zoe Takacs and Wyatt Shaw
Info: Database and PickleDatabase class definition
'''
import json
import pickle
from pathlib import Path
import logging

db_logger = logging.getLogger("Database")
db_logger.setLevel(level = logging.INFO)
"""
DB Structure

Users {
    "User1": {
        proficency: "beginner" string
        letter_scores: [] #array of len(alphabet)
    }
}

"""
class Database:
    def __init__(self, db_name: str = "data"):
        #Name of database
        self.db_name = db_name
        #Runtime store of data
        self.db_data = {}
    
    def db_create(self) -> dict:
        #create empty user dict 
        db_logger.info(f"Creating DB = {self.db_name}")
        return self.db_data
    
    def load_db(self) -> dict:
        #if a path exists to the database
        db_logger.info(f"Loading DB = {self.db_name}")
        if Path(self.db_name).exists():
            #return the dictionary from the JSON
            with open(self.db_name, "r") as db:
                return json.load(db)
        else:
            return self.db_create()

    def save_db(self, data) -> None:
        db_logger.info(f"Saving DB = {self.db_name}")
        if not self.db_data:
            db_logger.error("Saving Empty Database!")
        with open(self.db_name, "w") as db:
            #save the dictionary as a JSON
            json.dump(data, db, indent=4)

# New PickleDatabase class inheriting from Database
class PickleDatabase(Database):
    def __init__(self, db_name: str = "data"):
        # Add .pkl extension if not already present
        self.db_name = f"{db_name}.pkl" if not db_name.endswith(".pkl") else db_name
        self.db_data = {}

    # No need to override db_create as it doesn't deal with serialization

    def load_db(self) -> dict:
        # If a path exists to the database
        db_logger.info(f"Loading DB = {self.db_name}")
        if Path(self.db_name).exists():
            # Return the dictionary from the pickle file
            with open(self.db_name, "rb") as db:  # Changed to 'rb' for binary reading
                return pickle.load(db)
        else:
            return self.db_create()
        
    def save_db(self, data) -> None:
        db_logger.info(f"Saving DB = {self.db_name}")
        if not data:
            db_logger.error("Saving Empty Database!")
        with open(self.db_name, "wb") as db:  # Changed to 'wb' for binary writing
            # Save the dictionary using pickle
            pickle.dump(data, db) 


if __name__ == "__main__":
    print("Database Testing")
    our_users = Database("our_user_db")
    data = our_users.load_db()
    print(data)