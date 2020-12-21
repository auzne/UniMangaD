import _sqlite3

# execute("INSERT INTO sources (name, home_link, search_link, manga_link, chap_link, img_link) VALUES ('1','2','3','4','5','6);")
# returns str or bool -> False if goes wrong, otherwise returns bool -> True

# read("SELECT * FROM sources;")
# returns str if goes wrong, otherwise returns empty or filled list

# readOne(f"SELECT * FROM bookmarks;")
# returns str if goes wrong, otherwise returns NoneType -> None when empty or Tuple if filled

class Database:
    def __init__(self):
        self.connection = _sqlite3.connect("./utils/database.db")
        self.cursor = self.connection.cursor()
        self.createTables()

    def read(self, query: str):
        try:
            self.cursor.execute(query)
            query_result = self.cursor.fetchall()
            return query_result
        except Exception as e:
            return f"[ERR] (read:conn.py) {e}"

    def readOne(self, query: str):
        try:
            self.cursor.execute(query)
            query_result = self.cursor.fetchone()
            return query_result
        except Exception as e:
            return f"[ERR] (readOne:conn.py) {e}"

    def execute(self, query: str, returnError: bool = False):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            if returnError:
                return f"[ERR] (execute:conn.py): {e}"
            return False

    def createTables(self):
        self.execute("""CREATE TABLE IF NOT EXISTS sources (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL,
            home_link       TEXT NOT NULL,
            search_link     TEXT NOT NULL,
            manga_link      TEXT NOT NULL,
            chap_link       TEXT NOT NULL,
            img_link        TEXT NOT NULL
        );""")
        self.execute("""CREATE TABLE IF NOT EXISTS downloads (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            fk_id           INTEGER,
            manga_name      TEXT NOT NULL,
            total_caps      INTEGER DEFAULT 0,
            last_down       INTEGER DEFAULT 0,
            FOREIGN KEY (fk_id) REFERENCES sources (id)
        );""")
        self.execute("""CREATE TABLE IF NOT EXISTS bookmarks (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            fk_id           INTEGER,
            manga_name      TEXT NOT NULL,
            manga_link      TEXT NOT NULL,
            FOREIGN KEY (fk_id) REFERENCES sources (id)
        );""")
