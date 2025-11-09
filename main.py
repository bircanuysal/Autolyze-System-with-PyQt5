import sys

from PyQt5.QtWidgets import QApplication
from controllers.LoginController import LoginController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    controller = LoginController()
    controller.show()

    sys.exit(app.exec_())
