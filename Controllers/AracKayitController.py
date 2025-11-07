from PyQt5.QtWidgets import QWidget, QMessageBox
from Views.arackayit.AracKayitView import Ui_CarRegistration_Widget
from Controllers.AracListeController import AracListeController
from Models.AracModel import AracModel
from Models.Database import Database

class AracKayitController(QWidget):
    def __init__(self, user):
        super().__init__()
        self.ui = Ui_CarRegistration_Widget()
        self.ui.setupUi(self)

        self.user = user
        self.db = Database()

        # --- SABİT KATSAYILAR ---
        self.paint_low = 1.5
        self.paint_mid = 2.5
        self.paint_high = 3.5
        self.paint_front2_extra = 4
        self.paint_front3_extra = 5

        self.change_low = 2.5
        self.change_mid = 4
        self.change_high = 6
        self.change_front2_extra = 8
        self.change_front3_extra = 10

        # --- BOYALI PARÇA GRUPLARI ---
        self.low_parts_paint = [
            self.ui.rightFrontDoorP_CheckBox_2,
            self.ui.leftFrontDoorP_CheckBox_2,
            self.ui.rightRearDoorP_CheckBox_2,
            self.ui.leftRearDoorP_CheckBox_2,
            self.ui.rightRearFenderP_CheckBox_2,
            self.ui.leftRearFenderP_CheckBox_2,
            self.ui.rearHoodP_CheckBox_2
        ]

        self.mid_parts_paint = [
            self.ui.hoodP_CheckBox_2,
            self.ui.rightFrontFenderP_CheckBox_2,
            self.ui.leftFrontFenderP_CheckBox_2
        ]

        self.high_parts_paint = [
            self.ui.roofP_CheckBox_2
        ]

        # --- DEĞİŞEN PARÇA GRUPLARI ---
        self.low_parts_change = [
            self.ui.rightFrontDoorP_CheckBox_2,
            self.ui.leftFrontDoorP_CheckBox_2,
            self.ui.rightRearDoorP_CheckBox_2,
            self.ui.leftRearDoorP_CheckBox_2,
            self.ui.rightRearFenderP_CheckBox_2,
            self.ui.leftRearFenderP_CheckBox_2,
            self.ui.rearHoodP_CheckBox_2
        ]

        self.mid_parts_change = [
            self.ui.hoodP_CheckBox_2,
            self.ui.rightFrontFenderP_CheckBox_2,
            self.ui.leftFrontFenderP_CheckBox_2
        ]

        self.high_parts_change = [
            self.ui.roofP_CheckBox_2
        ]
        
        self.ui.mark_ComboBox.currentTextChanged.connect(self.load_models)
        self.ui.addCar_Button.clicked.connect(self.add_car)
        self.ui.showCar_Button.clicked.connect(self.open_car_list)


        self.load_models()

    def load_models(self):
        brand = self.ui.mark_ComboBox.currentText()
        models = self.db.get_models_by_brand(brand)

        self.ui.model_ComboBox.clear()
        self.ui.model_ComboBox.addItems(models)

    def add_car(self):
        carNo = self.ui.CarNo_Line.text()
        brand = self.ui.mark_ComboBox.currentText()
        model = self.ui.model_ComboBox.currentText()
        km = int(self.ui.km_LineEdit.text())
        year = int(self.ui.year_LineEdit.text())

        # Boya / Değişen sayısı
        painted_count = sum([
            cb.isChecked() for cb in self.ui.paintedInfo_GroupBox.findChildren(type(self.ui.hoodP_CheckBox_2))
        ])

        changed_count = sum([
            cb.isChecked() for cb in self.ui.ChagedInfo_GroupBox.findChildren(type(self.ui.hood_CheckBox_2))
        ])

        score = self.GetScore()

        car = AracModel(
            user_id=self.user.id,
            carNo=carNo,
            brand=brand,
            model=model,
            km=km,
            year=year,
            painted_count=painted_count,
            changed_count=changed_count,
            score=score
        )

        self.db.add_car(car)
        QMessageBox.information(self, "Başarılı", "Araç eklendi.")
        
    def open_car_list(self):
        self.arac_list_window = AracListeController(self.user)
        self.arac_list_window.show()
        
    def GetScore(self):
        total_penalty = 0

        # ------------------------
        # BOYALI PARÇALAR
        # ------------------------
        total_penalty += sum(cb.isChecked() for cb in self.low_parts_paint) * self.paint_low
        total_penalty += sum(cb.isChecked() for cb in self.mid_parts_paint) * self.paint_mid
        total_penalty += sum(cb.isChecked() for cb in self.high_parts_paint) * self.paint_high

        # Ön 3 parça boyalı
        front_paint_parts = {
            "right": self.ui.rightFrontFenderP_CheckBox_2.isChecked(),
            "left": self.ui.leftFrontFenderP_CheckBox_2.isChecked(),
            "hood": self.ui.rearHoodP_CheckBox_2.isChecked()
        }
        painted_count_front = sum(front_paint_parts.values())

        if painted_count_front == 3:
            total_penalty += self.paint_front3_extra
        elif painted_count_front == 2:
            total_penalty += self.paint_front2_extra


        # ------------------------
        # DEĞİŞEN PARÇALAR
        # ------------------------
        total_penalty += sum(cb.isChecked() for cb in self.low_parts_change) * self.change_low
        total_penalty += sum(cb.isChecked() for cb in self.mid_parts_change) * self.change_mid
        total_penalty += sum(cb.isChecked() for cb in self.high_parts_change) * self.change_high

        # Ön 3 parça değişen
        front_change_parts = {
            "right": self.ui.rightFrontFender_CheckBox_2.isChecked(),
            "left": self.ui.leftFrontFender_CheckBox_2.isChecked(),
            "hood": self.ui.hood_CheckBox_2.isChecked()
        }
        changed_count_front = sum(front_change_parts.values())

        if changed_count_front == 3:
            total_penalty += self.change_front3_extra
        elif changed_count_front == 2:
            total_penalty += self.change_front2_extra


        # ------------------------
        # KM CEZASI
        # ------------------------
        km = int(self.ui.km_LineEdit.text())
        total_penalty += min(30, km / 5000)

        # ------------------------
        # MODEL YILI CEZASI
        # ------------------------
        year = int(self.ui.year_LineEdit.text())
        total_penalty += max(0, (2025 - year) * 1.2)

        # ------------------------
        # FINAL SCORE
        # ------------------------
        score = max(0, 100 - total_penalty)
        return round(score)


