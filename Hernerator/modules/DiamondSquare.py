'''
The diamond-square algorithm 
'''
import random  
from Hernerator import Renderer

class DiamondSquare(Renderer.Renderer):
    
    Name = 'Clouds Generator (Diamond Square)'
    def __init__(self,Options={}):
        super().__init__(Options)
    
    # pow of segment's width and height  
    SW=8
    SH=8
    def mapGenerator(self):
        print('start')
        Map = {}
        X=0
        Y=0
        CW=self.CW
        CH=self.CH
        # segment's width and height
        W=2**self.SW
        H=2**self.SH
        while Y<=CH+H:
            if X>=CW+W:
                X=0
                Y+=H
            Map[X,Y]=random.random()
            X+=W 
              

        # if segment 0x0 == random noise
        if self.SW==0 and self.SH == 0 :
            self.render(Map)
            return
        # Max and min Amplituda (Max=256/2)
        AM = 0.5
        Am = 0.001  
        # mean of segment's width and height (if W==H then WH2 == W)
        WH2 = (W+H)/2
        # width and height for part of segment
        w=W
        h=H
        stage1=True
        # stage1=True - stage I, stage1=False - stage II and III
        while w>1 or h>1:
            # 0.5 of segment's part
            w2=w>>1
            h2=h>>1
            # mean of segment's part width and height
            wh2=(w+h)/2
            # Amplituda (A). Is limiter of random coefficient.
            # value of pixel data = mean of sum neighboring pixels value + random*Amplituda
            # or a5 = (a1+a2+a3+a4)/4 + A*random()
            # whithout random - is gradient effect
            # whithout A - is random noise effekt
            # From the straight line: ( AM-Am )*wh2 + ( wh2m-wh2M )*A + ( wh2M*Am - wh2m*AM )=0; 
            A =  ( ( AM-Am )*wh2 + WH2*Am - AM )/( WH2-1 )
            
            # 3 stage of algoritm:
            # 	
            #   set a5          set a5.4 and a5.2        set a5.1 and a5.3 
            #	a1----a2    	 +---a5.1---+   		+----a5'---+
            #   | \  / |    	 |     |    |   		|     |    |
            #I)	|  a5  |	II)	a5.4<-a5->a5.2  III)	a1->a5.1<-a2
            #   | /  \ |		 |     |    |			|     |    |
            #   a3----a4		 +---a5.3---+			+----a5----+
            #

            
            X=0
            Y=0
            while Y<=CH:
                
                if stage1 == True:
                    #stage I 
                    sum= (Map[X,Y]+Map[(X+w),Y]+Map[(X+w),(Y+h)]+Map[X,(Y+h)])/4
                    min = sum-A
                    max = sum+A 
                    if not ((X+w2),(Y+h2)) in Map:
                        Map[(X+w2),(Y+h2)]=int(random.uniform(min,max)/Am)*Am 
                else:
                    #stage 2
                    a1=Map[X,Y]
                    a2=Map[(X+w),Y]
                    a3=Map[(X+w),(Y+h)]
                    a4=Map[X,(Y+h)]
                    a5=Map[(X+w2),(Y+h2)]

                    #for a5.1 
                    x = X+w2 
                    y = Y
                    a_tmp = (a1+a2+a5)/3-A if y==0 else  Map[x,(y-h2)]
                    sum = (a1+a2+a5+a_tmp)/4
                    min = sum-A
                    max = sum+A
                    if not (x,y) in Map:
                        Map[x,y]=int(random.uniform(min,max)/Am)*Am
                    
                    #for a5.2
                    x = X+w
                    y = Y+h2 
                    a_tmp = (a2+a3+a5)/3-A if x>=CW else  Map[(x+w2),y]
                    sum = (a2+a3+a5+a_tmp)/4
                    min = sum-A
                    max = sum+A
                    if not (x,y) in Map:
                        Map[x,y]=int(random.uniform(min,max)/Am)*Am
                    
                    #for a5.3
                    x = X+w2
                    y = Y+h 
                    a_tmp = (a3+a4+a5)/3-A if y>=CH else  Map[x,(y+h2)]
                    sum = (a3+a4+a5+a_tmp)/4
                    min = sum-A
                    max = sum+A
                    if not (x,y) in Map:
                        Map[x,y]=int(random.uniform(min,max)/Am)*Am

                    #for a5.4
                    x = X
                    y = Y+h2 
                    a_tmp = (a4+a1+a5)/3-A if x==0 else  Map[(x-w2),y]
                    sum = (a4+a1+a5+a_tmp)/4
                    min = sum-A
                    max = sum+A
                    if not (x,y) in Map:
                        Map[x,y]=int(random.uniform(min,max)/Am)*Am
                        

                X+=w
                if X >= CW:
                    X=0
                    Y+=h

            # ENDwhile Y-CH 
            if w<=1 and h<=1:
                break

            if stage1==False:
                w=1 if w == 1 else w>>1
                h=1 if h == 1 else h>>1
                print(w)
            
            #True to False | False to True
            stage1=bool(1-stage1)
            

        #End while w!=0 and h!=0

        self.render(Map)

    
    
#DiamondSquare()