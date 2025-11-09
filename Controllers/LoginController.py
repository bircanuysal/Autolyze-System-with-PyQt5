from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from views.login.LoginView import Ui_MainWindow
from controllers.AracKayitController import AracKayitController
from models.UserModel import UserModel
from models.Database import Database

class LoginController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = Database()

        self.ui.logIn_PushButton.clicked.connect(self.on_login)

    def on_login(self):
        username = self.ui.name_LineEdit.text().strip()

        if not username:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı boş olamaz.")
            return

        user = self.db.get_user(username)

        if user is None:
            user = UserModel(username=username)
            user = self.db.add_user(user)

        self.car_window = AracKayitController(user)
        self.car_window.show()
        self.close()
