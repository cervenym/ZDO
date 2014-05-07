'''
Created on 9. 4. 2014
Demo pro semestralni praci ze ZDO. Vyzaduje obrazek "demoZnacka.jpg". Ukazuje cely algoritmus, obrazek lze samozrejme vymenit za 
jiny.
@author: cervenym
'''
import glob
import os
import cv2
import skimage.filter
import numpy
import matplotlib.pyplot as plt
import time
import skimage.morphology
import scipy

def eukleidovskaVzdalenost(vektor1,vektor2):  
    vzdalenost = 0.0
    poz = 0
    for x in vektor1:
        y = vektor2[poz]
        vzdalenost = vzdalenost + float(x)-float(y)**2
        poz = poz+1
    vysledek = numpy.sqrt(vzdalenost)  
    return vysledek

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

def vyberZelenou(huehue,saturace,value): #VYBERE I PONEKUD MODROU ZELENOU - POUZITA NA ZNACKACH MA PRIMES MODRE
    TF2 = huehue >=38
    TF1 = huehue <=100
        
    TF = TF1*TF2 + 0
    kernel_big = skimage.morphology.diamond(1)
    TF = skimage.morphology.binary_opening(TF, kernel_big) # OTEVRENI
    TF = cv2.GaussianBlur(TF,(5,5), 5) #GAUSSOVSKA FILTRACE PODRUHE
    return TF

def vyberHrany(cernobily): #CHYBELO
    kernel_big = skimage.morphology.diamond(1)
    TF = cv2.Canny(cernobily,50,50)
    #plt.imshow(TF)
    #plt.show()
    
    TF = skimage.morphology.binary_dilation(TF, kernel_big) # DILATACE
    TF = cv2.GaussianBlur(TF,(5,5), 5) #GAUSSOVSKA FILTRACE PODRUHE
    return TF

def vyberSymbol(cernobily,cervena): #CHYBELO TAKE
    kernel_big = skimage.morphology.rectangle(1,1)
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

def zvyseniKontrastu(im):
    im2 = numpy.empty(im.shape, dtype = 'float32')
    
    for i in range(im.shape[0]):    
        for j in range(im.shape[1]):    
            im2[i,j] = 0.8 * im[i,j] +100
            if im2[i,j] > 255:    
                im2[i,j] = 255    
            if im2[i,j] < 0:    
                im2[i,j] = 0
    return im2


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

def dejVzdalenost(seznam1,seznam2):
    vektor1 = numpy.asarray(seznam1)
    vektor2 = numpy.asarray(seznam2)
    cislo = numpy.linalg.norm(vektor1-vektor2)
    return cislo

jabko= cv2.imread('demoZnacka.jpg', cv2.CV_LOAD_IMAGE_COLOR)
vektor = udelejObraz('demoZnacka.jpg')
#jabko= cv2.imread('aha.jpg', cv2.CV_LOAD_IMAGE_COLOR)
start = time.time()
jabkoRGB = cv2.cvtColor(jabko,cv2.COLOR_BGR2RGB)


print"========"
print"puvodni obrazek"

plt.imshow(jabkoRGB)
delkax = len(jabkoRGB[0,:])
delkay =  len(jabkoRGB[:,0])
plt.title('puvodni obrazek ' + str(delkax) + ":" + str(delkay))
plt.show()


x = cv2.resize(jabko,(100,100)  ,interpolation=cv2.INTER_LINEAR) #NORMALIZACE BILINEARNI TRANSFORMACE
filtrovanejabko = cv2.GaussianBlur(x,(5,5), 5) #GAUSSOVSKA FILTRACE

y = cv2.resize(jabkoRGB,(100,100)  ,interpolation=cv2.INTER_LINEAR) # V RGB MISTO BGR ABY TO BYLO HEZKY VIDET
jy = cv2.GaussianBlur(y,(5,5), 5) 

maska = cv2.getGaussianKernel(5,5)
print"========"
print"Obrazek po normalizaci na velikost 100:100 pixelu a gaussovske filtraci nasledujicim jadrem:"
print maska

plt.title('obrazek po zmene velikosti a gaussovske filtraci 100:100')
plt.imshow(jy)
plt.show()


prebarveny = cv2.cvtColor(filtrovanejabko,cv2.COLOR_BGR2HSV) #PREVEDENI NA HSV
cernobily = cv2.cvtColor(filtrovanejabko,cv2.COLOR_BGR2GRAY) #PREVEDENI NA HSV

huehue =  prebarveny[:,:,0] 
saturace = prebarveny[:,:,1] 
value = prebarveny[:,:,2] 

print"========"
print"Obrazek po prevedeni na barevny model HSV"

a = plt.figure(figsize = (9,4))
plt.subplot(111)
plt.suptitle('obrazek v HSV')
plt.subplot(131)
plt.imshow(huehue,plt.gray())
plt.title('Hue')
plt.subplot(132)
plt.imshow(saturace,plt.gray())
plt.title('Saturation')
plt.subplot(133)
plt.imshow(value,plt.gray())
plt.title('Value')
plt.show()

TFcervena = vyberCervenou(huehue,saturace,value)
TFmodra = vyberModrou(huehue,saturace,value)
TFzluta = vyberZlutou(huehue,saturace,value)
TFbila = vyberBilou(huehue,saturace,value)
TFzelena= vyberZelenou(huehue,saturace,value)
TFhrany= vyberHrany(cernobily)
TFhrany= vyberHrany(cernobily)
TFsymbol = vyberSymbol(TFbila,TFcervena)

TF1 = huehue <=179 #cervena1
TF2 = huehue >=160 #cervena2

TF4 = huehue <= 22 #oranzova
TF3 = saturace >=90# TMAVA ORANZOVA 
oranzova = (TF4*TF3)
cervena = (TF1*TF2)
TF = (TF1*TF2)+(TF4*TF3) + 0
kernel_big = skimage.morphology.diamond(1)
TF = skimage.morphology.binary_opening(TF, kernel_big) # OTEVRENI
TF = cv2.GaussianBlur(TF,(5,5), 5) #GAUSSOVSKA FILTRACE PODRUHE

#print "ukazka masky pro cervenou:"
#print kernel_big
#print

print"========"
print"Ukazka vybrani barevnych slozek z obrazu, v tomto pripade:"
print"cervena = ruda (hue 160-179)+oranzova (hue <22 and saturace >90):"
print "na soucet je pote jeste aplikovano binarni otevreni nasledujicim jadrem:"
print kernel_big
print "a gaussovska filtrace stejnym jadrem jako uz bylo pouzito"

a = plt.figure(figsize = (9,3))
plt.suptitle('vybrani cervene')
plt.subplot(131)
plt.imshow(cervena,plt.gray())
plt.title('ruda')
plt.subplot(132)
plt.imshow(oranzova,plt.gray())
plt.title('oranzova')
plt.subplot(133)
plt.imshow(TF,plt.gray())
plt.title(' otevrena a filtrovana cervena')
plt.show()

print"========"
print"Ukazka Ferretovych prumetu pro cervenou slozku. Z techto prumetu je posleze"
print"sestaven obrazovy vektor dane znacky. "
print"Jelikoz je obrazek normalizovany na velikost 100:100 ma kazdy prumet 100 hodnot, dohromady ma kazda slozka 200 hodnot "

figurka = plt.figure(figsize = (9,9))
plt.suptitle('cervena = ruda+oranzova')
ax = figurka.add_subplot(2,2,1)
ax.imshow(TF,plt.gray())
plt.title('cervena')
ax = figurka.add_subplot(2,2,2)
ax.plot(prumetY(TFcervena))
plt.title('prumet osy Y')
ax = figurka.add_subplot(2,2,3)
ax.plot(prumetX(TFcervena))
plt.title('prumet osy X')
plt.show()
ukazka = prumetX(TFcervena)

#print "Ukazka prvnich deseti hodnot obrazu: " + str(ukazka[1:10])

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

print"========"
print"Vsechny slozky obrazu"
print"Kazda slozka ma 200 hodnot, slozek je 7, celkova delka vektoru priznaku = 1400."
print vektor
print len(vektor)

b = plt.figure(figsize = (13,2))
plt.suptitle('Ukazka vsech barevnych slozek')
plt.subplot(181)
plt.imshow(TFcervena,plt.gray())
plt.title('cervena')
plt.subplot(182)
plt.imshow(TFmodra,plt.gray())
plt.title('modra')
plt.subplot(183)
plt.imshow(TFzluta,plt.gray())
plt.title('zluta')
plt.subplot(184)
plt.imshow(TFbila,plt.gray())
plt.title('bila')
plt.subplot(185)
plt.imshow(TFzelena,plt.gray())
plt.title('zelena')
plt.subplot(186)
plt.imshow(TFhrany,plt.gray())
plt.title('hrany')
plt.subplot(187)
plt.imshow(TFsymbol,plt.gray())
plt.title('symbol')
plt.subplot(188)
plt.imshow(jabkoRGB)
plt.title('puvodni')
plt.show()

print"========"
print"Slozky jsou vicemene vybrany podobne jako cervena, jen s jinymi parametry. Vyjimky tvori slozky hrany a symbol"
print"hrany:"
print"Jsou ziskany pomoci Cannyho hranoveho detektoru a je na ne misto otevreni aplikovana pouze dilatace"
print"symbol:"
print"Jedna se o bilou slozku uvnitr cerveneho uzavreneho utvaru, ziskano logickymi operacemi za pomoci vyplneni der"
print"u slozky cervena. Oduvodneni je zlepseni klasifikace znacek lisicich se pouze cernym symbolem, pro necervene znacky "
print"je nulova "

print"========"
print"Pouzity klasifikator:"
print"Nejblizsi soused, vlastni implementace. Z cele tridy se vypocte prumer tez vzor tridy, "
print"a neznamemu obrazu je prirazena trida, k jejimuz vzoru ma nejmensi eukleidovskou vzdalenost.  "
