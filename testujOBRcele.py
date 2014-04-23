'''
Created on 8. 4. 2014
VAROVANI - BEZI DLOUHO
Program pro otestovani dane mnoziny. Vyzaduje soubory "OBR_1.txt","OBR_2.txt","OBR_3.txt". Ty lze ziskat spusteninm programu
"trenujOBR3.py". Vysledky zapise do souboru "OBR_vysledky.txt".
 Adresar je v programu (natvrdo) dany:
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
import scipy

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


def dejVzdalenost(seznam1,seznam2):
    vektor1 = numpy.asarray(seznam1)
    vektor2 = numpy.asarray(seznam2)
    cislo = numpy.linalg.norm(vektor1-vektor2)
    return cislo

def zapisPole(pole,soubor):
    for x in pole:
        soubor.write(str(x) + ' ')
    return

def  zapisVysledkyUspesnosti(labels,vektorUspesnosti):
    soubor = open('OBR_vysledkyCELE.txt','w')
    zapisPole(labels,soubor)
    soubor.write("\n")
    zapisPole(vektorUspesnosti,soubor)
    soubor.write("\n")
    suma = 0.0
    for i in vektorUspesnosti:
        suma = suma+i
    prumer = suma / len(vektorUspesnosti)
    soubor.write("Prumerna uspesnost je " + str(prumer))
    print ("Prumerna uspesnost je " + str(prumer))
    return

def otestujRGBtridu(trida,tridy,etalony,spravne):
    #trida = testovane obrazy
    #tridy = pole se str nazvy natrenovanych Trid 
    #etalon = etaloyn nalezejici tridam
    #spravne = str spravne tridy
    uspesne = 0.0;
    #delka = len(trida)
    
    
    for obr in trida:
        obrazUI = udelejObraz(obr)
        poleVzdalenosti = []
        pozice = 0
        for etalon in etalony:
            #print etalon
            #print obrazUI
            eukleidovskaVzdalenost = dejVzdalenost(etalon,obrazUI)           
            poleVzdalenosti.append(eukleidovskaVzdalenost)
            pozice = pozice+1
        #mam pole vzdalenosti pro dany obraz
        index,hodnota = vyberMinPole(poleVzdalenosti)
        vybrana = tridy[index]
        #print poleVzdalenosti
        if(vybrana == spravne):
            #print vybrana + " urceno spravne"
            uspesne = uspesne+1.0
        #else:
            #print("spravne je " + spravne + " klasifikatorem urceno: " + vybrana)
            
        
    #print uspesne
    return uspesne
 
def vyberMinPole(pole):
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

def nactiTridyEtalonyZeSouboru(nazev):
    soubor = open(nazev,'r')
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

def otestuj():
    print 'program zahajen'
    
    
    
    
    files,labels = readImageDir('D:\semestr\obrazy\zdo2014-training\zdo2014-training');
    tridy1,etalony1 = nactiTridyEtalonyZeSouboru('OBRcely.txt')
    tridy2,etalony2 = nactiTridyEtalonyZeSouboru('OBRcely.txt')
    tridy3,etalony3 = nactiTridyEtalonyZeSouboru('OBRcely.txt')
    
    files.append(0)# pridani nuly aby se nacetla i posledni trida v poradi
    labels.append(0)
    
    vektorUspesnosti = []
    
    counter = 0
    ukazatel = 0.0
    kurentni = 0
    trida = [];
    vysledne = []
    #print delka
    for i in files:
        #print str(ukazatel/delka * 100) + " %"
        if(kurentni == 0 or labels[counter]== kurentni):#pokracuje se v dane tride
            trida.append(i)
            kurentni = labels[counter]
            #print "yes"
            #a = True
        else: #nova trida
            #print len(trida)
            tretina = len(trida)/3
            
            
            trida1 = trida[0:tretina+1]            
            trida2 = trida[tretina+1:2*tretina+1]            
            trida3 = trida[2*tretina+1:len(trida)]
            spravne = labels[counter-1] #prave nactena trida, zmeni se pozdeji
            vysledne.append(spravne)
            print("testuji: " + spravne)
            
            
            uspesnost1 = otestujRGBtridu(trida1,tridy1,etalony1,spravne)
            
            uspesnost2 = otestujRGBtridu(trida2,tridy2,etalony2,spravne)
    
            uspesnost3 = otestujRGBtridu(trida3,tridy3,etalony3,spravne)
            
            uspesne = 0.0+uspesnost1+uspesnost2+uspesnost3
            podil = uspesne/len(trida)
            print podil
            vektorUspesnosti.append(podil)
            
            trida = []
            trida.append(i)
            kurentni = labels[counter]
            #print "no"
            #a = False
        #print str(counter) + " " + str(a)
        counter = counter+1
        ukazatel = ukazatel+1
    #print vysledne
    zapisVysledkyUspesnosti(vysledne,vektorUspesnosti)
    
    
#start = time.time()  
otestuj() 
#konec = time.time()
#print konec - start    