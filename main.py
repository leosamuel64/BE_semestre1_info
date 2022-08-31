# Import des modules
from flask import Flask,render_template,request,redirect,session
from fonctions import *
from flask_session import Session
import os 
import random
from datetime import datetime
import pickle

# Configuration de Flask
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# ----------------------- FONCTIONS AUXILIAIRES -----------------------

def ecrire_game(dico,nom,score,figure_bool, chemin="data/games.txt"):
    dico[nom]=[score,figure_bool]
    with open(chemin, "wb") as fp:   #Pickling
        pickle.dump(dico, fp)
        
def charger_games(chemin="data/games.txt"):
    with open("data/games.txt", "rb") as fp:   # Unpickling
        b = pickle.load(fp)
    return b

def charger_scores(chemin):
    res=[]
    file=open(chemin,'r')
    for ligne in file:
        rank,nom,date,score=ligne.strip().split(',')
        res.append([rank,nom,date,score])
    return res

def ecrire_score(chemin,nom,date,score):
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
    res=True
    for liste in matrice:
        for b in liste:
            if b==True:
                res=False 
    return res 



# ----------------------- VARIABLES GLOBALES -----------------------

NOM_DU_SITE="Yam's"
NOMBRE_LANCER=3
DICO_FONCTIONS={    'un':un,
                    'deux':deux,
                    'trois':trois,
                    'quatre':quatre,
                    'cinq':cinq,
                    'six':six,
                    'sup':superieur,
                    'inf':inferieur,
                    'carre':carre,
                    'full':full,
                    'petite':petite_suite,
                    'grande':grande_suite,
                    'yams':yams        
                }

DICO_PLACES=    {   'un':(0,0),
                    'deux':(0,1),
                    'trois':(0,2),
                    'quatre':(0,3),
                    'cinq':(0,4),
                    'six':(0,5),
                    'sous_total':(0,6),
                    'prime':(0,7),
                    'total_1':(0,8),
                    'sup':(1,0),
                    'inf':(1,1),
                    'total_2':(1,2),
                    'carre':(2,0),
                    'full':(2,1),
                    'petite':(2,2),
                    'grande':(2,3),
                    'yams':(2,4),
                    'total_3':(2,5),
                    'total_final':(2,6)  
                }



# ----------------------- ROUTAGE DES PAGES WEB -----------------------

@app.route ('/')
def index():
    return render_template('header_home.html')+render_template('index.html',parties=charger_scores('data/scores.txt'))+render_template('footer.html')

@app.route ('/regles.html')
def regles():
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Règles')+render_template('regles.html',)+render_template('footer.html')

@app.route ('/jouer.html')
def jouer():
    session['false']=False
    if ('lancer' not in session) or (session['lancer']==NOMBRE_LANCER):
        session['lancer']=0
    if 'des' not in session:
        l=[random.randint(1,6) for _ in range(5)]
        session['des']=l
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html',)+render_template('footer.html')


@app.route ('/charger_game',methods = ['GET'])
def charger_game_html():
    dico=charger_games()
    session['scores'], session['figure_bool']=dico[session['user']]
    session['lancer']=0
    session['fin']=False
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')


@app.route ('/save_game',methods = ['GET'])
def save_game_html():
    dico=charger_games()
    
    ecrire_game(dico,session['user'],session['scores'],session['figure_bool'])
    session['in_dico']=True
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')
    

@app.route ('/lancer',methods = ['GET'])
def lancer():
    result=request.args
    session['lancer']+=1
    for i in range(5):
        if str(i) in result:
        # if True:
            session['des'][i]=random.randint(1,6)
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')

@app.route ('/reset',methods = ['GET'])
def reset():
    session['des']=[random.randint(1,6) for _ in range(5)]
    
    session['scores']=[[0,0,0,0,0,0,0,0,0],
                           [0,0,0],
                           [0,0,0,0,0,0,0]]
    session['figure_bool']=[[True,True,True,True,True,True],
                                [True,True],
                                [True,True,True,True,True]]
    session['lancer']=0
    session['fin']=False
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')


@app.route ('/enregistrer',methods = ['GET'])
def maj_score():
    if 'scores' not in session:
        session['scores']=[[0,0,0,0,0,0,0,0,0],
                           [0,0,0],
                           [0,0,0,0,0,0,0]]
        
    if 'figure_bool' not in session:
        session['figure_bool']=[[True,True,True,True,True,True],
                                [True,True],
                                [True,True,True,True,True]]
        
 
    
    result=request.args
    session['lancer']=0
    session['des']=[random.randint(1,6) for _ in range(5)]
    point=DICO_FONCTIONS[result['figure']](session['des'])
    x,y=DICO_PLACES[result['figure']]
    session['scores'][x][y]=point
    session['figure_bool'][x][y]=False
    session['fin']=verif_fin(session['figure_bool'])
    
    
    x,y=DICO_PLACES['sous_total']
    session['scores'][x][y] = sous_total(session['scores'])
    
    x,y=DICO_PLACES['prime']
    session['scores'][x][y] = prime(session['scores'])
    
    x,y=DICO_PLACES['total_1']
    session['scores'][x][y] = total1(session['scores'])
    
    x,y=DICO_PLACES['total_2']
    session['scores'][x][y] = total2(session['scores'])
    
    x,y=DICO_PLACES['total_3']
    session['scores'][x][y] = total3(session['scores'])
    
    x,y=DICO_PLACES['total_final']
    session['scores'][x][y] = total_final(session['scores'])
    
    
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')



@app.route ('/scores.html')
def scores():
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Scores')+render_template('scores.html',parties=charger_scores('data/scores.txt'))+render_template('footer.html')

@app.route ('/fin_score',methods = ['GET'])
def fin_score():
    name=session['user']
    ecrire_score('data/scores.txt',name,datetime.today().strftime('%Y-%m-%d'),total_final(session['scores']))
    
    session['des']=[random.randint(1,6) for _ in range(5)]
    
    session['scores']=[[0,0,0,0,0,0,0,0,0],
                           [0,0,0],
                           [0,0,0,0,0,0,0]]
    session['figure_bool']=[[True,True,True,True,True,True],
                                [True,True],
                                [True,True,True,True,True]]
    session['lancer']=0
    session['fin']=False
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')

@app.route ('/connecter.html')
def connection():
    return render_template('header_home.html')+render_template('connecter.html',)+render_template('footer.html')

@app.route ('/deco.html')
def deco():
    session['user']=''
    return redirect('/')



@app.route ('/connect',methods = ['POST'])
def connect():   
    if request.form['action'] == 'connect':     
        form_user=request.form['login']
        form_password=request.form['pwd']
        
        stream = os.popen('./hachage '+form_password)
        output = stream.read()
        try:
            if int(output)==int(get_hash(form_user)):
                session['user']=form_user
                session['save_dico']=charger_games()
                if session['user'] in session['save_dico']:
                    session['in_dico']=True
                else:
                    session['in_dico']=False
                return redirect('/')
            else:
                page = """
                    <html>
                        <head>
                            <meta http-equiv="Refresh" content="5; url=/connecter.html" />
                        </head>
                        <body>
                        Mauvais mot de passe ou nom d'utilisateur. Redirection automatique dans 5 secondes
                        </body>
                    </html>
                        """  
                return page
        except:
            page = """
                    <html>
                        <head>
                            <meta http-equiv="Refresh" content="5; url=/connecter.html" />
                        </head>
                        <body>
                        Mauvais mot de passe ou nom d'utilisateur. Redirection automatique dans 5 secondes
                        </body>
                    </html>
                        """  
            return page
    elif request.form['action'] == 'add':
        form_user=request.form['login']
        form_password=request.form['pwd']
        print(existe_deja(form_user))
        if not existe_deja(form_user):
            add_user(form_user,form_password)
        else:
            page = """
                    <html>
                        <head>
                            <meta http-equiv="Refresh" content="5; url=/connecter.html" />
                        </head>
                        <body>
                        L'utilisateur existe déjà. Redirection automatique dans 5 secondes
                        </body>
                    </html>
                        """  
            return page
        return redirect('/connecter.html')


# ----------------------- EXECUTION DU SERVEUR WEB -----------------------

if __name__ == '__main__' :
    app.run(debug = True)