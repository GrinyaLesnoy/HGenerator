'''
------ CC 0 1.0 ---------------
'''
import krita
from krita import * 
from HGenerator import dataPreparater
class HGeneratorExtension(krita.Extension):
    def __init__(self, parent):
        super().__init__(parent)
		
    def setup(self):
        pass 
		
    def createActions(self, window):
        action = window.createAction("HGenerator", "Horseradish's Generator", "tools/scripts")
        action.setToolTip("Horseradish's Generator")
        action.triggered.connect(self.initialize)

    def initialize(self):
        #DiamondSquare.DiamondSquare()
        self.dataPreparater = dataPreparater.HGDataPreparater()
        self.dataPreparater.initialize()
		 

Scripter.addExtension(HGeneratorExtension(krita.Krita.instance()))