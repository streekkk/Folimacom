from PySide6.QtWidgets import QApplication


def center_window(self):
    self.qt_rectangle = self.frameGeometry()
    self.center_point = QApplication.primaryScreen().geometry().center()
    self.qt_rectangle.moveCenter(self.center_point)
    self.move(self.qt_rectangle.topLeft())