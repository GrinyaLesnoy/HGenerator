'''
------ CC 0 1.0 ---------------
'''
from PyQt5.QtWidgets import QDialog

class HerneratorDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

    def closeEvent(self, event):
        event.accept()