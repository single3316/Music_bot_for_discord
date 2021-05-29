import sqlite3


class Sql:
    def __init__(self, author_id, conn, name):
        self.author_name = name
        self.author = author_id
        self.conn = conn
        self.new = self.check_user()
        if self.new:
            self.add_user()

    def check_user(self):
        cursor = self.conn.cursor()
        user = cursor.execute('SELECT * FROM users WHERE id = ?', (int(self.author),)).fetchone()
        if user is None:
            return True
        else:
            return False

    def add_user(self):
        user = [int(self.author), self.author_name, 0, 0]
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO users(id, name, score, level) VALUES(?, ?, ?, ?)', user)
        self.conn.commit()

    def add_point(self, point):
        cursor = self.conn.cursor()
        score = cursor.execute('SELECT score FROM users WHERE id = ?', (int(self.author),)).fetchone()[0]
        level = cursor.execute('SELECT level FROM users WHERE id = ?', (int(self.author),)).fetchone()[0]
        score += point
        if score >= 1000:
            level += 1
            cursor.execute('UPDATE users SET score = 0, level = ? where id = ?', (level, int(self.author),))
        else:
            cursor.execute('UPDATE users SET score = ? where id = ?', (score, int(self.author),))
        self.conn.commit()

    def get_name(self):
        cursor = self.conn.cursor()
        user = cursor.execute('SELECT name FROM users WHERE id = ?', (int(self.author),)).fetchone()[0]
        return user

    def get_score(self):
        cursor = self.conn.cursor()
        user = cursor.execute('SELECT score FROM users WHERE id = ?', (int(self.author),)).fetchone()[0]
        return user

    def get_level(self):
        cursor = self.conn.cursor()
        user = cursor.execute('SELECT level FROM users WHERE id = ?', (int(self.author),)).fetchone()[0]
        return user

    def get_rank(self):
        cursor = self.conn.cursor()
        user_list = cursor.execute('SELECT name FROM users ORDER BY level DESC').fetchall()
        rank = 1
        for i in user_list:
            if self.author_name == i[0]:
                return rank
            rank += 1
        return None

    def get_ten_users(self):
        user_list = []
        cursor = self.conn.cursor()
        users = cursor.execute('SELECT name, id FROM users ORDER BY level DESC').fetchall()
        h = 1
        for i in users:
            user_list.append([i[0], i[1], h])
            if h == 6:
                return user_list
            h += 1


