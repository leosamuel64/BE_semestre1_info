# Structures de données

## Feuille des scores
La feuille des scores est une liste de liste de la forme suivante :

```python
[   [un,deux,trois,quatre,cinq,six,sous_total,prime,total1],
    [Supérieur, Inférieur, total2],
    [Carré,Full,petite_suite,grande_suite,yams,total3,total_final]    
]
```

Afin de facilité l'accessiblité, il existe un dictionnaire qui fait le lien entre le nom de la case et la position dans la matrice des scores :

```python
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
```

Le choix de la structure pour la feuille des scores est un matrice au lieu d'un dictionnaire car il sera ensuite plus simple d'itérer dessus.

## Système de compte

La structure de données est une base de données SQL. Elle est constitué d'une seul table associant un login à un hash.
Les mots de passe ne sont pas enregistrer. Ils sont hashé lors de la création du compte puis a chaque connexion pour permettre la vérification.

## Sauvegarde des scores

La sauvegarde des scores est réalisé au moyen d'un fichier texte. Les scores sont triés pour faire afficher le meilleur score en premier.

## Sauvegarde des parties

Chaque partie est représenté par deux matrices. La première est la matrice des scores et la deuxième la matrice indiquant si la figure a été joué.

La sauvegarde est réalisé avec un dictionnaire assiciant un nom d'utilisateur au couple des deux matrices. Ce dictionnaire est ensuite enregistrer dans un fichier.

