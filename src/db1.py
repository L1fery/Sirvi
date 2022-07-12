import sqlite3

rank = 3
rank_name = 'новокек'
chat_id = 0
rep = 0


class DB:
    def __init__(self):
        self.connect = sqlite3.connect('db.db', check_same_thread=False)
        self.cursor = self.connect.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY, 
                username TEXT, 
                first_name TEXT, 
                last_name TEXT,
                rank INTEGER,
                rank_name TEXT,
                chat_id INTEGER,
                rep INTEGER
            ) """)
        self.connect.commit()

        user = self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
        def add_user(self, user_id, username, first_name, last_name, rank, rank_name, chat_id, rep):
            if not user:
                self.cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?,?)",
                                    (user_id, username, first_name, last_name, rank, rank_name, chat_id, rep))
                self.connect.commit()
            else:
                return

    def update_rank(self, user_id, rank):
        self.cursor.execute("UPDATE users SET rank = ? WHERE user_id = ?", (rank, user_id))
        self.connect.commit()
        self.cursor.execute("UPDATE users SET rank_name = ? WHERE user_id = ?", (rank_name, user_id))
        self.connect.commit()

    def get_top(self):
        users = self.cursor.execute(
            "SELECT rank, username, user_id, rank_name, first_name FROM users ORDER BY rank DESC LIMIT 10").fetchall()
        return '\n'.join(' | '.join([str(i[0]), f'<a href="tg://user?id={str(i[2])}">{i[4]}</a>']) for i in users)

    def get_rank(self, user_id):
        user1 = self.cursor.execute('SELECT rank, username, user_id, rank_name FROM users WHERE user_id = ?',
                                    (user_id,)).fetchone()
        return ' | '.join([str(user1[0]), str(user1[1]), str(user1[2]), str(user1[3])])

    def get_rank1(self, user_id):
        user1 = self.cursor.execute('SELECT rank, rank_name FROM users WHERE user_id = ?',
                                    (user_id,)).fetchone()
        return ' | '.join([str(user1[0]), str(user1[1])])

    def add_rep(self, rep, user_id):
        self.cursor.execute("UPDATE users SET rep = ? WHERE user_id = ?", (rep, user_id))
        self.connect.commit()

    def global_rep(self):
        users = self.cursor.execute(
            "SELECT rep, username, user_id, rank_name, first_name FROM users ORDER BY rep DESC LIMIT 10").fetchall()
        return '\n'.join(' | '.join([str(i[0]), f'<a href="tg://user?id={str(i[2])}">{i[4]}</a>']) for i in users)

    def get_rep(self, user_id):
        gg_rep = self.cursor.execute('SELECT rep FROM users WHERE user_id = ?',
                                     (user_id,)).fetchone()
        return ' | '.join([str(gg_rep[0])])
