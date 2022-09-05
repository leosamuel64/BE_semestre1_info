import sqlite3
import os
import pickle




# ---------------------------------------------------------------------
# ----------------- FONCTIONS POUR COMPTER LES POINTS -----------------
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
    res=0
    for i in dés:
        if i==2:
            res+=2
    print(dés,res)
    return res


def trois(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    res=0
    for i in dés:
        if i==3:
            res+=3
    return res


def quatre(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    res=0
    for i in dés:
        if i==4:
            res+=4
    return res


def cinq(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    res=0
    for i in dés:
        if i==5:
            res+=5
    return res


def six(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    res=0
    for i in dés:
        if i==6:
            res+=6
    return res


def superieur(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return sum(dés)


def inferieur(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    return sum(dés)


def carre(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    res=0
    for i in dés:
        if dés.count(i)>=4:
            res=40+sum(dés)
    return res


def full(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    res=0
    for i in dés:
        if dés.count(i)==3:
            for a in dés :
                if dés.count(a)==2:
                    res=30+sum(dés)
    return res


def petite_suite(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    res=True
    sans_doubles_liste=sans_doubles(dés)
    if len(sans_doubles_liste)!=4:
        return 0
    else:
        for i in range(0,3):
            if sans_doubles_liste[i]!=sans_doubles_liste[i+1]-1:
                res=False
    return res*45

def grande_suite(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    res=True
    dés.sort()
    for i in range(0,4):
        if dés[i]!=dés[i+1]-1:
            res=False
    return int(res)*50


def yams(dés):
    """
    Entrée : dés - Liste des numéro des dés ([1,2,3,2,3])
    Sortie : point - Entier qui indique le nombre de point associé à la liste des dés
    """
    res=0
    for i in dés:
        if dés.count(i)==5:
            res=50+sum(dés)
    return res




# ---------------------------------------------------------------------
# --------------------- FONCTIONS POUR LES TOTAUX ---------------------
# ---------------------------------------------------------------------




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




# ---------------------------------------------------------------------
# -------------------------- AUTRES FONCTIONS -------------------------
# ---------------------------------------------------------------------




def sans_doubles(dés):
    """
    Renvoie la liste sans double et trié
    """
    dico={i:0 for i in range(1,7) }
    for i in dés:
        dico[i]+=1  
    res=[i for i in range(1,7) if dico[i]!=0]
    return res


def add_user(login,password):
    """
    Ajoute un utilisateur dans la base de données SQL
    """
    stream = os.popen('./hachage '+password)
    hash_txt = stream.read()
    
    connection = sqlite3.connect('data/database.db')
    
    request='''
    INSERT INTO users (login,hash)
       VALUES ("'''+login+'", '+hash_txt+')'
       
    connection.execute(request)
    connection.commit()
    connection.close()
    
    
def remove_user(login):
    """
    Enlève un utilisateur dans la base de données SQL
    """
    connection = sqlite3.connect('data/database.db')
    
    request="""
    DELETE from users
        where login='"""+login+"'"
       
    connection.execute(request)
    connection.commit()
    connection.close()
    
def changer_password(login,password):
    """
    Change le mot de passe dans la base de données SQL
    """
    stream = os.popen('./hachage '+password)
    hash = stream.read()
    connection = sqlite3.connect('data/database.db')
    
    request="""
    DELETE from users
        where login='"""+login+"'"
       
    connection.execute(request)
    connection.commit()
    
    request='''
    INSERT INTO users (login,hash)
       VALUES ("'''+login+'", '+hash+')'
       
    cursor = connection.execute(request)
    connection.commit()
    connection.close()
      
def existe_deja(login):
    """
    Indique si un utilisateur existe déjà
    """
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
    """
    Indique le hash du mot de passe associé à un login
    La fonction hash à la signature : hash : login (str) |-> hash (int) 
    La fonction de hash n'est pas bijective car Card(ensemble_login)>Card(ensemble_hash) ((MD5))
    """
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


def ecrire_game(dico,nom,score,figure_bool, chemin="data/games.txt"):
    """
    Sauvegarde le dico des parties dans un fichier texte
    """
    dico[nom]=[score,figure_bool]
    with open(chemin, "wb") as fp:
        pickle.dump(dico, fp)
     
        
def charger_games(chemin="data/games.txt"):
    """
    Renvoie le dico des parties du fichier texte de sauvegarde
    """
    with open("data/games.txt", "rb") as fp:   # Unpickling
        b = pickle.load(fp)
    return b


def charger_scores(chemin):
    """
    Renvoie la liste des scores enregistrer
    """
    res=[]
    file=open(chemin,'r')
    for ligne in file:
        rank,nom,date,score=ligne.strip().split(',')
        res.append([rank,nom,date,score])
    return res


def ecrire_score(chemin,nom,date,score):
    """
    Ajouter un nouveau score dans le fichier de sauvegarde et le classe à la bonne position
    """
    liste=charger_scores(chemin)
    liste.append([0,nom,date,score])
    
    sous_liste=[[int(scoreL),nomL,dateL] for (_,nomL,dateL,scoreL) in liste]
    sous_liste.sort(reverse=True)
    
    file=open(chemin,'w')
    i=1
    for ligne in sous_liste:
        s,n,d=ligne
        file.write(str(i)+','+str(n)+','+str(d)+','+str(s)+'\n')
        i+=1
    file.close()
    
        
def verif_fin(matrice):
    """
    Indique si toutes les figures ont été traitées
    """
    res=True
    for liste in matrice:
        for b in liste:
            if b==True:
                res=False 
    return res 
