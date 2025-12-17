import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your password",
            database="your database"
        )
        self.cursor = self.conn.cursor()

    def execute(self, query, values=None):
        self.cursor.execute(query, values or ())
        self.conn.commit()

    def fetch(self, query, values=None):
        self.cursor.execute(query, values or ())
        return self.cursor.fetchall()
