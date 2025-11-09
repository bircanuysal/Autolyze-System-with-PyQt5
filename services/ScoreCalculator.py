# services/score_calculator.py
class ScoreCalculator:
    def __init__(self, ui):
        self.ui = ui

        # Katsayılar
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

        # Boya grupları
        self.low_parts_paint = [...]
        self.mid_parts_paint = [...]
        self.high_parts_paint = [...]

        # Değişen grupları
        self.low_parts_change = [...]
        self.mid_parts_change = [...]
        self.high_parts_change = [...]

    def calculate(self):
        total = 0

        # Boya hesaplama
        total += sum(cb.isChecked() for cb in self.low_parts_paint) * self.paint_low
        total += sum(cb.isChecked() for cb in self.mid_parts_paint) * self.paint_mid
        total += sum(cb.isChecked() for cb in self.high_parts_paint) * self.paint_high

        # Ön 3 boya
        front_paint_parts = {
            "right": self.ui.rightFrontFenderP_CheckBox_2.isChecked(),
            "left": self.ui.leftFrontFenderP_CheckBox_2.isChecked(),
            "hood": self.ui.rearHoodP_CheckBox_2.isChecked()
        }
        count_front_paint = sum(front_paint_parts.values())
        if count_front_paint == 3:
            total += self.paint_front3_extra
        elif count_front_paint == 2:
            total += self.paint_front2_extra

        # Değişen hesaplama
        total += sum(cb.isChecked() for cb in self.low_parts_change) * self.change_low
        total += sum(cb.isChecked() for cb in self.mid_parts_change) * self.change_mid
        total += sum(cb.isChecked() for cb in self.high_parts_change) * self.change_high

        # Ön 3 değişen
        front_change_parts = {
            "right": self.ui.rightFrontFender_CheckBox_2.isChecked(),
            "left": self.ui.leftFrontFender_CheckBox_2.isChecked(),
            "hood": self.ui.hood_CheckBox_2.isChecked()
        }
        count_front_change = sum(front_change_parts.values())
        if count_front_change == 3:
            total += self.change_front3_extra
        elif count_front_change == 2:
            total += self.change_front2_extra

        # KM
        km = int(self.ui.km_LineEdit.text())
        total += min(30, km / 5000)

        # Yıl
        year = int(self.ui.year_LineEdit.text())
        total += max(0, (2025 - year) * 1.2)

        score = max(0, 100 - total)
        return round(score)
