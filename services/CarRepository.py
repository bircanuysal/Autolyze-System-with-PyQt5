from models.Database import Database
from models.AracModel import AracModel

class CarRepository:
    def __init__(self):
        self.db = Database()

    def add_car(self, car: AracModel):
        return self.db.add_car(car)

    def car_exists(self, carNo: str, user_id: int) -> bool:
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM cars WHERE ilan_no = ? AND user_id = ?",
            (carNo, user_id)
        )
        result = cursor.fetchone()
        return result[0] > 0

    def get_models_by_brand(self, brand: str):
        return self.db.get_models_by_brand(brand)
