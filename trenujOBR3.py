'''
Created on 7. 4. 2014
Created on 8. 4. 2014
VAROVANI - BEZI DLOUHO
Program pro trenovani dane mnoziny. Vysledky zapise do souboru "OBR_1.txt","OBR_2.txt" a "OBR_3.txt". Trenovaci data nacte z 
adresare. Adresar je v programu (natvrdo) dany:
'D:\semestr\obrazy\zdo2014-training\zdo2014-training'
Pokud mate adresar jiny tak jej prosim zmente.
@author: cervenym
'''

import cv2
import skimage.filter
import glob
import os
import numpy
import skimage.morphology
import scipy.ndimage

def vyberBilou(huehue,saturace,value): # OTSU PRAHOVANI
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

def vyberSymbol(cernobily,cervena): #CHYBELO TAKE
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

def prumetY(matice):
    vysledek = [0]*len(matice)
    counter =0;
    for x in matice:
        vysledek[counter] = numpy.sum(x)
        counter = counter+1
    return vysledek

def prumetX(matice):
    vysledek = [0]*len(matice)
    for x in matice:
        #print x
        counter =0;
        for i in x:
            #print vysledek
            vysledek[counter] = vysledek[counter] + i
            counter = counter+1
    return vysledek

def vyberCervenou(huehue,saturace,value): #TRIK JE VYBRAT TAKE TMAVOU ORANZOVOU (aka hnedou?)
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

def vyberModrou(huehue,saturace,value):
    TF2 = huehue >=95
    TF1 = huehue <=110
    TF3 = saturace >= 80
    
    TF = TF1*TF2*TF3 + 0
    kernel_big = skimage.morphology.diamond(1)
    TF = skimage.morphology.binary_opening(TF, kernel_big) # OTEVRENI
    TF = cv2.GaussianBlur(TF,(5,5), 5) #GAUSSOVSKA FILTRACE PODRUHE
    return TF
    
def vyberZlutou(huehue,saturace,value):
    TF2 = huehue >=20
    TF1 = huehue <=40
    TF3 = saturace >= 80
    
    TF = TF1*TF2*TF3 + 0
    kernel_big = skimage.morphology.diamond(1)
    TF = skimage.morphology.binary_opening(TF, kernel_big) # OTEVRENI
    TF = cv2.GaussianBlur(TF,(5,5), 5) #GAUSSOVSKA FILTRACE PODRUHE
    return TF

def vyberZelenou(huehue,saturace,value): #VYBERE I PONEKUD MODROU ZELENOU - POUZITA NA ZNACKACH MA PRIMES MODRE
    TF2 = huehue >=38
    TF1 = huehue <=100
        
    TF = TF1*TF2 + 0
    kernel_big = skimage.morphology.diamond(1)
    TF = skimage.morphology.binary_opening(TF, kernel_big) # OTEVRENI
    TF = cv2.GaussianBlur(TF,(5,5), 5) #GAUSSOVSKA FILTRACE PODRUHE
    return TF

def vyberHrany(cernobily): #CHYBELO
    TF = cv2.Canny(cernobily,50,50)
    #plt.imshow(TF)
    #plt.show()
    kernel_big = skimage.morphology.diamond(1)
    TF = skimage.morphology.binary_dilation(TF, kernel_big) # DILATACE
    TF = cv2.GaussianBlur(TF,(5,5), 5) #GAUSSOVSKA FILTRACE PODRUHE
    return TF

def udelejObraz(nazev):
    jabko= cv2.imread(nazev, cv2.CV_LOAD_IMAGE_COLOR)
    x = cv2.resize(jabko,(100,100)  ,interpolation=cv2.INTER_LINEAR) #NORMALIZACE
    filtrovanejabko = cv2.GaussianBlur(x,(5,5), 5) #GAUSSOVSKA FILTRACE
    prebarveny = cv2.cvtColor(filtrovanejabko,cv2.COLOR_BGR2HSV) #PREVEDENI NA HSV
    cernobily = cv2.cvtColor(filtrovanejabko,cv2.COLOR_BGR2GRAY) #PREVEDENI NA HSV    
    huehue =  prebarveny[:,:,0] 
    saturace = prebarveny[:,:,1] 
    value = prebarveny[:,:,2]
    
    TFcervena = vyberCervenou(huehue,saturace,value)
    TFmodra = vyberModrou(huehue,saturace,value)
    TFzluta = vyberZlutou(huehue,saturace,value)
    TFbila = vyberBilou(huehue,saturace,value)
    TFzelena= vyberZelenou(huehue,saturace,value)    
    TFhrany = vyberHrany(cernobily)
    TFsymbol = vyberSymbol(TFbila,TFcervena)
    
    Xcervena = prumetX(TFcervena)
    Ycervena = prumetY(TFcervena)
    Xmodra = prumetX(TFmodra)
    Ymodra = prumetY(TFmodra)
    Xzluta = prumetX(TFzluta)
    Yzluta = prumetY(TFzluta)
    Xbila = prumetX(TFbila)
    Ybila = prumetY(TFbila)
    Xzelena = prumetX(TFzelena)
    Yzelena = prumetY(TFzelena)   
    Xhrany = prumetX(TFhrany)
    Yhrany = prumetY(TFhrany)  
    Xsymbol = prumetX(TFsymbol)
    Ysymbol = prumetY(TFsymbol)  
    
    vektor = Xcervena + Xmodra + Xzluta + Xbila + Xzelena + Xhrany+ Xsymbol+  Ycervena + Ymodra + Yzluta + Ybila + Yzelena + Yhrany+Ysymbol
    #vektor = Xcervena + Xmodra + Xzluta + Xbila + Xzelena + Xhrany+  Ycervena + Ymodra + Yzluta + Ybila + Yzelena + Yhrany
    return vektor

def zapisPole(pole,soubor):
    for x in pole:
        soubor.write(str(x) + ' ')
    return

def zapisTridyaEtalonyDoSouboru(tridy,etalony,cast):
    if(cast == 1): # ===ROZDELENI NA CASTI
        nazev = "OBR_1.txt"
    if(cast == 2):
        nazev = "OBR_2.txt"
    if(cast == 3):
        nazev = "OBR_3.txt"
                
    soubor = open(nazev,'w')
    counter = 0 
    for x in tridy:
        soubor.write(x)
        soubor.write('\n')
        zapisPole(etalony[counter],soubor)
        soubor.write('\n')
        counter = counter+1
    
    
    return

def nactiTridyEtalonyZeSouboru():
    soubor = open('OBR.txt','r')
    tridy = []
    etalony = []
    radky = soubor.readlines()
    #print radky
    counter = 1
    for radek in radky:
        radek = radek.strip()
        if(counter % 2 == 1): #radek je trida
            tridy.append(radek)
        else:                 #radek je etalon
            radek = radek.strip()
            radek = radek.split()
            policko = []
            for x in radek:
                h = float(x)
                policko.append(h)
                
            etalony.append(policko)
        counter = counter+1
    #print tridy
    #print etalony
    return tridy,etalony

def vydelVektorCislem(vektor,cislo):
    #print vektorA
    #print vektorB
    counter = 0    
    vektorD = vektor
    for b in vektor:
        vektorD[counter] = b/cislo
        counter = counter+1
    return vektorD      
    

def sectiVektory(vektorA,vektorB):
    #print vektorA
    #print vektorB
    counter = 0    
    vektorD = vektorA
    for b in vektorB:
        vektorD[counter] = vektorA[counter]+b
        counter = counter+1
    return vektorD      

def vytvorEtalon(trida):
    delka = len(trida) + 0.0
    #print delka
    soucet = 0
    for obr in trida:
        #print obr
        obraz = udelejObraz(obr)
        #print obraz
        if(soucet == 0):
            soucet = obraz
        else:
            soucet = sectiVektory(soucet,obraz)
    #print soucet
    etalon = vydelVektorCislem(soucet,delka)
    #print"*****"
    #print etalon
    #print"*****"
    return etalon

def readImageDir(path):
    dirs = glob.glob(os.path.join(os.path.normpath(path) ,'*'))
    #print dirs
    labels = []
    files = []
    for onedir in dirs:
        #print onedir
        base, lab = os.path.split(onedir)
        if os.path.isdir(onedir):
            filesInDir = glob.glob(os.path.join(onedir, '*'))
            for onefile in filesInDir:
                labels.append(lab)
                files.append(onefile)
        
    return files, labels        

def trenujObrazy(cast):
    print 'program zahajen'
    files,labels = readImageDir('D:\semestr\obrazy\zdo2014-training\zdo2014-training');
   
    #print delka
    #print labels[10]
    
    files.append(0)# pridani nuly aby se nacetla i posledni trida v poradi
    labels.append(0)
    
    etalony = []
    tridy = []
    
    counter = 0
    ukazatel = 0.0
    kurentni = 0
    trida = [];
    
    delka = len(files)
    #print delka
    for i in files:
        print str(cast) + " + " + str(ukazatel/delka * 100) + " %"
        if(kurentni == 0 or labels[counter]== kurentni):#pokracuje se v dane tride
            trida.append(i)
            kurentni = labels[counter]
            #print "yes"
            #a = True
        else: #nova trida
            #print len(trida)
            tridy.append(kurentni)
            tretina = len(trida)/3
           
            if(cast == 1): # ===ROZDELENI NA CASTI
                trida = trida[tretina+1:len(trida)]
            if(cast == 2):
                trida = trida[0:tretina+1] + trida[2*tretina+1:len(trida)]
            if(cast == 3):
                trida = trida[0:2*tretina+1]
            ''' TESTOVACI MNOZINA
            print tretina
            if(cast == 1): # ===ROZDELENI NA CASTI
                trida = trida[0:tretina+1]
            if(cast == 2):
                trida = trida[tretina+1:2*tretina+1]
            if(cast == 3):
                trida = trida[2*tretina+1:len(trida)]
                
            TESTOVACI MNOZINA'''
            etalon = vytvorEtalon(trida)
            etalony.append(etalon)
            trida = []
            trida.append(i)
            kurentni = labels[counter]
            #print "no"
            #a = False
        #print str(counter) + " " + str(a)
        counter = counter+1
        ukazatel = ukazatel+1
        
    #print(tridy)  
    #print etalony 
    '''MAM TRIDY A ETALONY'''
    zapisTridyaEtalonyDoSouboru(tridy,etalony,cast)
    print'program ukoncen vysledky zapsany do souboru OBR_' + str(cast) + '.txt'

trenujObrazy(1)
trenujObrazy(2)
trenujObrazy(3)