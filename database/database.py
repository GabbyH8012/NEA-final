import sqlite3
from unittest import result

db_name = "database/swimmer_info.db"


def createTables():
    conn = sqlite3.connect(db_name)
    #connects to sqlite3 database and creates the database if it doesn't exist

    cursor = conn.cursor()
    #controls structure via cursor

    cursor.execute("""
        CREATE TABLE user (
            rankings_ID INTEGER NOT NULL UNIQUE PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            CHECK (length(rankings_ID) < 11 AND length(rankings_ID) > 3),    
            CHECK (password GLOB '*[0-9]*' AND password GLOB '*[A-Z]*' AND password GLOB '*[a-z]*')
                );
        """)


    cursor.execute("""
        CREATE TABLE race (
            race_ID INTEGER NOT NULL UNIQUE PRIMARY KEY,
            distance INTEGER NOT NULL,
            stroke TEXT NOT NULL,
            course TEXT NOT NULL,
            CHECK (race_ID < 36 AND race_ID > 0)
                );
        """)


    cursor.execute("""
        CREATE TABLE competition (
            comp_name TEXT NOT NULL UNIQUE PRIMARY KEY,
            venue TEXT               
                );
        """)


    cursor.execute("""
        CREATE TABLE goal (
            rankings_ID INTEGER NOT NULL,
            race_ID INTEGER NOT NULL,
            goal_time TIME,
            PRIMARY KEY (rankings_ID , race_ID),
            FOREIGN KEY (rankings_ID) REFERENCES user(rankings_ID),
            FOREIGN KEY (race_ID) REFERENCES race(race_ID)
                    );
        """)


    cursor.execute("""
        CREATE TABLE meet(
            comp_name TEXT NOT NULL,
            date DATE NOT NULL,
            target BOOL,
            PRIMARY KEY (comp_name , date),
            FOREIGN KEY (comp_name) REFERENCES competition(comp_name)
                );       
        """)


    cursor.execute("""
        CREATE TABLE result(
            rankings_ID INTEGER NOT NULL,
            race_ID INTEGER NOT NULL,
            comp_name TEXT NOT NULL,
            date DATE NOT NULL,
            final_time TIME,
            goal_time TIME,
            PRIMARY KEY (rankings_ID , race_ID , comp_name , date),
            FOREIGN KEY (rankings_ID) REFERENCES user(rankings_ID),
            FOREIGN KEY (race_ID) REFERENCES race(race_ID),
            FOREIGN KEY (comp_name) REFERENCES competition(comp_name),
            FOREIGN KEY (date) REFERENCES meet(date)
                );
        """)



# Database access function to check if there is already a swimmer with the same rankings_ID or email
# -----------------------------------------------------------------------------------
def check_existing_swimmer(rankings_ID: int , email: str) -> bool:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * 
                        FROM user 
                        WHERE rankings_ID = ? """ , (str(rankings_ID),))
        result = cursor.fetchone()

        cursor.execute("""SELECT * 
                        FROM user 
                        WHERE email = ? """ , (email,))
        result2 = cursor.fetchone()

        if result == None and result2 == None:
            return False
        else:
            return True



# Database access function to add a new swimmer to the database with the imputted details
# ---------------------------------------------------------------------------------------
def add_new_swimmer(rankings_ID: int, name: str, email: str, password: str) -> bool:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user (rankings_ID, email, password, name) VALUES (?, ?, ?, ?)", (str(rankings_ID), email, password, name))
        conn.commit()
        return True
    


# Database access function to check if login credentials are correct
# ------------------------------------------------------------------
def check_login_credentials(rankings_ID: int, password: str) -> bool:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT password 
                        FROM user 
                        WHERE rankings_ID = ? """ , (str(rankings_ID),))
        result = cursor.fetchone()

        if result == None:
            return False
        elif result[0] == password:
            return True
        else:
            return False
    


# Database access function to return current user's and name and email address
# ----------------------------------------------------------------------------
def get_user_info(rankings_ID: int):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT name, email 
                        FROM user 
                        WHERE rankings_ID = ? """ , (str(rankings_ID),))
        result = cursor.fetchone()

        return result
    


# Database access function to delete an account from the database
# ---------------------------------------------------------------
def delete_account(rankings_ID: int):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM user 
                        WHERE rankings_ID = ? """ , (str(rankings_ID),))
        return True
    


# Database access function to populate the race table
# ---------------------------------------------------
def populate_race_table():

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        race_list = [
            ("1", 50, "Freestyle", "Short"),
            ("2", 100, "Freestyle", "Short"),
            ("3", 200, "Freestyle", "Short"),
            ("4", 400, "Freestyle", "Short"),
            ("5", 800, "Freestyle", "Short"),
            ("6", 1500, "Freestyle", "Short"),
            ("7", 50, "Breaststroke", "Short"),
            ("8", 100, "Breaststroke", "Short"),
            ("9", 200, "Breaststroke", "Short"),
            ("10", 50, "Butterfly", "Short"),
            ("11", 100, "Butterfly", "Short"),
            ("12", 200, "Butterfly", "Short"),
            ("13", 50, "Backstroke", "Short"),
            ("14", 100, "Backstroke", "Short"),
            ("15", 200, "Backstroke", "Short"),
            ("16", 200, "Individual Medley", "Short"),
            ("17", 400, "Individual Medley", "Short"),
            ("18", 100, "Individual Medley", "Short"),

            ("19", 50, "Freestyle", "Long"),
            ("20", 100, "Freestyle", "Long"),
            ("21", 200, "Freestyle", "Long"),
            ("22", 400, "Freestyle", "Long"),
            ("23", 800, "Freestyle", "Long"),
            ("24", 1500, "Freestyle", "Long"),
            ("25", 50, "Breaststroke", "Long"),
            ("26", 100, "Breaststroke", "Long"),
            ("27", 200, "Breaststroke", "Long"),
            ("28", 50, "Butterfly", "Long"),
            ("29", 100, "Butterfly", "Long"),
            ("30", 200, "Butterfly", "Long"),
            ("31", 50, "Backstroke", "Long"),
            ("32", 100, "Backstroke", "Long"),
            ("33", 200, "Backstroke", "Long"),
            ("34", 200, "Individual Medley", "Long"),
            ("35", 400, "Individual Medley", "Long")
        ]


        cursor.executemany("INSERT INTO race (race_ID, distance, stroke, course) VALUES (?, ?, ?, ?)", race_list)

    return True



# Database access function to find the name of a race given the race_ID
# ---------------------------------------------------------------------
def find_race_from_ID(race_ID: int):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT distance, stroke
                        FROM race
                        WHERE race_ID = ? """ , (str(race_ID),))
        result = cursor.fetchone()
        result = str(result[0]) + " " + str(result[1])
        return result
    


# Database access function to enter extracted data into the database
# ------------------------------------------------------------------
def push_extracted_data(rankings_ID: int, race_ID: int, comp_name: str, date: str, final_time: str, venue: str):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        
        print(comp_name, "+" , venue)
        cursor.execute("INSERT INTO competition (comp_name, venue) VALUES (?, ?)", (comp_name, venue))
        cursor.execute("INSERT INTO meet (comp_name, date) VALUES (?, ?)", (comp_name, date))
        cursor.execute("INSERT INTO result (rankings_ID, race_ID, comp_name, date, final_time) VALUES (?, ?, ?, ?, ?)", (rankings_ID, race_ID, comp_name, date, final_time))


    return True


# createTables()
# populate_race_table()