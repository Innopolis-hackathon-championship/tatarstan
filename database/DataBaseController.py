import sqlite3


class DataBase:
    def __init__(self):
        self.con = sqlite3.connect("./database/DataBase.db")
        self.cur = self.con.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER UNIQUE NOT NULL,
        balance FLOAT DEFAULT -1,
        role INTEGER NOT NULL DEFAULT 0,
        auth INTEGER NOT NULL DEFAULT 0
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS menu(
        name_food TEXT UNIQUE,
        amount INTEGER NOT NULL
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS couriers(
        id INTEGER PRIMARY KEY UNIQUE,
        order_id INTEGER UNIQUE NOT NULL,
        courier_id INTEGER NOT NULL,
        to_whom_id INTEGER NOT NULL,
        name_of_to_whom TEXT NOT NULL,
        office TEXT NOT NULL,
        code_word TEXT NOT NULL
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS archive_deliveries(
        courier_id INTEGER NOT NULL,
        to_whom_id INTEGER NOT NULL,
        name_of_to_whom TEXT NOT NULL
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        to_whom_id INTEGER NOT NULL,
        name_of_to_whom TEXT NOT NULL,
        composition TEXT NOT NULL,
        office TEXT NOT NULL
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS auth_keys(
        user_id INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL,
        key TEXT UNIQUE NOT NULL
        )""")

        self.con.commit()

    def update_balance(self, user_id, number):  # если number<0, то это вычитание, если number>0, то добавление баланса
        self.cur.execute("""UPDATE users SET balance = (balance + ?) WHERE user_id = ?""", (number, user_id))
        self.con.commit()

    def get_delivers_from_user(self, courier_id):  # функция для получения id пользователей кому должен доставить user
        result = self.cur.execute("""SELECT * FROM couriers WHERE courier_id = ?""", (courier_id,)).fetchall()

        delivers = list()
        for i in range(len(result)):
            column_names = [description[0] for description in self.cur.description]
            delivers.append(dict(zip(column_names, result[i])))
        return delivers

    def set_courier(self, order_id, courier_id, to_whom_id, name_of_to_whom, office, code_word):
        self.cur.execute(
            """INSERT INTO couriers(order_id, courier_id, to_whom_id, name_of_to_whom, office, code_word) """ +
            """VALUES(?, ?, ?, ?, ?, ?)""",
            (order_id, courier_id, to_whom_id, name_of_to_whom, office, code_word))
        self.con.commit()

    def remove_order_in_couriers(self, _id):
        self.cur.execute("""INSERT INTO archive_deliveries VALUES(?, ?, ?)""", tuple(self.cur.execute(
            """SELECT courier_id, to_whom_id, name_of_to_whom FROM couriers WHERE id = ?""",
            (_id,)).fetchone()))
        self.cur.execute("""DELETE FROM couriers WHERE id = ?""", (_id,))
        self.con.commit()

    def get_code_word_courier(self, _id):
        try:
            word = self.cur.execute("""SELECT code_word FROM couriers WHERE id = ?""", (_id,)).fetchone()
            return word[0]
        except:
            return ""

    def set_user(self, user_id, balance=-1, role=0, auth=0):
        self.cur.execute("""INSERT INTO users VALUES(?, ?, ?, ?)""", (user_id, balance, role, auth))
        self.con.commit()

    def get_user(self, user_id):
        result = self.cur.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,)).fetchone()
        column_names = [description[0] for description in self.cur.description]
        return dict(zip(column_names, result))

    def set_user_role(self, user_id, role):
        self.cur.execute("""UPDATE users SET role = ? WHERE user_id = ?""", (role, user_id))
        self.con.commit()

    def set_user_auth(self, user_id):
        self.cur.execute("""UPDATE users SET auth=1 WHERE user_id = ?""", (user_id,))
        self.con.commit()

    def set_food(self, name_food, amount):
        self.cur.execute("""INSERT INTO menu VALUES(?, ?)""", (name_food, amount))
        self.con.commit()

    def check_food_have(self, name):
        res = None
        try:
            res = self.cur.execute("""SELECT * FROM menu WHERE name_food = ?""", (name,)).fetchone()
        except:
            pass
        if res is None:
            return False
        else:
            return True

    def update_food(self, name_food, number):  # если number<0, то это вычитание, если number>0, то добавление еды
        self.cur.execute("""UPDATE menu SET amount = (amount + ?) WHERE name_food = ?""", (number, name_food))
        self.con.commit()

    def get_food_amount(self, name):
        amo = -1
        try:
            amo = self.cur.execute("""SELECT amount FROM menu WHERE name_food = ?""", (name,)).fetchone()[0]
        except:
            pass
        return amo

    def get_all_food(self):
        result = self.cur.execute("""SELECT * FROM menu""").fetchall()

        food_arr = list()
        column_names = [description[0] for description in self.cur.description]
        for i in range(len(result)):
            food_arr.append(dict(zip(column_names, result[i])))
        return food_arr

    def get_all_couriers(self):
        return [i[0] for i in self.cur.execute("""SELECT user_id FROM users WHERE role=2""").fetchall()]

    def get_courier_by_codeword(self, codeword):
        try:
            result = self.cur.execute("""SELECT * FROM couriers WHERE code_word = ?""", (codeword,)).fetchone()
            column_names = [description[0] for description in self.cur.description]
            return dict(zip(column_names, result))
        except:
            return dict()

    def check_courier_order_id(self, order_id):
        res = self.cur.execute("""SELECT * FROM couriers WHERE order_id = ?""", (order_id,)).fetchone()
        return res is None

    def get_all_orders(self):
        return [i[0] for i in self.cur.execute("""SELECT id FROM orders""").fetchall()]

    def get_order(self, order_id):
        result = self.cur.execute("""SELECT * FROM orders WHERE id = ?""", (order_id,)).fetchone()
        column_names = [description[0] for description in self.cur.description]

        return dict(zip(column_names, result))

    def set_order(self, to_whom_id, name_of_to_whom, composition, office):
        self.cur.execute("""INSERT INTO orders(to_whom_id, name_of_to_whom, composition, office) VALUES(?, ?, ?, ?)""",
                         (to_whom_id, name_of_to_whom, composition, office))
        self.con.commit()

    def del_order(self, order_id):
        self.cur.execute("""DELETE FROM orders WHERE id = ?""", (order_id,))
        self.con.commit()

    def check_auth_key(self, user_id, auth_key):  # auth_key - введеный пользоваталем ключ
        key = self.cur.execute("""SELECT key FROM auth_keys WHERE user_id = ?""", (user_id,)).fetchone()[0]
        return key == auth_key

    def get_info_from_auth_keys(self, user_id):
        result = self.cur.execute("""SELECT * FROM auth_keys WHERE user_id = ?""", (user_id,)).fetchone()
        column_names = [description[0] for description in self.cur.description]
        return dict(zip(column_names, result))

    def set_auth_key(self, user_id, name, key):
        self.cur.execute("""INSERT INTO auth_keys VALUES(?, ?, ?)""", (user_id, name, key))
        self.con.commit()

    def get_info_from_auth_keys(self, user_id):
        result = self.cur.execute("""SELECT * FROM auth_keys WHERE user_id = ?""", (user_id,)).fetchone()
        column_names = [description[0] for description in self.cur.description]
        return dict(zip(column_names, result))
