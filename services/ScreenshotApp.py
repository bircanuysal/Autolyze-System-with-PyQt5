import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QGuiApplication, QPixmap
from PyQt5.QtCore import QTimer

class ScreenshotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Araç Analiz")
        self.setGeometry(300, 200, 500, 400)

        # Son alınan görüntü
        self.latest_pixmap = None

        # UI
        self.image_label = QLabel("Henüz ekran görüntüsü alınmadı.")
        self.image_label.setStyleSheet("border:1px solid gray;")
        self.image_label.setScaledContents(True)

        self.save_button = QPushButton("Araç Kaydet")
        self.save_button.clicked.connect(self.save_image)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        # Clipboard dinleme (her 500ms kontrol)
        self.clipboard = QGuiApplication.clipboard()
        self.last_checksum = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(500)

    def check_clipboard(self):
        """Clipboard'a yeni görüntü düştüyse yakala"""
        mime = self.clipboard.mimeData()

        if mime.hasImage():
            pix = self.clipboard.image()

            # Aynı görüntüyü tekrar almamak için checksum kontrolü
            checksum = hash(pix.bits().asstring(pix.byteCount()))
            if checksum == self.last_checksum:
                return

            self.last_checksum = checksum

            self.latest_pixmap = QPixmap.fromImage(pix)
            self.image_label.setPixmap(self.latest_pixmap)
            self.image_label.setText("")

    def save_image(self):
        if self.latest_pixmap is None:
            print("Kaydedilecek görüntü yok.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Görüntüyü Kaydet", "arac.png", "PNG Files (*.png)"
        )

        if file_path:
            self.latest_pixmap.save(file_path)
            print("Kaydedildi:", file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenshotApp()
    window.show()
    sys.exit(app.exec_())
