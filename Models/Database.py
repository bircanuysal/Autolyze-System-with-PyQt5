import sqlite3
from models.UserModel import UserModel
from models.AracModel import AracModel

class Database:
    def __init__(self, db_name="arac_kayit.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        self.insert_default_models()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Kullanıcı tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE
            )
        """)

        # Araç tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                ilan_no INTEGER,
                brand TEXT,
                model TEXT,
                km INTEGER,
                year INTEGER,
                painted_count INTEGER,
                changed_count INTEGER,
                score INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")


        # Marka – Model tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS brand_models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT,
                model TEXT
            )
        """)

        self.conn.commit()

    def insert_default_models(self):
        cursor = self.conn.cursor()

        # Eğer tablo boşsa içerik ekle
        cursor.execute("SELECT COUNT(*) FROM brand_models")
        if cursor.fetchone()[0] > 0:
            return  # zaten ekli

        marka_modeller = {
            "Audi": ["A3", "A4", "A5", "A6", "Q3", "Q5", "Q7"],
            "Bmw": ["1 Serisi", "2 Serisi", "3 Serisi", "4 Serisi", "5 Serisi", "X Serisi", "M Serisi"],
            "Mercedes Benz": ["A Serisi", "B Serisi", "C Serisi", "E Serisi", "S Serisi", "AMG"],
            "Volkswagen": ["Golf", "Polo", "Passat", "Tiguan", "Arteon"]
        }

        for brand, models in marka_modeller.items():
            for m in models:
                cursor.execute("INSERT INTO brand_models (brand, model) VALUES (?, ?)", (brand, m))

        self.conn.commit()

    # -------------------------
    # USER FONKSIYONLARI
    # -------------------------

    def get_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        
        if row:
            return UserModel(id=row[0], username=row[1])
        return None

    def add_user(self, user: UserModel):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (username) VALUES (?)", (user.username,))
        self.conn.commit()
        user.id = cursor.lastrowid
        return user

    # -------------------------
    # MARKA – MODEL
    # -------------------------

    def get_models_by_brand(self, brand):
        cursor = self.conn.cursor()
        cursor.execute("SELECT model FROM brand_models WHERE brand = ?", (brand,))
        results = cursor.fetchall()
        return [r[0] for r in results]

    # -------------------------
    # ARAÇ FONKSIYONLARI
    # -------------------------

    def add_car(self, car: AracModel):
        cursor = self.conn.cursor()
        cursor.execute("""
    INSERT INTO cars (user_id, ilan_no, brand, model, km, year, painted_count, changed_count, score)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (car.user_id, car.carNo, car.brand, car.model, car.km, car.year,
      car.painted_count, car.changed_count, car.score))

        self.conn.commit()
        return cursor.lastrowid

    def get_cars_by_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cars WHERE user_id = ?", (user_id,))
        results = cursor.fetchall()

        cars = []
        for row in results:
            cars.append(AracModel(
                id=row[0],
                user_id=row[1],
                carNo=row[2],
                brand=row[3],
                model=row[4],
                km=row[5],
                year=row[6],
                painted_count=row[7],
                changed_count=row[8],
                score=row[9]
            ))
        return cars
