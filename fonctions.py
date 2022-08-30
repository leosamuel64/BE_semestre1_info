from regex import F


def convert_int(m):
    res=''
    for lettre in m:
        try:
            int(lettre)
            res+=lettre
        except:
            ()
    return int(res)

def liste_aeroport():
    res=[]
    f=open('data/airports.txt')
    for ligne in f:
        t = ligne.split()
        temp=t[0]+'-'
        for i in range(3,len(t)):
            temp+=t[i]+' '
        res.append([t[0],temp[0:len(temp)-1]])

    return res

import sqlite3
import os


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
    
    

  
        