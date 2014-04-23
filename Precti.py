'''
Created on 16. 4. 2014

@author: cervenym
'''
def nactiVysledky():
    soubor = open('OBR_vysledky.txt','r')
    radky = soubor.readlines()
    prva = radky[0]
    druha = radky[1]
    treti = radky[2]
    print treti
    
    prva = prva.strip()
    prva = prva.split()
    druha = druha.strip()
    druha = druha.split()
    
    counter = 0
    for x in prva:
        print x
        print druha[counter]
        counter = counter+1

    return prva,druha

nactiVysledky()