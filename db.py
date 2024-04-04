# db.py
import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="counter"
        )

    def insert_entering(self, id_people):
        cursor = self.connection.cursor()
        query = "INSERT INTO people_entering (id_people) VALUES (%s)"
        cursor.execute(query, (id_people,))
        self.connection.commit()
        cursor.close()

    def insert_exiting(self, id_people):
        cursor = self.connection.cursor()
        query = "INSERT INTO people_exiting (id_people) VALUES (%s)"
        cursor.execute(query, (id_people,))
        self.connection.commit()
        cursor.close()

    def close(self):
        self.connection.close()
