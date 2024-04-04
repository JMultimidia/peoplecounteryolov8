# db.py
import mysql.connector
import os
from dotenv import load_dotenv

# Carregue as variáveis de ambiente
load_dotenv()

def create_database_instance():
    db_host = os.getenv("DB_HOST", "localhost")
    db_database = os.getenv("DB_NAME", "video_analytics")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "root")

    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_database
        )
        print("Conexão bem-sucedida!")
        return Database(connection)
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

class Database:
    def __init__(self, connection):
        self.connection = connection

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
