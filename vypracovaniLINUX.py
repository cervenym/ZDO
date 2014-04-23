'''
Created on 8. 4. 2014
Nadstavba zadani ze ZDO, pro LINUX, shoda se zadanim BOHUZEL NETESTOVANO 
'''
import cv2
import skimage.morphology
import numpy
import scipy.ndimage
import os
import pickle

class Znacky:
    """
    skupina jmenem cervenym

    """
    def __init__(self):
        
        def nactiTridyEtalonyPickle(self,nazev):
            pole = pickle.load( open( nazev, "rb" ) )
            tridy = pole[0]
            etalony = pole[1]
            return tridy,etalony
        #cesta ke skriptu
        path_to_script = os.path.dirname(os.path.abspath(__file__))
        # spojeni s relativni cestou
        classifier_path = os.path.join(path_to_script, "OBRpickle.p")
        self.tridy,self.etalony = nactiTridyEtalonyPickle(classifier_path)
        pass
        
    
        
    def vyberBilou(self,huehue,saturace,value): # OTSU PRAHOVANI
        #print saturace[50][50]
        #print value[50][50]
        #print numpy.mean(saturace)
        TF1 = saturace <= numpy.mean(saturace) 
        TF2 = value >= numpy.mean(value) -35 # znackaModra
        TF = TF1*TF2+ 0
        kernel_big = skimage.morphology.diamond(3)
        TF = skimage.morphology.binary_closing(TF, kernel_big) # OTEVRENI
        TF = cv2.GaussianBlur(TF,(5,5), 5) #GAUSSOVSKA FILTRACE PODRUHE
        return TF
    
    def vyberSymbol(self,cernobily,cervena): #CHYBELO TAKE
        kernel_big = skimage.morphology.rectangle(3,3)
        #cernobily2 = skimage.morphology.binary_dilation(cernobily, kernel_big)
        #plt.imshow(cernobily2,plt.gray())
        #plt.show()    
        vyplneny = scipy.ndimage.morphology.binary_fill_holes(cervena) #VYPLNENI DER CERVENE
        cervenaF = cervena ==0
        vyplnenyT = vyplneny ==1
        vyplnenyT = vyplneny*cervenaF
        cernobilyF = cernobily ==0 #NEBILE OBLASTI OBRAZKU
        cernobilyT = cernobily ==1
        vnitrek = (cernobilyF *vyplnenyT) #VNITREK CERVENEHO TROJUHELNIKU (mozna symbol)
        #TF = (cernobilyF) * vnitrek # SYMBOL CERNY
        TF = (cernobilyT*vyplnenyT) # SYMBOL "BILY"
        TF = TF+ 0
        #print numpy.min(TF)
        TF = skimage.morphology.binary_dilation(TF, kernel_big) # DILATACE
        return TF
    
    def prumetY(self,matice):
        vysledek = [0]*len(matice)
        counter =0;
        for x in matice:
            vysledek[counter] = numpy.sum(x)
            counter = counter+1
        return vysledek
    
    def prumetX(self,matice):
        vysledek = [0]*len(matice)
        for x in matice:
            #print x
            counter =0;
            for i in x:
                #print vysledek
                vysledek[counter] = vysledek[counter] + i
                counter = counter+1
        return vysledek
    
    def vyberCervenou(self,huehue,saturace,value): #TRIK JE VYBRAT TAKE TMAVOU ORANZOVOU (aka hnedou?)
        TF1 = huehue <=179 #cervena1
        TF2 = huehue >=160 #cervena2
        TF4 = huehue <= 22 #oranzova
        TF3 = saturace >=90# TMAVA ORANZOVA 
        TF = (TF1*TF2)+(TF4*TF3) + 0
        #TF = TF*TF3 + 0
        
        #plt.imshow(TF)
        #plt.show()
        kernel_big = skimage.morphology.diamond(1)
        #print TF
        TF = skimage.morphology.binary_opening(TF, kernel_big) # OTEVRENI
        TF = cv2.GaussianBlur(TF,(5,5), 5) #GAUSSOVSKA FILTRACE PODRUHE
        return TF
    
    def vyberModrou(self,huehue,saturace,value):
        TF2 = huehue >=95
        TF1 = huehue <=110
        TF3 = saturace >= 80
        
        TF = TF1*TF2*TF3 + 0
        kernel_big = skimage.morphology.diamond(1)
        TF = skimage.morphology.binary_opening(TF, kernel_big) # OTEVRENI
        TF = cv2.GaussianBlur(TF,(5,5), 5) #GAUSSOVSKA FILTRACE PODRUHE
        return TF
        
    def vyberZlutou(self,huehue,saturace,value):
        TF2 = huehue >=20
        TF1 = huehue <=40
        TF3 = saturace >= 80
        
        TF = TF1*TF2*TF3 + 0
        kernel_big = skimage.morphology.diamond(1)
        TF = skimage.morphology.binary_opening(TF, kernel_big) # OTEVRENI
        TF = cv2.GaussianBlur(TF,(5,5), 5) #GAUSSOVSKA FILTRACE PODRUHE
        return TF
    
    def vyberZelenou(self,huehue,saturace,value): #VYBERE I PONEKUD MODROU ZELENOU - POUZITA NA ZNACKACH MA PRIMES MODRE
        TF2 = huehue >=38
        TF1 = huehue <=100
            
        TF = TF1*TF2 + 0
        kernel_big = skimage.morphology.diamond(1)
        TF = skimage.morphology.binary_opening(TF, kernel_big) # OTEVRENI
        TF = cv2.GaussianBlur(TF,(5,5), 5) #GAUSSOVSKA FILTRACE PODRUHE
        return TF
    
    def vyberHrany(self,cernobily): #CHYBELO
        TF = cv2.Canny(cernobily,50,50)
        #plt.imshow(TF)
        #plt.show()
        kernel_big = skimage.morphology.diamond(1)
        TF = skimage.morphology.binary_dilation(TF, kernel_big) # DILATACE
        TF = cv2.GaussianBlur(TF,(5,5), 5) #GAUSSOVSKA FILTRACE PODRUHE
        return TF
    
    def udelejObraz(self,jabko):
        #print nazev
        #jabko= cv2.imread(nazev, cv2.CV_LOAD_IMAGE_COLOR)
        x = cv2.resize(jabko,(100,100)  ,interpolation=cv2.INTER_LINEAR) #NORMALIZACE
        filtrovanejabko = cv2.GaussianBlur(x,(5,5), 5) #GAUSSOVSKA FILTRACE
        prebarveny = cv2.cvtColor(filtrovanejabko,cv2.COLOR_BGR2HSV) #PREVEDENI NA HSV
        cernobily = cv2.cvtColor(filtrovanejabko,cv2.COLOR_BGR2GRAY) #PREVEDENI NA HSV    
        huehue =  prebarveny[:,:,0] 
        saturace = prebarveny[:,:,1] 
        value = prebarveny[:,:,2]
        
        TFcervena = self.vyberCervenou(huehue,saturace,value)
        TFmodra = self.vyberModrou(huehue,saturace,value)
        TFzluta = self.vyberZlutou(huehue,saturace,value)
        TFbila = self.vyberBilou(huehue,saturace,value)
        TFzelena= self.vyberZelenou(huehue,saturace,value)    
        TFhrany = self.vyberHrany(cernobily)
        TFsymbol = self.vyberSymbol(TFbila,TFcervena)
        
        Xcervena = self.prumetX(TFcervena)
        Ycervena = self.prumetY(TFcervena)
        Xmodra = self.prumetX(TFmodra)
        Ymodra = self.prumetY(TFmodra)
        Xzluta = self.prumetX(TFzluta)
        Yzluta = self.prumetY(TFzluta)
        Xbila = self.prumetX(TFbila)
        Ybila = self.prumetY(TFbila)
        Xzelena = self.prumetX(TFzelena)
        Yzelena = self.prumetY(TFzelena)   
        Xhrany = self.prumetX(TFhrany)
        Yhrany = self.prumetY(TFhrany)  
        Xsymbol = self.prumetX(TFsymbol)
        Ysymbol = self.prumetY(TFsymbol)  
        
        vektor = Xcervena + Xmodra + Xzluta + Xbila + Xzelena + Xhrany+ Xsymbol+  Ycervena + Ymodra + Yzluta + Ybila + Yzelena + Yhrany+Ysymbol
        #vektor = Xcervena + Xmodra + Xzluta + Xbila + Xzelena + Xhrany+  Ycervena + Ymodra + Yzluta + Ybila + Yzelena + Yhrany
        return vektor
    
    def nactiTridyEtalonyPickle(self,nazev):
        pole = pickle.load( open( nazev, "rb" ) )
        tridy = pole[0]
        etalony = pole[1]
        return tridy,etalony
    
    def vyberMinPole(self,pole):
        index = 0
        pozice = 0
        hodnota = 0
        minimum = pole[0]
        for x in pole:
            if (x < minimum):
                minimum = x
                hodnota = x
                index = pozice
            pozice = pozice+1
        return index,hodnota
    
    def dejVzdalenost(self,seznam1,seznam2):
        vektor1 = numpy.asarray(seznam1)
        vektor2 = numpy.asarray(seznam2)
        cislo = numpy.linalg.norm(vektor1-vektor2)
        return cislo


    def rozpoznejZnacku(self, image):
        
        obr = image
        
        obrazUI = self.udelejObraz(obr)
        poleVzdalenosti = []
        pozice = 0
        for etalon in self.etalony:
            eukleidovskaVzdalenost = self.dejVzdalenost(etalon,obrazUI)           
            poleVzdalenosti.append(eukleidovskaVzdalenost)
            pozice = pozice+1
        index,hodnota = self.vyberMinPole(poleVzdalenosti)
        vybrana = self.tridy[index]
        
        retval = vybrana
        return retval
            
'''KONEC CLASS Znacky'''
