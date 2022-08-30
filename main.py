# Import des modules
from flask import Flask,render_template,request,redirect,session
from fonctions import *
from flask_session import Session
import os 

# Configuration de Flask
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ----------------------- FONCTIONS AUXILIAIRES -----------------------



# ----------------------- VARIABLES GLOBALES -----------------------

NOM_DU_SITE="Yam's"




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
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html',)+render_template('footer.html')

@app.route ('/scores.html')
def scores():
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Scores')+render_template('scores.html',parties=[["1","Leo",'24/12/2022','32']])+render_template('footer.html')




# ----------------------- EXECUTION DU SERVEUR WEB -----------------------

if __name__ == '__main__' :
    app.run(debug = True)