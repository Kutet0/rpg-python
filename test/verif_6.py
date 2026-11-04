"""Vérification du chapitre 6 — lancer depuis la racine : python -m test.verif_6

Lance ton jeu.py sans fenêtre, appuie sur les touches à ta place, et note l'état du jeu
à chaque frame. Ton jeu.py doit utiliser les variables etat et messages, comme dans l'énoncé.

Scénario joué : choisir Guerrier, boire une potion à PV max (refusée), attaquer,
attendre le monstre, fuir, puis R pour revenir au choix de classe.
"""
import runpy
import sys

from test.verif import bilan, groupe, verifier, verifier_vrai

import pygame

# frame -> touches appuyées à cette frame
SCENARIO = {
    10: [pygame.K_RETURN],                        # choisir Guerrier
    20: [pygame.K_DOWN], 25: [pygame.K_DOWN],     # aller sur Potion
    30: [pygame.K_RETURN],                        # potion refusée (PV au max)
    40: [pygame.K_UP], 45: [pygame.K_UP],         # revenir sur Attaquer
    50: [pygame.K_RETURN],                        # attaquer -> tour du monstre
    160: [pygame.K_DOWN], 165: [pygame.K_DOWN], 170: [pygame.K_DOWN],   # aller sur Fuir
    180: [pygame.K_RETURN],                       # fuir
    200: [pygame.K_r],                            # revenir au choix de classe
}
FRAME_QUIT = 220
FRAME_MAX = 400


class TropLong(Exception):
    pass


etats = []
messages_vus = []
_get = pygame.event.get
_flip = pygame.display.flip


def faux_get(*args, **kwargs):
    evenements = _get(*args, **kwargs)
    n = len(etats)
    for touche in SCENARIO.get(n, []):
        evenements.append(pygame.event.Event(pygame.KEYDOWN, key=touche))
    if n >= FRAME_QUIT:
        evenements.append(pygame.event.Event(pygame.QUIT))
    return evenements


def fausse_flip(*args, **kwargs):
    variables = sys._getframe(1).f_globals
    etats.append(variables.get("etat", "<pas de variable etat>"))
    for message in variables.get("messages") or []:
        if message not in messages_vus:
            messages_vus.append(message)
    if len(etats) > FRAME_MAX:
        raise TropLong()
    return _flip(*args, **kwargs)


pygame.event.get = faux_get
pygame.display.flip = fausse_flip
pygame.display.update = fausse_flip


@groupe("1. Lancement du scénario")
def _():
    try:
        runpy.run_path("jeu.py", run_name="__main__")
        verifier_vrai("le jeu s'arrête quand on ferme la fenêtre (QUIT)", True)
    except TropLong:
        verifier_vrai("le jeu s'arrête quand on ferme la fenêtre (QUIT)", False,
                      "la boucle continue après QUIT : en_cours passe-t-il à False ?")


@groupe("2. Les transitions")
def _():
    suite = []
    for etat in etats:
        if not suite or suite[-1] != etat:
            suite.append(etat)
    print(f"         états traversés : {' -> '.join(map(str, suite))}")
    verifier("suite des états", suite,
             ["CHOIX_CLASSE", "TOUR_JOUEUR", "TOUR_MONSTRE", "TOUR_JOUEUR", "FUITE", "CHOIX_CLASSE"])
    duree_monstre = etats.count("TOUR_MONSTRE")
    verifier_vrai("le monstre attend environ 1 seconde (45 à 80 frames)", 45 <= duree_monstre <= 80,
                  f"TOUR_MONSTRE a duré {duree_monstre} frames")


@groupe("3. Le journal")
def _():
    verifier_vrai("message d'apparition du monstre", any("sauvage apparaît !" in m for m in messages_vus))
    verifier_vrai("potion refusée : 'Tu as déjà tous tes PV.' dans le journal",
                  "Tu as déjà tous tes PV." in messages_vus)
    verifier_vrai("le héros a attaqué (message de attaquer)",
                  any(m.startswith("Ednir") or "esquive l'attaque de Ednir" in m for m in messages_vus))
    verifier_vrai("fuite : 'Tu prends la fuite !' dans le journal", "Tu prends la fuite !" in messages_vus)


bilan()
