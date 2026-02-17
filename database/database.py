import sqlite3

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
            CHECK (length(rankings_ID) < 11 AND length(rankings_ID) > 3)
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
            entry_time TIME,
            final_time TIME,
            PRIMARY KEY (rankings_ID , race_ID , comp_name , date),
            FOREIGN KEY (rankings_ID) REFERENCES user(rankings_ID),
            FOREIGN KEY (race_ID) REFERENCES race(race_ID),
            FOREIGN KEY (comp_name) REFERENCES competition(comp_name),
            FOREIGN KEY (date) REFERENCES meet(date)
                );
        """)



# Database access function to check if there is already a swimmer with the same SE_ID
# -----------------------------------------------------------------------------------
def check_existing_swimmer(SE_ID: int) -> bool:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * 
                        FROM user 
                        WHERE rankings_ID = ? """ , (str(SE_ID),))
        result = cursor.fetchone()

        if result == None:
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
    

