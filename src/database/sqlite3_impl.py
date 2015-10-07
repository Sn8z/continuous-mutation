import sqlite3

"""
tabeler
id, felmedelande
id, typ av fel
id, filnamn
fel_id, typ_id, fil_id
"""

db = sqlite3.connect(":memory:")

def createDB():
    cursor = db.cursor()

    cursor.execute('''CREATE TABLE error_msg(
    id INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 0, msg TEXT UNIQUE )''')


    cursor.execute('''CREATE TABLE error_type(
    id INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 0, type TEXT UNIQUE )''')


    cursor.execute('''CREATE TABLE filename(
    id INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 0, name TEXT UNIQUE)''')


    cursor.execute('''CREATE TABLE errors(
    msg_id INT, type_id INT, file_id,
    FOREIGN KEY (msg_id) REFERENCES error_msg(id), 
    FOREIGN KEY (type_id) REFERENCES error_type(id), 
    FOREIGN KEY (file_id) REFERENCES filename(id)
    )''')


    db.commit()

    #db.close()


def insert(error_msg, error_type, filename):
    
    cursor = db.cursor()

    cursor.execute("INSERT OR IGNORE INTO error_msg  (msg) VALUES (?)", (error_msg, ))
    msg_id = cursor.lastrowid;

    cursor.execute("INSERT OR IGNORE INTO error_type (type) VALUES (?)", (error_type, ))
    type_id = cursor.lastrowid;
    
    cursor.execute("INSERT OR IGNORE INTO filename (name) VALUES (?)", (filename,))
    file_id = cursor.lastrowid;

    cursor.execute("INSERT OR IGNORE INTO errors VALUES(?,?,?)", (msg_id, type_id, file_id))

    db.commit()
    #db.close()


def find(_error_msg):
    """
    find error type by error msg. Returns list with all related error types
    [{error_msg},{error_type}]
    """
    cursor = db.cursor()

    cursor.execute('''SELECT error_msg.msg, error_type.type FROM errors
    LEFT JOIN error_msg
    ON error_msg.id = errors.msg_id
    LEFT JOIN error_type
    ON error_type.id = errors.type_id
    WHERE error_msg.msg = (?)''', (_error_msg,))

    return cursor.fetchall()



def printAllTables():

    cursor = db.cursor()

    print("ERROR_MSG")
    cursor.execute("SELECT * FROM error_msg")
    for row in cursor:
        print(row)

    print("ERROR_TYPE")
    cursor.execute("SELECT * FROM error_type")
    for row in cursor:
        print(row)

    print("FILENAME")
    cursor.execute("SELECT * FROM filename")
    for row in cursor:
        print(row)


    print("ERRORS")
    cursor.execute("SELECT * FROM errors")
    for row in cursor:
        print(row)

        


      
    