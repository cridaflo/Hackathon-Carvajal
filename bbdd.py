import mysql.connector

mydb = mysql.connector.connect(
    host="35.226.15.108",
    user="root",
    passwd="1234",
    database="logs"
)

my_cursor = mydb.cursor()


def login(usr, pwd):
    my_cursor.execute("SELECT * FROM credenciales")
    result = my_cursor.fetchall()

    for x in result:
        if(x["email"]==usr and x["pwd"]):
            return True
    
    return False