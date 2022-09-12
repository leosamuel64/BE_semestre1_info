# Import des modules
from flask import Flask,render_template,request,redirect,session
from fonctions import *
from flask_session import Session
import os 
import random
from datetime import datetime

# Configuration de Flask
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# ----------------------- VARIABLES GLOBALES -----------------------

NOM_DU_SITE="Yam's"
NOMBRE_LANCER=2
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




# ---------------------------------------------------------------------
# ----------------------- ROUTAGE DES PAGES WEB -----------------------
# ---------------------------------------------------------------------




@app.route ('/')
def index():
    """
    Page d'accueil du site
    """
    if 'user' not in session:
        session['user']=''
    if 'scores' not in session:
        session['scores']=[[0,0,0,0,0,0,0,0,0],
                           [0,0,0],
                           [0,0,0,0,0,0,0]]
        
    if 'figure_bool' not in session:
        session['figure_bool']=[[True,True,True,True,True,True],
                                [True,True],
                                [True,True,True,True,True]]
    return render_template('header_home.html',page_name=NOM_DU_SITE)+render_template('index.html',parties=charger_scores('data/scores.txt'))+render_template('footer.html')


@app.route ('/option_compte.html')
def option_compte():
    """
    Page pour gérer son compte
    """
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Option compte')+render_template('option_compte.html')+render_template('footer.html')


@app.route ('/regles.html')
def regles():
    """
    Page avec les règles
    """
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Règles')+render_template('regles.html',)+render_template('footer.html')


@app.route ('/jouer.html')
def jouer():
    """
    Page de jeu du mode solo
    """
    if ('lancer' not in session) or (session['lancer']==NOMBRE_LANCER):
        session['lancer']=0
    if 'des' not in session:
        l=[random.randint(1,6) for _ in range(5)]
        session['des']=l
        
    session['projection']=[ [un(session['des']),deux(session['des']),trois(session['des']),quatre(session['des']),cinq(session['des']),six(session['des']),0,0,0],
                            [superieur(session['des']),inferieur(session['des']),0],
                            [carre(session['des']),full(session['des']),petite_suite(session['des']),grande_suite(session['des']),yams(session['des']),0,0]]
    
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Solo')+render_template('jouer.html',)+render_template('footer.html')


@app.route ('/jouer_multi.html')
def jouer_multi():
    """
    Page du jeu du mode multijoueur
    """
    if 'mutliplayer' not in session:
        session['multiplayer']=False
        
    if ('lancer' not in session) or (session['lancer']==NOMBRE_LANCER):
        session['lancer']=0
    if 'des' not in session:
        l=[random.randint(1,6) for _ in range(5)]
        session['des']=l
        
    session['projection']=[ [un(session['des']),deux(session['des']),trois(session['des']),quatre(session['des']),cinq(session['des']),six(session['des']),0,0,0],
                            [superieur(session['des']),inferieur(session['des']),0],
                            [carre(session['des']),full(session['des']),petite_suite(session['des']),grande_suite(session['des']),yams(session['des']),0,0]]
    
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Multijoueur')+render_template('jouer_multi.html',)+render_template('footer.html')


@app.route ('/scores.html')
def scores():
    """
    Page avec les scores
    """
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Scores')+render_template('scores.html',parties=charger_scores('data/scores.txt'))+render_template('footer.html')


@app.route ('/connecter.html')
def connection():
    """
    Page de connexion
    """
    return render_template('header_home.html')+render_template('connecter.html',)+render_template('footer.html')




# ---------------------------------------------------------------------
# ----------------------- ROUTAGES INTERACTIONS -----------------------
# ---------------------------------------------------------------------




@app.route ('/remove_user')
def remove_user_db():
    """
    Redirection pour supprimer un compte de la base de données des comptes 
    """
    remove_user(session['user'])
    session['user']=''
    return render_template('header_home.html')+render_template('index.html',parties=charger_scores('data/scores.txt'))+render_template('footer.html')


@app.route ('/change_password',methods = ['GET'])
def change_password():
    """
    Redirection qui modifie le mot de passe d'un utilisateur dans la base de données des comptes 
    """
    result=request.args
    nv_mdp=result['pass']
    log=session["user"]
    changer_password(log,nv_mdp)
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('index.html')+render_template('footer.html')


@app.route ('/deco')
def deco():
    """
    Redirection qui déconnecte l'utilisateur
    """
    session['user']=''
    return redirect('/')
    

@app.route ('/lance_multi',methods = ['GET'])
def lance_multi():
    """
    Redirection qui lance une partie en multijoueur
    """
    
    session['multiplayer']=True
    result=request.args
    txt = result['0']
    nom=txt.split(',')
    session['nom_multi']=nom
    session['nb_joueur_multi']=len(nom)
    
    dico_multi={}
    for i in nom:
        dico_multi[i]=[[[0,0,0,0,0,0,0,0,0],
                        [0,0,0],
                        [0,0,0,0,0,0,0]],
                       [[True,True,True,True,True,True],
                        [True,True],
                        [True,True,True,True,True]]]
        
    session['dico_multi']=dico_multi
    session['tour_multi']=0
    
    session['scores']=session['dico_multi'][session['nom_multi'][session['tour_multi']%session['nb_joueur_multi']]][0]
    session['figure_bool']=session['dico_multi'][session['nom_multi'][session['tour_multi']%session['nb_joueur_multi']]][1]
    session['projection']=[ [un(session['des']),deux(session['des']),trois(session['des']),quatre(session['des']),cinq(session['des']),six(session['des']),0,0,0],
                            [superieur(session['des']),inferieur(session['des']),0],
                            [carre(session['des']),full(session['des']),petite_suite(session['des']),grande_suite(session['des']),yams(session['des']),0,0]]
    
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer_multi.html',)+render_template('footer.html')


@app.route ('/charger_game',methods = ['GET'])
def charger_game_html():
    """
    Redirection qui charge la dernière partie sauvée
    """
    dico=charger_games()
    session['scores'], session['figure_bool']=dico[session['user']]
    session['lancer']=0
    session['fin']=False
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')


@app.route ('/save_game',methods = ['GET'])
def save_game_html():
    """
    Redirection qui sauve la partie en cours
    """
    dico=charger_games()
    
    ecrire_game(dico,session['user'],session['scores'],session['figure_bool'])
    session['in_dico']=True
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')
    

@app.route ('/lancer',methods = ['GET'])
def lancer():
    """
    Redirection qui met à jour la liste des dés en fonction des dés selectionnés (mode solo)
    """
    result=request.args
    session['lancer']+=1
    
    for i in range(5):
        if str(i) in result and session['lancer']<=NOMBRE_LANCER:
            session['des'][i]=random.randint(1,6)
            
    session['projection']=[ [un(session['des']),deux(session['des']),trois(session['des']),quatre(session['des']),cinq(session['des']),six(session['des']),0,0,0],
                            [superieur(session['des']),inferieur(session['des']),0],
                            [carre(session['des']),full(session['des']),petite_suite(session['des']),grande_suite(session['des']),yams(session['des']),0,0]]
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')


@app.route ('/lancer_multi',methods = ['GET'])
def lancer_multi():
    """
    Redirection qui met à jour la liste des dés en fonction des dés selectionnés (mode multi)
    """
    result=request.args
    session['lancer']+=1
    for i in range(5):
        if str(i) in result:
            session['des'][i]=random.randint(1,6)
            
    session['projection']=[ [un(session['des']),deux(session['des']),trois(session['des']),quatre(session['des']),cinq(session['des']),six(session['des']),0,0,0],
                            [superieur(session['des']),inferieur(session['des']),0],
                            [carre(session['des']),full(session['des']),petite_suite(session['des']),grande_suite(session['des']),yams(session['des']),0,0]]
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer_multi.html')+render_template('footer.html')


@app.route ('/reset',methods = ['GET'])
def reset():
    """
    Redirection qui met la partie à zéro (mode solo)
    """
    session['des']=[random.randint(1,6) for _ in range(5)]
    
    session['scores']=[[0,0,0,0,0,0,0,0,0],
                           [0,0,0],
                           [0,0,0,0,0,0,0]]
    session['figure_bool']=[[True,True,True,True,True,True],
                                [True,True],
                                [True,True,True,True,True]]
    session['projection']=[ [un(session['des']),deux(session['des']),trois(session['des']),quatre(session['des']),cinq(session['des']),six(session['des']),0,0,0],
                            [superieur(session['des']),inferieur(session['des']),0],
                            [carre(session['des']),full(session['des']),petite_suite(session['des']),grande_suite(session['des']),yams(session['des']),0,0]]
    
    session['lancer']=0
    session['fin']=False
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')


@app.route ('/reset_multi',methods = ['GET'])
def reset_mutli():
    """
    Redirection qui met la partie à zéro (mode multi)
    """
    session['des']=[random.randint(1,6) for _ in range(5)]
    
    session['scores']=[[0,0,0,0,0,0,0,0,0],
                           [0,0,0],
                           [0,0,0,0,0,0,0]]
    session['figure_bool']=[[True,True,True,True,True,True],
                                [True,True],
                                [True,True,True,True,True]]
    session['lancer']=0
    session['fin']=False
    session['multiplayer']=False
    
    session['projection']=[ [un(session['des']),deux(session['des']),trois(session['des']),quatre(session['des']),cinq(session['des']),six(session['des']),0,0,0],
                            [superieur(session['des']),inferieur(session['des']),0],
                            [carre(session['des']),full(session['des']),petite_suite(session['des']),grande_suite(session['des']),yams(session['des']),0,0]]
    
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer_multi.html')+render_template('footer.html')


@app.route ('/enregistrer',methods = ['GET'])
def maj_score():
    """
    Redirection qui met à jour le score après avoir mis une figure (mode solo)
    """
    if 'scores' not in session:
        session['scores']=[[0,0,0,0,0,0,0,0,0],
                           [0,0,0],
                           [0,0,0,0,0,0,0]]
        
    if 'figure_bool' not in session:
        session['figure_bool']=[[True,True,True,True,True,True],
                                [True,True],
                                [True,True,True,True,True]]
           
    result=request.args
    if result!={}:
        session['lancer']=0
        point=DICO_FONCTIONS[result['figure']](session['des'])
        x,y=DICO_PLACES[result['figure']]
        session['scores'][x][y]=point
        session['figure_bool'][x][y]=False
        session['fin']=verif_fin(session['figure_bool'])
        session['des']=[random.randint(1,6) for _ in range(5)]
        
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
        
        session['projection']=[ [un(session['des']),deux(session['des']),trois(session['des']),quatre(session['des']),cinq(session['des']),six(session['des']),0,0,0],
                            [superieur(session['des']),inferieur(session['des']),0],
                            [carre(session['des']),full(session['des']),petite_suite(session['des']),grande_suite(session['des']),yams(session['des']),0,0]]
    
          
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer.html')+render_template('footer.html')


@app.route ('/enregistrer_multi',methods = ['GET'])
def maj_score_multi():
    """
    Redirection qui met à jour le score après avoir mis une figure (mode mutli)
    """
    if 'scores' not in session:
        session['scores']=[[0,0,0,0,0,0,0,0,0],
                           [0,0,0],
                           [0,0,0,0,0,0,0]]
        
    if 'figure_bool' not in session:
        session['figure_bool']=[[True,True,True,True,True,True],
                                [True,True],
                                [True,True,True,True,True]]
        
    result=request.args
    
    if result!={}:
        session['lancer']=0
        point=DICO_FONCTIONS[result['figure']](session['des'])
        x,y=DICO_PLACES[result['figure']]
        session['scores'][x][y]=point
        session['figure_bool'][x][y]=False
        session['fin']=verif_fin(session['figure_bool'])
        session['des']=[random.randint(1,6) for _ in range(5)]
          
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
        
        session['tour_multi']=session['tour_multi']+1
        
        session['scores']=session['dico_multi'][session['nom_multi'][session['tour_multi']%session['nb_joueur_multi']]][0]
        session['figure_bool']=session['dico_multi'][session['nom_multi'][session['tour_multi']%session['nb_joueur_multi']]][1]
         
         
        session['projection']=[ [un(session['des']),deux(session['des']),trois(session['des']),quatre(session['des']),cinq(session['des']),six(session['des']),0,0,0],
                            [superieur(session['des']),inferieur(session['des']),0],
                            [carre(session['des']),full(session['des']),petite_suite(session['des']),grande_suite(session['des']),yams(session['des']),0,0]]
    
    return render_template('header_home.html',page_name=NOM_DU_SITE+' - Jouer')+render_template('jouer_multi.html')+render_template('footer.html')


@app.route ('/fin_score',methods = ['GET'])
def fin_score():
    """
    Redirection qui ajoute le score dans le tableau des scores
    """
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


@app.route ('/connect',methods = ['POST'])
def connect():
    """
    Redirection qui gère la connexion d'un utilisateur (avec la base de données)
    """   
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




# ---------------------------------------------------------------------
# ---------------------- EXECUTION DU SERVEUR WEB ---------------------
# ---------------------------------------------------------------------




if __name__ == '__main__' :
    app.run(debug = True)
