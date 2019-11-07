import mysql.connector

mydb = mysql.connector.connect(
    host="35.226.15.108",
    user="root",
    passwd="1234",
    database="logs"
)


def login(usr, pwd):
    my_cursor = mydb.cursor()
    my_cursor.execute("SELECT email, pwd FROM credenciales")
    result = my_cursor.fetchall()

    for x in result:
        if(x[0]==usr and x[1]==pwd):
            return True
    
    return False

def register(usr, pwd, token):
    try:

        my_cursor = mydb.cursor()
        my_cursor.execute("INSERT INTO credenciales (email, pwd, token) VALUES (%s, %s, %s)", (usr, pwd, token))

        mydb.commit()
        return True
    except:
        return False
