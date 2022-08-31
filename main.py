# Import des modules
from flask import Flask,render_template,request,redirect,session
from fonctions import *
from flask_session import Session
import os 
import random

# Configuration de Flask
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# ----------------------- FONCTIONS AUXILIAIRES -----------------------



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
                    'total_3':(2,5)  
                }



# ----------------------- ROUTAGE DES PAGES WEB -----------------------

@app.route ('/index.html')
@app.route ('/')
def index():
    return render_template('header_home.html')+render_template('index.html',parties=[["1","Leo",'24/12/2022','32']])+render_template('footer.html')

@app.route ('/regles.html')
def regles():
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Règles')+render_template('regles.html',)+render_template('footer.html')

@app.route ('/jouer.html')
def jouer():
    if ('lancer' not in session) or (session['lancer']==NOMBRE_LANCER):
        session['lancer']=0
    if 'des' not in session:
        l=[random.randint(1,6) for _ in range(5)]
        session['des']=l
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html',)+render_template('footer.html')


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
                           [0,0,0,0,0,0]]
    session['figure_bool']=[[True,True,True,True,True,True,True,True,True],
                                [True,True,True],
                                [True,True,True,True,True,True]]
    session['lancer']=0
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')


@app.route ('/enregistrer',methods = ['GET'])
def maj_score():
    if 'scores' not in session:
        session['scores']=[[0,0,0,0,0,0,0,0,0],
                           [0,0,0],
                           [0,0,0,0,0,0]]
        
    if 'figure_bool' not in session:
        session['figure_bool']=[[True,True,True,True,True,True,True,True,True],
                                [True,True,True],
                                [True,True,True,True,True,True]]
    result=request.args
    session['lancer']=0
    session['des']=[random.randint(1,6) for _ in range(5)]
    point=DICO_FONCTIONS[result['figure']](session['des'])
    x,y=DICO_PLACES[result['figure']]
    session['scores'][x][y]=point
    session['figure_bool'][x][y]=False
    
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
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')



@app.route ('/scores.html')
def scores():
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Scores')+render_template('scores.html',parties=[["1","Leo",'24/12/2022','32']])+render_template('footer.html')




# ----------------------- EXECUTION DU SERVEUR WEB -----------------------

if __name__ == '__main__' :
    app.run(debug = True)