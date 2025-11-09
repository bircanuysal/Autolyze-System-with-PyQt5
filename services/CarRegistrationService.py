# services/car_registration_service.py
from models.AracModel import AracModel

class CarRegistrationService:
    def __init__(self, repository, score_calculator):
        self.repository = repository
        self.score_calculator = score_calculator

    def register_car(self, user, carNo, brand, model, km, year):
        if self.repository.car_exists(carNo, user.id):
            return False, "Bu CarNo zaten kayıtlı."

        score = self.score_calculator.calculate()

        car = AracModel(
            user_id=user.id,
            carNo=carNo,
            brand=brand,
            model=model,
            km=km,
            year=year,
            painted_count=0,
            changed_count=0,
            score=score
        )

        self.repository.add_car(car)
        return True, "Araç başarıyla eklendi."
