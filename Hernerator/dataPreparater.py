'''
Autor: Grinya Lesnoy
Site: https://github.com/GrinyaLesnoy
License: GPL
'''
import krita
from Hernerator import HerneratorDialog
import Hernerator
import importlib 
from Hernerator.modules  import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QFormLayout, QMessageBox, QComboBox, QVBoxLayout,QHBoxLayout, QDialogButtonBox, QSpinBox, QFrame)
#from ConfigParser import SafeConfigParser
import os.path
from os import listdir
import json

class dataPreparater:
    def __init__(self):
        #config = SafeConfigParser()
        #config.read('config.ini')
        #color config.get('main', 'color')
        #SW = config.getint('main', 'SW')
        #SH = config.getint('main', 'SH') 

        self.mainDialog = HerneratorDialog.HerneratorDialog()
        self.mainLayout = QVBoxLayout(self.mainDialog)
        #text notes
        self.formLayout = QFormLayout()
        self.ModulesBox = QComboBox()
        #color selection
        self.ColorsBox = QComboBox()
        #segment size
        self.segmLayout = QHBoxLayout()
        self.SW = QSpinBox()
        self.SH = QSpinBox()
        #buttons
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        #buttons actions
        self.buttonBox.accepted.connect(self.confirmButton)
        self.buttonBox.rejected.connect(self.mainDialog.close)

        self.mainDialog.setWindowModality(Qt.NonModal)
        self.kritaInstance = krita.Krita.instance()
        self.view = Application.activeWindow().activeView()
        self.KritaVers = Application.version ()
        self.initialize()
        

    _Alpfa_ = "Opacity"
    colorSep = " / "
    config = {}
    defaultConfig = {
        'SW' : 8,
        'SH' : 8,
        'Mod' :  'DiamondSquare',
        'colorID' : 0
    }
    configFile = "config.json"
    def initialize(self):
        #self.module = 'DiamondSquare'
        #Get modules
         
        dir = os.path.dirname(__file__) 
        #get config file
        config = self.config
        self.configFile = os.path.join(dir,self.configFile)
        if os.path.isfile(self.configFile):
            with open(self.configFile, mode='r',encoding='utf-8') as f:
                try :
                    j=json.load(f)
                except:
                    j = {}          
        else:
            j = {} 

        config = {**self.defaultConfig,**j}
        
        self.Modules = []
        curr = 0
        selected_m = config['Mod']
        for file in os.listdir(os.path.join(dir,'modules')):
            if file!='__init__.py' and file.endswith(".py"):
                m = file[:-3]
                #globals()[m]
                mod = importlib.import_module("Hernerator.modules."+ m)
                c = getattr(mod ,m)
                try:
                    name = c.Name
                except:
                    name = m 
                if(m == selected_m):
                    curr = len(self.Modules)
                    
                self.Modules.append((m,mod,name))
                self.ModulesBox.addItem(name)

        
        self.ModulesBox.setCurrentIndex(curr)
        #segments steps
        self.SW.setValue(config['SW'])
        self.SH.setValue(config['SH'])
        self.SW.setRange(1, 10000)
        self.SH.setRange(1, 10000)
        self.segmLayout.addWidget(self.SW)
        self.segmLayout.addWidget(self.SH)
        #colors selection
        cs = self.colorSep
        Items = [
            "Black"+cs+"White",
            "Black"+cs+self._Alpfa_,
            "White"+cs+self._Alpfa_,
            "Front color"+cs+"Back color",
            "Front color"+cs+self._Alpfa_
        ]
        ## items value? {"Black/White":"ЧБ"}
        self.ColorsBox.addItems(Items)
        self.ColorsBox.setCurrentIndex(config['colorID'])
        #setCurrentIndex(self.items.keys().index("Black/White"))
        #for i in Items:
        #    self.ColorsBox.addItem(i) 
        
        self.formLayout.addRow('Modul', self.ModulesBox)
        self.formLayout.addRow('Color', self.ColorsBox)
        self.formLayout.addRow('Segment size (2**)', self.segmLayout)

        #decor line
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        #add elements to form
        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(self.line)
        self.mainLayout.addWidget(self.buttonBox)

        #add all to layout
        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(self.line)
        self.mainLayout.addWidget(self.buttonBox)

        self.mainDialog.resize(300, 250)
        self.mainDialog.setWindowTitle("Generator")
        self.mainDialog.setSizeGripEnabled(True)
        self.mainDialog.show()
        self.mainDialog.activateWindow()

    def getComponents(self,type): 
        KritaVers = self.KritaVers  
        type+= 'GroundColor' if (KritaVers=='4.0.0' or KritaVers=='4.0.1') else 'groundColor'
        return getattr(self.view,type)().components()

    
    def confirmButton(self):
        config = self.config
        Colors = self.ColorsBox.currentText().split(self.colorSep)
        SW=self.SW.value()
        SH=self.SH.value()

        #save config file
        config['SW']=SW
        config['SH']=SH
        config['colorID']=self.ColorsBox.currentIndex()
        config['Mod']=self.ModulesBox.currentIndex()
        with open(self.configFile, mode='w',encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4, separators=(',', ': '))
        
        view = Application.activeWindow().activeView()  
        # Front Color
        if Colors[0]=='White' :
            CFront = [1.0,1.0,1.0,1.0]
        elif 'Front' in Colors[0]:
            components = self.getComponents('fore')
            #foregroundColor
            CFront=[
                components[0],
                components[1],
                components[2],
                components[3]
            ]
        else:
            CFront = [0.0,0.0,0.0,1.0]
        # Back Color
        
        if Colors[1]==self._Alpfa_:
            CBack = CFront[:]
            CBack[3]=0.0
        elif 'Back' in Colors[1] :
            components = self.getComponents('back')
            CBack=[
                components[0],
                components[1],
                components[2],
                components[3]
            ]
        else:
            CBack = [1.0,1.0,1.0,1.0]
        
        Options = {
            "CFront" : CFront,
            "CBack" : CBack,
            "SW":SW,
            "SH":SH
        } 
        #Hernerator.modules.DiamondSquare.DiamondSquare(Options)
        module = self.Modules[config['Mod']]
        getattr(module[1], module[0])(Options)
        #self.msgBox = QMessageBox(self.mainDialog)
        #self.msgBox.setText("Complete!")
        #self.msgBox.exec_()
        self.mainDialog.close()
 