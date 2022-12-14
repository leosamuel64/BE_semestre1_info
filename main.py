# Import des modules
from flask import Flask, render_template, request, redirect, session
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


# ------------------------------------------------------------------
# ----------------------- VARIABLES GLOBALES -----------------------
# ------------------------------------------------------------------


NOM_DU_SITE = "Yam's"

NOMBRE_LANCER = 2

DICO_FONCTIONS = {'un': un,
                  'deux': deux,
                  'trois': trois,
                  'quatre': quatre,
                  'cinq': cinq,
                  'six': six,
                  'sup': superieur,
                  'inf': inferieur,
                  'carre': carre,
                  'full': full,
                  'petite': petite_suite,
                  'grande': grande_suite,
                  'yams': yams
                  }

DICO_PLACES = {'un': (0, 0),
               'deux': (0, 1),
               'trois': (0, 2),
               'quatre': (0, 3),
               'cinq': (0, 4),
               'six': (0, 5),
               'sous_total': (0, 6),
               'prime': (0, 7),
               'total_1': (0, 8),
               'sup': (1, 0),
               'inf': (1, 1),
               'total_2': (1, 2),
               'carre': (2, 0),
               'full': (2, 1),
               'petite': (2, 2),
               'grande': (2, 3),
               'yams': (2, 4),
               'total_3': (2, 5),
               'total_final': (2, 6)
               }


# ---------------------------------------------------------------------
# ----------------------- ROUTAGE DES PAGES WEB -----------------------
# ---------------------------------------------------------------------


@app.route('/')
def index():
    """
    Page d'accueil du site
    """
    session['connected'] = read_connected()
    if 'user' not in session:
        session['user'] = ''
    if 'scores' not in session:
        session['scores'] = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0]]

    if 'figure_bool' not in session:
        session['figure_bool'] = [[True, True, True, True, True, True],
                                  [True, True],
                                  [True, True, True, True, True]]
    session['dice_img'] = {1: "one", 2: "two",
                           3: 'three', 4: "four", 5: "five", 6: "six"}
    return render_template('header_home.html', page_name=NOM_DU_SITE)+render_template('index.html', parties=charger_scores('data/scores.txt'))+render_template('footer.html')


@app.route('/option_compte.html')
def option_compte():
    """
    Page pour g??rer son compte
    """
    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Option compte')+render_template('option_compte.html')+render_template('footer.html')


@app.route('/regles.html')
def regles():
    """
    Page avec les r??gles
    """
    return render_template('header_home.html', page_name=NOM_DU_SITE+' - R??gles')+render_template('regles.html',)+render_template('footer.html')


@app.route('/jouer.html')
def jouer():
    """
    Page de jeu du mode solo
    """
    if ('lancer' not in session) or (session['lancer'] == NOMBRE_LANCER):
        session['lancer'] = 0
    if 'des' not in session:
        l = [random.randint(1, 6) for _ in range(5)]
        session['des'] = l

    session['projection'] = [[un(session['des']), deux(session['des']), trois(session['des']), quatre(session['des']), cinq(session['des']), six(session['des']), 0, 0, 0],
                             [superieur(session['des']),
                              inferieur(session['des']), 0],
                             [carre(session['des']), full(session['des']), petite_suite(session['des']), grande_suite(session['des']), yams(session['des']), 0, 0]]

    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Solo')+render_template('jouer.html',)+render_template('footer.html')


@app.route('/jouer_multi.html')
def jouer_multi():
    """
    Page du jeu du mode multijoueur
    """
    if 'mutliplayer' not in session:
        session['multiplayer'] = False

    if ('lancer' not in session) or (session['lancer'] == NOMBRE_LANCER):
        session['lancer'] = 0
    if 'des' not in session:
        l = [random.randint(1, 6) for _ in range(5)]
        session['des'] = l

    session['projection'] = [[un(session['des']), deux(session['des']), trois(session['des']), quatre(session['des']), cinq(session['des']), six(session['des']), 0, 0, 0],
                             [superieur(session['des']),
                              inferieur(session['des']), 0],
                             [carre(session['des']), full(session['des']), petite_suite(session['des']), grande_suite(session['des']), yams(session['des']), 0, 0]]

    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Local')+render_template('jouer_multi.html',)+render_template('footer.html')


@app.route('/lan.html')
def jouer_lan():
    """
    Page du jeu du mode multijoueur
    """
    if 'mutliplayer' not in session:
        session['multiplayer'] = False

    if ('lancer' not in session) or (session['lancer'] == NOMBRE_LANCER):
        session['lancer'] = 0

    if 'des' not in session:
        l = [random.randint(1, 6) for _ in range(5)]
        session['des'] = l

    session['projection'] = [[un(session['des']), deux(session['des']), trois(session['des']), quatre(session['des']), cinq(session['des']), six(session['des']), 0, 0, 0],
                             [superieur(session['des']),
                              inferieur(session['des']), 0],
                             [carre(session['des']), full(session['des']), petite_suite(session['des']), grande_suite(session['des']), yams(session['des']), 0, 0]]

    dico = charger_games(chemin='data/lan.txt')
    session['lan'] = dico
    session['multiplayer'] = True

    return render_template('header_home.html', page_name=NOM_DU_SITE+' - En ligne')+render_template('lan.html',)+render_template('footer.html')


@app.route('/scores.html')
def scores():
    """
    Page avec les scores
    """
    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Scores')+render_template('scores.html', parties=charger_scores('data/scores.txt'))+render_template('footer.html')


@app.route('/connecter.html')
def connection():
    """
    Page de connexion
    """
    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Se connecter')+render_template('connecter.html',)+render_template('footer.html')


@app.route('/chat.html')
def chat():
    """
    Page du chat
    """
    l = read_chat()
    l.reverse()
    session['chat'] = l
    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Chat')+render_template('chat.html',)+render_template('footer.html')


@app.route('/nv_compte.html')
def nv_compte():
    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Nouveau compte')+render_template('nv_compte.html',)+render_template('footer.html')


# ---------------------------------------------------------------------
# ----------------------- ROUTAGES INTERACTIONS -----------------------
# ---------------------------------------------------------------------


@app.route('/remove_user')
def remove_user_db():
    """
    Redirection pour supprimer un compte de la base de donn??es des comptes 
    """
    remove_user(session['user'])
    session['user'] = ''
    return redirect('/')


@app.route('/change_password', methods=['POST'])
def change_password():
    """
    Redirection qui modifie le mot de passe d'un utilisateur dans la base de donn??es des comptes 
    """
    result = request.form
    nv_mdp = result['pass']
    log = session["user"]
    changer_password(log, nv_mdp)
    return redirect('/')


@app.route('/change_photo', methods=['GET'])
def change_photo():
    result = request.args
    session['photo'] = result['photo']
    f = open('data/photos.txt', 'r')
    photo = {}
    for ligne in f:
        nom, image = ligne.strip().split(';')
        photo[nom] = image
    photo[session['user']] = result['photo']
    f.close()
    f = open('data/photos.txt', 'w')
    for cl?? in photo.keys():
        f.write(cl??+';'+photo[cl??]+'\n')
    f.close()
    return redirect('/')


@app.route('/deco')
def deco():
    """
    Redirection qui d??connecte l'utilisateur
    """
    enleve_connected(session['user'])
    session['multiplayer'] = False
    session['user'] = ''

    return redirect('/')


@app.route('/lance_multi', methods=['GET'])
def lance_multi():
    """
    Redirection qui lance une partie en multijoueur
    """
    session['multiplayer'] = True
    result = request.args
    txt = result['0']
    nom = txt.split(',')
    session['nom_multi'] = nom
    session['nb_joueur_multi'] = len(nom)

    dico_multi = {}
    for i in nom:
        dico_multi[i] = [[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0]],
                         [[True, True, True, True, True, True],
                          [True, True],
                          [True, True, True, True, True]]]

    session['dico_multi'] = dico_multi
    session['tour_multi'] = 0

    session['scores'] = session['dico_multi'][session['nom_multi']
                                              [session['tour_multi'] % session['nb_joueur_multi']]][0]
    session['figure_bool'] = session['dico_multi'][session['nom_multi']
                                                   [session['tour_multi'] % session['nb_joueur_multi']]][1]
    session['projection'] = [[un(session['des']), deux(session['des']), trois(session['des']), quatre(session['des']), cinq(session['des']), six(session['des']), 0, 0, 0],
                             [superieur(session['des']),
                              inferieur(session['des']), 0],
                             [carre(session['des']), full(session['des']), petite_suite(session['des']), grande_suite(session['des']), yams(session['des']), 0, 0]]

    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Local')+render_template('jouer_multi.html',)+render_template('footer.html')


@app.route('/charger_game', methods=['GET'])
def charger_game_html():
    """
    Redirection qui charge la derni??re partie sauv??e
    """
    dico = charger_games()
    session['scores'], session['figure_bool'] = dico[session['user']]
    session['fin'] = False
    session['des'] = [random.randint(1, 6) for _ in range(5)]
    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Solo')+render_template('jouer.html')+render_template('footer.html')


@app.route('/join_lan', methods=['GET'])
def join_lan():
    """
    Redirection qui permet de rejoindre une partie ne ligne avec un code session
    """
    session['multiplayer'] = True
    result = request.args
    id_game = result['0']

    session['id_lan'] = int(id_game)
    session['fin'] = False
    return redirect('lan.html')


@app.route('/lance_lan', methods=['GET'])
def lance_lan():
    """
    Redirection qui cr??er une partie en ligne (cr??ation de la partie et d'un code session)
    """
    session['multiplayer'] = True

    dico = charger_games(chemin='data/lan.txt')
    result = request.args
    j1 = result['0']
    j2 = result['1']

    id_game = dico['last_id']+1
    dico['last_id'] = id_game
    dico[id_game] = [0,
                     [j1, j2],
                     [[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]],         [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                       [0, 0, 0],
                                                       [0, 0, 0, 0, 0, 0, 0]]],
                     [[[True, True, True, True, True, True],
                       [True, True],
                       [True, True, True, True, True]],       [[True, True, True, True, True, True],
                                                               [True, True],
                                                               [True, True, True, True, True]]],
                     [random.randint(1, 6) for _ in range(5)]
                     ]

    session['id_lan'] = id_game
    session['fin'] = False
    with open('data/lan.txt', "wb") as fp:
        pickle.dump(dico, fp)
    return redirect('lan.html')


@app.route('/save_game', methods=['GET'])
def save_game_html():
    """
    Redirection qui sauve la partie en cours
    """
    dico = charger_games()

    ecrire_game(dico, session['user'],
                session['scores'], session['figure_bool'])
    session['in_dico'] = True

    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Solo')+render_template('jouer.html')+render_template('footer.html')


@app.route('/lancer', methods=['GET'])
def lancer():
    """
    Redirection qui met ?? jour la liste des d??s en fonction des d??s selectionn??s (mode solo)
    """
    result = request.args
    session['lancer'] += 1

    for i in range(5):
        if str(i) in result and session['lancer'] <= NOMBRE_LANCER:
            session['des'][i] = random.randint(1, 6)

    session['projection'] = [[un(session['des']), deux(session['des']), trois(session['des']), quatre(session['des']), cinq(session['des']), six(session['des']), 0, 0, 0],
                             [superieur(session['des']),
                              inferieur(session['des']), 0],
                             [carre(session['des']), full(session['des']), petite_suite(session['des']), grande_suite(session['des']), yams(session['des']), 0, 0]]

    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Solo')+render_template('jouer.html')+render_template('footer.html')


@app.route('/lancer_multi', methods=['GET'])
def lancer_multi():
    """
    Redirection qui met ?? jour la liste des d??s en fonction des d??s selectionn??s (mode multi)
    """
    result = request.args
    session['lancer'] += 1
    for i in range(5):
        if str(i) in result:
            session['des'][i] = random.randint(1, 6)

    session['projection'] = [[un(session['des']), deux(session['des']), trois(session['des']), quatre(session['des']), cinq(session['des']), six(session['des']), 0, 0, 0],
                             [superieur(session['des']),
                              inferieur(session['des']), 0],
                             [carre(session['des']), full(session['des']), petite_suite(session['des']), grande_suite(session['des']), yams(session['des']), 0, 0]]

    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Local')+render_template('jouer_multi.html')+render_template('footer.html')


@app.route('/lancer_lan', methods=['GET'])
def lancer_lan():
    """
    Redirection qui met ?? jour la liste des d??s en fonction des d??s selectionn??s (mode multi)
    """
    result = request.args
    session['lancer'] += 1
    for i in range(5):
        if str(i) in result:
            session['des'][i] = random.randint(1, 6)

    session['projection'] = [[un(session['des']), deux(session['des']), trois(session['des']), quatre(session['des']), cinq(session['des']), six(session['des']), 0, 0, 0],
                             [superieur(session['des']),
                              inferieur(session['des']), 0],
                             [carre(session['des']), full(session['des']), petite_suite(session['des']), grande_suite(session['des']), yams(session['des']), 0, 0]]

    return render_template('header_home.html', page_name=NOM_DU_SITE+' - En ligne')+render_template('lan.html')+render_template('footer.html')


@app.route('/reset', methods=['GET'])
def reset():
    """
    Redirection qui met la partie ?? z??ro (mode solo)
    """
    session['des'] = [random.randint(1, 6) for _ in range(5)]

    session['scores'] = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0]]
    session['figure_bool'] = [[True, True, True, True, True, True],
                              [True, True],
                              [True, True, True, True, True]]
    session['projection'] = [[un(session['des']), deux(session['des']), trois(session['des']), quatre(session['des']), cinq(session['des']), six(session['des']), 0, 0, 0],
                             [superieur(session['des']),
                              inferieur(session['des']), 0],
                             [carre(session['des']), full(session['des']), petite_suite(session['des']), grande_suite(session['des']), yams(session['des']), 0, 0]]

    session['lancer'] = 0
    session['fin'] = False
    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Solo')+render_template('jouer.html')+render_template('footer.html')


@app.route('/reset_multi', methods=['GET'])
def reset_mutli():
    """
    Redirection qui met la partie ?? z??ro (mode multi)
    """
    session['des'] = [random.randint(1, 6) for _ in range(5)]

    session['scores'] = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0]]
    session['figure_bool'] = [[True, True, True, True, True, True],
                              [True, True],
                              [True, True, True, True, True]]
    session['lancer'] = 0
    session['fin'] = False
    session['multiplayer'] = False

    session['projection'] = [[un(session['des']), deux(session['des']), trois(session['des']), quatre(session['des']), cinq(session['des']), six(session['des']), 0, 0, 0],
                             [superieur(session['des']),
                              inferieur(session['des']), 0],
                             [carre(session['des']), full(session['des']), petite_suite(session['des']), grande_suite(session['des']), yams(session['des']), 0, 0]]

    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Local')+render_template('jouer_multi.html')+render_template('footer.html')


@app.route('/reset_lan', methods=['GET'])
def reset_lan():
    """
    Redirection qui met la partie ?? z??ro (mode multi)
    """
    session['des'] = [random.randint(1, 6) for _ in range(5)]

    session['scores'] = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0]]
    session['figure_bool'] = [[True, True, True, True, True, True],
                              [True, True],
                              [True, True, True, True, True]]
    session['lancer'] = 0
    session['fin'] = False
    session['multiplayer'] = False

    session['projection'] = [[un(session['des']), deux(session['des']), trois(session['des']), quatre(session['des']), cinq(session['des']), six(session['des']), 0, 0, 0],
                             [superieur(session['des']),
                              inferieur(session['des']), 0],
                             [carre(session['des']), full(session['des']), petite_suite(session['des']), grande_suite(session['des']), yams(session['des']), 0, 0]]

    return render_template('header_home.html', page_name=NOM_DU_SITE+' - En ligne')+render_template('lan.html')+render_template('footer.html')


@app.route('/enregistrer', methods=['GET'])
def maj_score():
    """
    Redirection qui met ?? jour le score apr??s avoir mis une figure (mode solo)
    """
    if 'scores' not in session:
        session['scores'] = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0]]

    if 'figure_bool' not in session:
        session['figure_bool'] = [[True, True, True, True, True, True],
                                  [True, True],
                                  [True, True, True, True, True]]

    result = request.args
    if result != {}:
        session['lancer'] = 0
        point = DICO_FONCTIONS[result['figure']](session['des'])
        x, y = DICO_PLACES[result['figure']]
        session['scores'][x][y] = point
        session['figure_bool'][x][y] = False
        session['fin'] = verif_fin(session['figure_bool'])
        session['des'] = [random.randint(1, 6) for _ in range(5)]

        x, y = DICO_PLACES['sous_total']
        session['scores'][x][y] = sous_total(session['scores'])

        x, y = DICO_PLACES['prime']
        session['scores'][x][y] = prime(session['scores'])

        x, y = DICO_PLACES['total_1']
        session['scores'][x][y] = total1(session['scores'])

        x, y = DICO_PLACES['total_2']
        session['scores'][x][y] = total2(session['scores'])

        x, y = DICO_PLACES['total_3']
        session['scores'][x][y] = total3(session['scores'])

        x, y = DICO_PLACES['total_final']
        session['scores'][x][y] = total_final(session['scores'])

        session['projection'] = [[un(session['des']), deux(session['des']), trois(session['des']), quatre(session['des']), cinq(session['des']), six(session['des']), 0, 0, 0],
                                 [superieur(session['des']),
                                  inferieur(session['des']), 0],
                                 [carre(session['des']), full(session['des']), petite_suite(session['des']), grande_suite(session['des']), yams(session['des']), 0, 0]]

    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Solo')+render_template('jouer.html')+render_template('footer.html')


@app.route('/enregistrer_lan', methods=['GET'])
def maj_score_lan():
    """
    Redirection qui met ?? jour le score apr??s avoir mis une figure (mode solo)
    """
    dico = session['lan'][session['id_lan']]
    tour = dico[0] % 2

    session['scores'] = dico[2][tour]
    session['figure_bool'] = dico[3][tour]

    result = request.args
    if result != {}:
        session['lancer'] = 0
        point = DICO_FONCTIONS[result['figure']](session['des'])
        x, y = DICO_PLACES[result['figure']]
        session['scores'][x][y] = point
        session['figure_bool'][x][y] = False
        session['fin'] = verif_fin(session['figure_bool'])
        session['des'] = [random.randint(1, 6) for _ in range(5)]

        x, y = DICO_PLACES['sous_total']
        session['scores'][x][y] = sous_total(session['scores'])

        x, y = DICO_PLACES['prime']
        session['scores'][x][y] = prime(session['scores'])

        x, y = DICO_PLACES['total_1']
        session['scores'][x][y] = total1(session['scores'])

        x, y = DICO_PLACES['total_2']
        session['scores'][x][y] = total2(session['scores'])

        x, y = DICO_PLACES['total_3']
        session['scores'][x][y] = total3(session['scores'])

        x, y = DICO_PLACES['total_final']
        session['scores'][x][y] = total_final(session['scores'])

        dico[2][tour] = session['scores']
        dico[3][tour] = session['figure_bool']
        dico[0] += 1
        session['lan']['id_lan'] = dico

        with open('data/lan.txt', "wb") as fp:
            pickle.dump(session['lan'], fp)

    return redirect('lan.html')


@app.route('/enregistrer_multi', methods=['GET'])
def maj_score_multi():
    """
    Redirection qui met ?? jour le score apr??s avoir mis une figure (mode mutli)
    """
    if 'scores' not in session:
        session['scores'] = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0]]

    if 'figure_bool' not in session:
        session['figure_bool'] = [[True, True, True, True, True, True],
                                  [True, True],
                                  [True, True, True, True, True]]

    result = request.args

    if result != {}:
        session['lancer'] = 0
        point = DICO_FONCTIONS[result['figure']](session['des'])
        x, y = DICO_PLACES[result['figure']]
        session['scores'][x][y] = point
        session['figure_bool'][x][y] = False
        session['fin'] = verif_fin(session['figure_bool'])
        session['des'] = [random.randint(1, 6) for _ in range(5)]

        x, y = DICO_PLACES['sous_total']
        session['scores'][x][y] = sous_total(session['scores'])

        x, y = DICO_PLACES['prime']
        session['scores'][x][y] = prime(session['scores'])

        x, y = DICO_PLACES['total_1']
        session['scores'][x][y] = total1(session['scores'])

        x, y = DICO_PLACES['total_2']
        session['scores'][x][y] = total2(session['scores'])

        x, y = DICO_PLACES['total_3']
        session['scores'][x][y] = total3(session['scores'])

        x, y = DICO_PLACES['total_final']
        session['scores'][x][y] = total_final(session['scores'])

        session['tour_multi'] = session['tour_multi']+1

        session['scores'] = session['dico_multi'][session['nom_multi']
                                                  [session['tour_multi'] % session['nb_joueur_multi']]][0]
        session['figure_bool'] = session['dico_multi'][session['nom_multi']
                                                       [session['tour_multi'] % session['nb_joueur_multi']]][1]

        session['projection'] = [[un(session['des']), deux(session['des']), trois(session['des']), quatre(session['des']), cinq(session['des']), six(session['des']), 0, 0, 0],
                                 [superieur(session['des']),
                                  inferieur(session['des']), 0],
                                 [carre(session['des']), full(session['des']), petite_suite(session['des']), grande_suite(session['des']), yams(session['des']), 0, 0]]

    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Local')+render_template('jouer_multi.html')+render_template('footer.html')


@app.route('/fin_score', methods=['GET'])
def fin_score():
    """
    Redirection qui ajoute le score dans le tableau des scores
    """
    name = session['user']
    ecrire_score('data/scores.txt', name,
                 datetime.today().strftime('%Y-%m-%d'), total_final(session['scores']))

    session['des'] = [random.randint(1, 6) for _ in range(5)]

    session['scores'] = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0]]
    session['figure_bool'] = [[True, True, True, True, True, True],
                              [True, True],
                              [True, True, True, True, True]]
    session['lancer'] = 0
    session['fin'] = False

    return render_template('header_home.html', page_name=NOM_DU_SITE+' - Solo')+render_template('jouer.html')+render_template('footer.html')


@app.route('/connect', methods=['POST'])
def connect():
    """
    Redirection qui g??re la connexion d'un utilisateur (avec la base de donn??es)
    """
    if request.form['action'] == 'connect':
        form_user = request.form['login']
        form_password = request.form['pwd']

        stream = os.popen('./hachage '+form_password)
        output = stream.read()
        try:
            if int(output) == int(get_hash(form_user)):
                session['user'] = form_user
                f = open('data/photos.txt', 'r')
                photo = {}
                for ligne in f:
                    nom, image = ligne.strip().split(';')
                    photo[nom] = image
                if form_user in photo:
                    session['photo'] = photo[form_user]
                else:
                    session.pop('photo')
                ajoute_connected(form_user)
                session['save_dico'] = charger_games()
                if session['user'] in session['save_dico']:
                    session['in_dico'] = True
                else:
                    session['in_dico'] = False
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
        form_user = request.form['login']
        form_password = request.form['pwd']
        form_password_confirm = request.form['confirm_pwd']

        if not existe_deja(form_user):
            ()
        else:
            page = """
                    <html>
                        <head>
                            <meta http-equiv="Refresh" content="5; url=/connecter.html" />
                        </head>
                        <body>
                        L'utilisateur existe d??j??. Redirection automatique dans 5 secondes
                        </body>
                    </html>
                        """
            return page
        if verif_mdp(form_password):
            ()
        else:
            page = """
                    <html>
                        <head>
                            <meta http-equiv="Refresh" content="5; url=/nv_compte.html" />
                        </head>
                        <body>
                        Le mot de passe doit avoir au moins : <br>
                        - Une majuscule <br>
                        - Une minuscule <br>
                        - Un chiffre <br>
                        - Six caract??res <br>
                        Redirection automatique dans 5 secondes...
                        </body>
                    </html>
                        """
            return page

        if form_password == form_password_confirm:
            add_user(form_user, form_password)
        else:
            page = """
                    <html>
                        <head>
                            <meta http-equiv="Refresh" content="5; url=/nv_compte.html" />
                        </head>
                        <body>
                        La confirmation n'est pas valide <br>
                        Redirection automatique dans 5 secondes...
                        </body>
                    </html>
                        """
            return page
        return redirect('/connecter.html')


@app.route('/send_msg', methods=['GET'])
def send_msg():
    """
    Redirection qui modifie le mot de passe d'un utilisateur dans la base de donn??es des comptes 
    """
    result = request.args

    ajoute_chat(session['user'], result['comment'])
    return redirect('/chat.html')


# ---------------------------------------------------------------------
# ---------------------- EXECUTION DU SERVEUR WEB ---------------------
# ---------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)
