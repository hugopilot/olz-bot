import config
import sqlite3
from sqlite3 import Error
from models import rank
def connect(file = config.databaseloc):
    try:
        conn = sqlite3.connect(file)
        return conn
    except Error:
        return -1

def close_con(con):
    con.close()

def updaterecord(id:int, role:rank.Rank):
    # First, create a connection with the db
    c = connect()
    cu = c.cursor()

    # Check for user
    q = "SELECT * FROM pupils WHERE id = {}".format(id)
    cu.execute(q)
    r = cu.fetchall()
    cu.close()
    cu = c.cursor()
    # If record doesn't yet exist, create one
    if(len(r) < 1):
        q = "INSERT INTO pupils (id, rank) VALUES('{}', '{}')".format(id, str(role))
        cu.execute(q)
        c.commit()
    # Else, just update it
    else:
        print(str(rank))
        q = "UPDATE pupils SET rank = '{}' WHERE id = '{}'".format(str(role), id)
        cu.execute(q)
        c.commit()

    # Finally, close the connection and exit
    close_con(c)

def getuser(id:int):
    # First, create a connection with the db
    c = connect()
    cu = c.cursor()

    # Check for user
    q = "SELECT * FROM pupils WHERE id = {}".format(id)
    cu.execute(q)
    r = cu.fetchall()

    # Close the connection
    close_con(c)
    # Return the result
    if(len(r) < 1):
        return False
    else:
        return r

    

