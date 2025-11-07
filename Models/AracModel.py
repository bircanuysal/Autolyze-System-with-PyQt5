class AracModel:
    def __init__(self, id=None, user_id=None, carNo=0, brand="", model="", km=0, year=0,
                 painted_count=0, changed_count=0, score=0):

        self.id = id
        self.carNo = carNo
        self.user_id = user_id
        self.brand = brand
        self.model = model
        self.km = km
        self.year = year
        self.painted_count = painted_count
        self.changed_count = changed_count
        self.score = score
