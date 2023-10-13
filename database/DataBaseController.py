import sqlite3


class DataBase:
    def __init__(self):
        self.con = sqlite3.connect("DataBase.db")
        self.cur = self.con.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER UNIQUE NOT NULL,
        balance FLOAT DEFAULT -1,
        role INTEGER NOT NULL DEFAULT 0,
        auth INTEGER NOT NULL DEFAULT 0
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS menu(
        name_food TEXT NOT NULL,
        url_pic TEXT,
        cost FLOAT NOT NULL,
        amount INTEGER NOT NULL
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS reviews(
        user_id INTEGER NOT NULL,
        feedback TEXT NOT NULL
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS couriers(
        id INTEGER PRIMARY KEY UNIQUE,
        courier_id INTEGER NOT NULL,
        to_whom_id INTEGER NOT NULL,
        name_of_to_whom TEXT NOT NULL,
        name_food TEXT NOT NULL,
        office TEXT NOT NULL,
        code_word TEXT NOT NULL
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS archive_deliveries(
        courier_id INTEGER NOT NULL,
        to_whom_id INTEGER NOT NULL,
        name_of_to_whom TEXT NOT NULL,
        name_food TEXT NOT NULL
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY,
        to_whom_id INTEGER NOT NULL,
        composition TEXT NOT NULL
        )""")

        self.con.commit()

    def get_delivers_from_user(self, courier_id):  # функция для получения id пользователей кому должен доставить user
        result = self.cur.execute("""SELECT * FROM couriers WHERE courier_id = ?""", (courier_id,)).fetchall()

        delivers = list()
        for i in range(len(result)):
            column_names = [description[0] for description in self.cur.description]
            delivers.append(dict(zip(column_names, result[i])))
        return delivers

    def set_courier(self, courier_id, to_whom_id, name_of_to_whom, name_food, office, code_word):
        self.cur.execute(
            """INSERT INTO couriers(courier_id, to_whom_id, name_of_to_whom, name_food, office, code_word) """ +
            """VALUES(?, ?, ?, ?, ?, ?)""",
            (courier_id, to_whom_id, name_of_to_whom, name_food, office, code_word))
        self.con.commit()

    def remove_order_in_couriers(self, _id):
        self.cur.execute("""INSERT INTO archive_deliveries VALUES(?, ?, ?, ?)""", tuple(self.cur.execute(
            """SELECT courier_id, to_whom_id, name_of_to_whom, name_food FROM couriers WHERE id = ?""",
            (_id,)).fetchone()))
        self.cur.execute("""DELETE FROM couriers WHERE id = ?""", (_id,))
        self.con.commit()

    def get_code_word_courier(self, _id):
        word = self.cur.execute("""SELECT code_word FROM couriers WHERE id = ?""", (_id,)).fetchone()

        return word[0]

    def set_user(self, user_id, balance=-1, role=0, auth=0):
        self.cur.execute("""INSERT INTO users VALUES(?, ?, ?, ?)""", (user_id, balance, role, auth))
        self.con.commit()

    def get_user(self, user_id):
        return self.cur.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,)).fetchone()

    def set_food(self, name_food, url_pic, cost, amount):
        self.cur.execute("""INSERT INTO menu VALUES(?, ?, ?, ?)""", (name_food, url_pic, cost, amount))
        self.con.commit()

    def get_all_couriers(self):
        return [i[0] for i in self.cur.execute("""SELECT user_id FROM users WHERE role=2""").fetchall()]

    def get_order(self, order_id):
        return self.cur.execute("""SELECT to_whom_id, composition FROM orders WHERE id = ?""", (order_id,)).fetchone()

    def set_order(self, to_whom_id, composition):
        self.cur.execute("""INSERT INTO orders(to_whom_id, composition) VALUES(?, ?)""", (to_whom_id, composition))
        self.con.commit()

    def del_order(self, order_id):
        self.cur.execute("""DELETE FROM orders WHERE id = ?""", (order_id,))
        self.con.commit()

    def get_all_orders(self):
        return [i[0] for i in self.cur.execute("""SELECT id FROM orders""").fetchall()]

    def set_feedback(self, user_id, feedback):
        self.cur.execute("""INSERT INTO reviews VALUES(?, ?)""", (user_id, feedback))
        self.con.commit()
