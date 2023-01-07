from auth import Login, Registration
from mainwindow import MainWindow
from PyQt6.QtWidgets import QApplication
import sys


app = QApplication(sys.argv)

reg = Registration()
login = Login()
main = MainWindow()
login.next(lambda: reg.show())
login.next2(lambda: main.show())
reg.next(lambda: main.show())
login.show()

sys.exit(app.exec())