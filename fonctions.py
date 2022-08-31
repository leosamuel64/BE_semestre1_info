import sqlite3
import os


# ---------------------------------------------------------------------
# --------------------- FONCTION POUR COMPTER LES POINTS ---------------------
# ---------------------------------------------------------------------




def un(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    res=0
    for i in dés:
        if i==1:
            res+=1
    print(dés,res)
    return res

def deux(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return 1

def trois(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return 1

def quatre(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return 1

def cinq(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return 1

def six(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return 1

def superieur(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return 1

def inferieur(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return 1

def carre(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return 1

def full(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return 1

def petite_suite(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return 1

def grande_suite(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return 1

def yams(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return 1




# ---------------------------------------------------------------------
# --------------------- FONCTIONS POUR LES TOTAUX ---------------------
# ---------------------------------------------------------------------


"""
La feuille des score est une liste de liste :
[   [un,deux,trois,quatre,cinq,six,sous_total,prime,total1],
    [Supérieur, Inférieur, total2],
    [Carré,Full,petite_suite,grande_suite,yams,total3]    
]

"""

def sous_total(score):
    """
    Entrée : score - Liste des scores
    Sortie : entier qui indique le total
    """
    res=0
    for i in range(0,6):
        res+=score[0][i]
    return res

def prime(score):
    """
    Entrée : score - Liste des scores
    Sortie : entier qui indique le total de la prime
    """
    if score[0][6]>=60:
        res=30
    else:
        res=0
    return res

def total1(score):
    """
    Entrée : score - Liste des scores
    Sortie : entier qui indique le total
    """
    return score[0][6]+score[0][7]

def total2(score):
    """
    Entrée : score - Liste des scores
    Sortie : entier qui indique le total
    """
    res=(score[1][0]-score[1][1])*score[0][0]
    if res>0:
        return res
    else:
        return 0

def total3(score):
    """
    Entrée : score - Liste des scores
    Sortie : entier qui indique le total
    """
    res=0
    for i in range(0,5):
        res+=score[2][i]
    return res

def total_final(score):
    """
    Entrée : score - Liste des scores
    Sortie : entier qui indique le total
    """
    
    return score[0][-1]+score[1][-1]+score[2][-2]


def add_user(login,password):
    stream = os.popen('./hachage '+password)
    hash = stream.read()
    connection = sqlite3.connect('data/database.db')
    
    request='''
    INSERT INTO users (login,hash)
       VALUES ("'''+login+'", '+hash+')'
       
    cursor = connection.execute(request)
    connection.commit()
    connection.close()
    
def existe_deja(login):
    request="""
    SELECT login from users
        where login='"""+login+"'"
    
    connection = sqlite3.connect('data/database.db')
    cursor = connection.execute(request)
    
    res=False
    for _ in cursor:
        res=True
    
    connection.commit()
    connection.close()
    return res

def get_hash(login):
    connection = sqlite3.connect('data/database.db')
    request='''
               SELECT hash FROM users
                WHERE login="'''+login+'"'
    cursor = connection.execute(request)
    for x in cursor:
        hash=x[0]
    
    connection.commit()
    connection.close()
    return hash