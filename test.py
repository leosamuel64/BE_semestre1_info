from random import random
import random


def sans_doubles(dés):
    """
    Renvoie la liste sans double et trié
    """
    dico={i:0 for i in range(1,7) }
    for i in dés:
        dico[i]+=1  
    res=[i for i in range(1,7) if dico[i]!=0]
    return res



def petite_suite(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    res=True
    sans_doubles_liste=sans_doubles(dés)
    if len(sans_doubles_liste)!=4:
        return False*0
    else:
        for i in range(0,3):
            if sans_doubles_liste[i]!=sans_doubles_liste[i+1]-1:
                res=False
    return res*45
        

print(petite_suite([1,2,2,4,3]))