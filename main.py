from auth import Login, Registration
from mainwindow import MainWindow
from PyQt6.QtWidgets import QApplication
import sys
from database import create_db_and_execute_sql_script


app = QApplication(sys.argv)

reg = Registration()
login = Login()
main = MainWindow()
login.next(lambda: reg.show())
login.next2(lambda: main.show())
reg.next(lambda: main.show())
login.show()

if __name__ == '__main__':
    create_db_and_execute_sql_script()

sys.exit(app.exec())