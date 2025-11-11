from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QWidget, QMessageBox
from views.arackayit.AracKayitView import Ui_CarRegistration_Widget
from controllers.AracListeController import AracListeController
from PyQt5.QtGui import QGuiApplication, QPixmap
from PyQt5.QtCore import QTimer
from services.ImageProcessingService import ImageProcessingService

from models.AracModel import AracModel
from models.Database import Database
class AracKayitController(QWidget):
    def __init__(self, user):
        super().__init__()
        self.ui = Ui_CarRegistration_Widget()
        self.ui.setupUi(self)
        
                # Screenshot değişkenleri
        self.latest_pixmap = None
        self.last_checksum = None

        # Clipboard listener
        self.clipboard = QGuiApplication.clipboard()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard_for_screenshot)
        self.timer.start(400)

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
        self.ui.AnalyzeSS_Button.clicked.connect(self.analyze_screenshot)

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
        
    def check_clipboard_for_screenshot(self):
        mime = self.clipboard.mimeData()

        if mime.hasImage():
            img = self.clipboard.image()

            # Aynı resmi tekrar işlememek için checksum
            try:
                checksum = hash(img.bits().asstring(img.byteCount()))
            except:
                return

            if checksum == self.last_checksum:
                return

            self.last_checksum = checksum
            self.latest_pixmap = QPixmap.fromImage(img)

            # QLabel’a bas
            self.ui.imageLabel.setPixmap(
                self.latest_pixmap.scaled(
                    self.ui.imageLabel.width(),
                    self.ui.imageLabel.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )   
            
    def analyze_screenshot(self):
        img_path = "temp_ss.png"
        self.latest_pixmap.save(img_path)

        analyzer = ImageProcessingService()
        result = analyzer.analyze_listing_image(img_path)

        QMessageBox.information(
            self,
            "OCR Sonuçları",
            str(result)
        )

"""    def save_screenshot(self, path="arac.png"):
        if not self.latest_pixmap:
            QMessageBox.warning(self, "Hata", "Henüz ekran görüntüsü alınmadı.")
            return False

        self.latest_pixmap.save(path)
        return True
"""
        




