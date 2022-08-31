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
    for i in range(5):
        if str(i) in result:
            session['des'][i]=random.randint(1,6)
            
            
    
    
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')


@app.route ('/scores.html')
def scores():
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Scores')+render_template('scores.html',parties=[["1","Leo",'24/12/2022','32']])+render_template('footer.html')




# ----------------------- EXECUTION DU SERVEUR WEB -----------------------

if __name__ == '__main__' :
    app.run(debug = True)