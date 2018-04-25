'''
------ CC 0 1.0 ---------------
'''
import krita
from krita import * 
from Hernerator import dataPreparater
class Hernerator(krita.Extension):
    def __init__(self, parent):
        super().__init__(parent)
		
    def setup(self):
        pass 
		
    def createActions(self, window):
        action = window.createAction("Hernerator", "Horseradish's Generator", "tools/scripts")
        action.setToolTip("Horseradish's Generator")
        action.triggered.connect(self.initialize)

    def initialize(self):
        #DiamondSquare.DiamondSquare()
        self.dataPreparater = dataPreparater.dataPreparater() 
		 

Scripter.addExtension(Hernerator(krita.Krita.instance()))