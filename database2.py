import sqlite3


class AuthData:
    def __init__(self):
        self.con = sqlite3.connect("DataBase.db")
        self.cur = self.con.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS auth_keys(
                user_id INTEGER UNIQUE NOT NULL,
                name TEXT NOT NULL,
                key TEXT UNIQUE NOT NULL
                )""")

        self.con.commit()

    def set_auth_key(self, user_id, name, key):
        self.cur.execute("""INSERT INTO auth_keys VALUES(?, ?, ?)""", (user_id, name, key))
        self.con.commit()

    def get_info_from_auth_keys(self, user_id):
        result = self.cur.execute("""SELECT * FROM auth_keys WHERE user_id = ?""", (user_id,)).fetchone()
        column_names = [description[0] for description in self.cur.description]
        return dict(zip(column_names, result))
