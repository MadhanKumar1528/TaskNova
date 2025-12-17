from db import Database

class Auth:
    def __init__(self):
        self.db = Database()

    def login(self, username, password):
        query = """
        SELECT id FROM users
        WHERE username=%s AND password=%s
        """
        result = self.db.fetch(query, (username, password))
        return result[0][0] if result else None

    def signup(self, username, password):
        try:
            query = """
            INSERT INTO users (username, password)
            VALUES (%s, %s)
            """
            self.db.execute(query, (username, password))
            return True
        except:
            return False
