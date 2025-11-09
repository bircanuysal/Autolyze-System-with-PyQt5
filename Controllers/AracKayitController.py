from PyQt5.QtWidgets import QWidget, QMessageBox
from views.arackayit.AracKayitView import Ui_CarRegistration_Widget
from controllers.AracListeController import AracListeController
from models.AracModel import AracModel
from models.Database import Database
class AracKayitController(QWidget):
    def __init__(self, user):
        super().__init__()
        self.ui = Ui_CarRegistration_Widget()
        self.ui.setupUi(self)
        
        from services.CarRepository import CarRepository
        from services.CarRegistrationService import CarRegistrationService  
        from services.ScoreCalculator import ScoreCalculator
        
        self.user = user
        self.repo = CarRepository()
        self.score_calc = ScoreCalculator(self.ui)
        self.service = CarRegistrationService(self.repo, self.score_calc)

        self.ui.mark_ComboBox.currentTextChanged.connect(self.load_models)
        self.ui.addCar_Button.clicked.connect(self.add_car)
        self.ui.showCar_Button.clicked.connect(self.open_car_list)

        self.load_models()

    def load_models(self):
        brand = self.ui.mark_ComboBox.currentText()
        models = self.repo.get_models_by_brand(brand)
        self.ui.model_ComboBox.clear()
        self.ui.model_ComboBox.addItems(models)

    def add_car(self):
        carNo = self.ui.CarNo_Line.text()
        brand = self.ui.mark_ComboBox.currentText()
        model = self.ui.model_ComboBox.currentText()
        km = int(self.ui.km_LineEdit.text())
        year = int(self.ui.year_LineEdit.text())

        success, message = self.service.register_car(
            self.user, carNo, brand, model, km, year
        )

        if success:
            QMessageBox.information(self, "Başarılı", message)
        else:
            QMessageBox.warning(self, "Hata", message)

    def open_car_list(self):
        self.arac_list_window = AracListeController(self.user)
        self.arac_list_window.show()

