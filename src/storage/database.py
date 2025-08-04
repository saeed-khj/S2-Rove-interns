import sqlite3

class Database:
    def __init__(self, db_url):
        self.db_path = db_url.replace("sqlite:///", "")
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origin TEXT,
                destination TEXT,
                date TEXT,
                price REAL,
                airline TEXT,
                departure_time TEXT
            )
        """)
        self.conn.commit()

    def save_data(self, records):
        cursor = self.conn.cursor()
        for record in records:
            print(f"Saving record: {record}")  # Print each record before saving
            cursor.execute("""
                INSERT INTO flights (origin, destination, date, price, airline, departure_time)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                record["origin"],
                record["destination"],
                record["date"],
                record["price"],
                record["airline"],
                record["departure_time"]
            ))
        self.conn.commit()
        print(f"Committed {len(records)} records to the database.")  # Print after commit

    def retrieve_data(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()