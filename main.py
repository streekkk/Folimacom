import sys
import os
from PySide6.QtWidgets import QApplication
from Folimacom_ui import Folimacom_ui

basedir = os.path.dirname(__file__)
'''
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'FIX.Folimacom.1.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass
'''
def main():
    app = QApplication(sys.argv)
    folimacom_window = Folimacom_ui()
    folimacom_window.show()
    with open(os.path.join(basedir, 'style/style.css'), 'r') as f:
        style = f.read()
        app.setStyleSheet(style)
    app.exec()


if __name__ == "__main__":
    main()
