import sqlite3


class Sql:
    def __init__(self, author_id, conn):
        self.author = author_id
        self.conn = conn
        self.new = self.check_user()

    def check_user(self):
        cursor = self.conn.cursor()
        user = cursor.execute('SELECT * FROM users WHERE id = ?', (int(self.author), )).fetchone()
        if user is None:
            print('Lol')
            return True
        else:
            print('LOL')
            return False