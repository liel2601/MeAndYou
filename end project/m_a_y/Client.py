
import sys

import login

from PyQt5.QtWidgets import QMainWindow, QApplication


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = login.Ui_login()
    ui.setupUi(window)
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
