'''
Author: Grinya Lesnoy
Site: https://github.com/GrinyaLesnoy
License: GPL
'''
import krita
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
import struct
from Hernerator import  Float16Compressor


class Renderer():
    def __init__(self,Options={}):
        self.d = Krita.instance().activeDocument()
        self.CW=self.d.width()
        self.CH=self.d.height()
        #dictionary to variable
        for k in Options:
            #if hasattr(self, Options):
            setattr(self, k, Options[k])

        self.n = self.d.activeNode()
         #get pixel data for sample
        ba=self.n.pixelData(0,0,1,1)
        #pixel size (bytes per pixel)
        self.pxSize = ba.size()
        
        #not editable layer
        if self.pxSize == 0:
            return 'Error: layer not editable'
        elif self.pxSize == 1:
        # in Krita mask have only 1 8 bit chanel oO
            self.chanelsCount = 1 
            #color model
            self.cm = "U8"
        else :
            self.chanelsCount = 4
            #color model
            self.cm=self.d.colorDepth() 

        self.ran = range(self.chanelsCount) 
        if self.cm == "F16":
            self.f16comp = Float16Compressor.Float16Compressor()

        #max colors
        # "U8" - 256 (0-255) "U16" - 65536 values (0-65535) "F16" and "F32" - 0.0-1.0
        self.mod=255 if self.cm == "U8" else 256**2-1 if  self.cm== "U16"  else  1.0

        
        #bits data in pixel Data per chanel: 8bit - 1, 16bit - 2, 32bit - 4
        # 8 bit - R G B A, 16bit - RR GG BB AA, 32bit - RRRR GGGG BBBB AAAA 
        self.chSize = 1 if self.pxSize == 1 else int(int(self.cm[1:])/8) 
        
        self.mapGenerator()

    def mapGenerator(self):
        pass

    CFront = [0.0,0.0,0.0,1.0]
    CBack = [1.0,1.0,1.0,1.0]

    #convert current layer pixel data to color array
    def getCurrentLayerPxData(self): 
        n = self.n 
        bBa=n.pixelData(0,0,self.CW,self.CH)
        s = bBa.size()
        
        ## Сделать поправку на положение слоя! 
        _curr=0 
        pxSize = self.pxSize
        chSize = self.chSize 
        cm=self.cm
        ran = self.ran
        mod=self.mod
        if cm == "F16":
            f16comp = self.f16comp
        A=[]
        while _curr < s:
            #get currebt pixel color          
            pixel = bBa[_curr:_curr+pxSize]
            _curr+=pxSize   
            temp=[]
            # l = 0 ... 3 [R,G,B,A]
            for l in ran:  
                # current color of pixel[start of color:end of color] (chSize - color's bytes count: U8 -1, U16 - 2 ...)
                pc =  pixel[ l*chSize : (l+1)*chSize ]
                temp.append(
                    f16comp.decompress(pc) if cm == 'F16' else struct.unpack('f', pc)[0] if cm == 'F32' else int.from_bytes(pc, byteorder='big')/mod 
                ) 
            A.append(temp) 
        return A

    def render(self,Map):
        print('render')  

        size = self.pxSize
        cm=self.cm
        chSize = self.chSize 
        mod=self.mod
        if cm == "F16":
            f16comp = self.f16comp

        #get colordata 
        CFront=self.CFront
        CBack=self.CBack
            #Color Delta - difference color data Front and Back
            #Front Red = Back Red + Deltd Red, Front Green = ... 
        #invert color from F32 
        #if cm == "F32" or cm == "F16":
        #    CFront[0],CFront[2]=CFront[2],CFront[0] 
        #    CBack[0],CBack[2]=CBack[2],CBack[0] 
        CD= [
            CFront[0]-CBack[0],
            CFront[1]-CBack[1],
            CFront[2]-CBack[2],
            CFront[3]-CBack[3]
            ]
            
        #convert Map to line
        X=0
        Y=0
        CW=self.CW
        CH=self.CH 
        ran = self.ran  
        #convert Generated Map to Color Map: 
        ColorMap = []
        while Y<CH:
            i=Map[X,Y]
            ColorMap.append([ (CBack[l]+CD[l]*i) for l in ran ])
            X+=1
            if X>=CW:
                X=0
                Y+=1
 
 
        # if Alpha == True - blending layre pixel data
        Alpha = True if CBack[3]<1 else False
        if Alpha==True :   
            ColorMap_old = self.getCurrentLayerPxData()
        
        #convert pixel data array to line from bytes
        ba=QByteArray()
        R = range(len(ColorMap))
        for i in R :      
            pixel = ColorMap[i]

            if  Alpha == True :
                pixel_bg = ColorMap_old[i]
                an = pixel_bg[3]

            for l in ran:
                c=pixel[l]
                if c<0:
                    c*=-1

                if  Alpha == True and an >0 :# 
                    #c = c+an if c== 3 else pixel_bg[l]*an + c*pixel[3]  
                    if l == 3 :
                        c+=an
                    else:
                        #????
                        c= pixel_bg[l]*an + c*pixel[3]
                
                if c<0:
                    c*=-1
                if c>1:
                    c=1
                
                if cm == 'F32':
                    c= struct.pack('f', c)
                elif cm == 'F16':
                    c = f16comp.compress(c)
                
                else :
                    #to int
                    #c=int(c*mod)
                    # mod 16 ==  255 ??! o_O
                    c=int(c*255)
                    # 255 => 0xff => ff
                    #c=format(c,'x')
                    c=hex(c)[2:]
                    # ff => ff, f => 0f
                    j = 2 if cm == 'U8' else 4
                    l=len(str(c))
                    c= '0'*(j-l)+c
                    #string to bites
                    c = bytes.fromhex(c)
                   
                ba.append(c)
 
        
        
        self.n.setPixelData(ba,0,0,CW,CH)
        #n.setVisible(False)
        #n.setVisible(True)
        print('finish')
        return 'finish' 
