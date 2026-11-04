"""Vérification de l'exercice 3.2 — lancer depuis la racine : python -m test.verif_3_2

Dessine sur une image en mémoire (pas de fenêtre), puis lit la couleur de quelques pixels.
"""
from test.verif import bilan, groupe, verifier, verifier_vrai

import pygame

from affichage import BLANC, GRIS, JAUNE, ORANGE, ROUGE, VERT, couleur_barre, dessiner_barre_pv, dessiner_texte
from moteur.personnages import Personnage

NOIR = (0, 0, 0)


def pixel(surface, x, y):
    return tuple(surface.get_at((x, y)))[:3]


@groupe("1. couleur_barre(ratio)")
def _():
    verifier("ratio 1.0 → VERT", couleur_barre(1.0), VERT)
    verifier("ratio 0.6 → VERT", couleur_barre(0.6), VERT)
    verifier("ratio 0.5 → ORANGE (il faut être AU-DESSUS de 0.5 pour VERT)", couleur_barre(0.5), ORANGE)
    verifier("ratio 0.3 → ORANGE", couleur_barre(0.3), ORANGE)
    verifier("ratio 0.2 → ROUGE", couleur_barre(0.2), ROUGE)
    verifier("ratio 0.0 → ROUGE", couleur_barre(0.0), ROUGE)


@groupe("2. dessiner_barre_pv(ecran, x, y, perso) — barre pleine")
def _():
    ecran = pygame.Surface((300, 50))
    ecran.fill(NOIR)
    perso = Personnage("Test", 50, 10, 2)
    dessiner_barre_pv(ecran, 10, 10, perso)
    verifier("milieu de la barre : VERT", pixel(ecran, 110, 18), VERT)
    verifier("coin haut-gauche : contour BLANC", pixel(ecran, 10, 10), BLANC)
    verifier("bord droit (x = 10 + 200 - 1) : contour BLANC", pixel(ecran, 209, 18), BLANC)
    verifier("bord bas (y = 10 + 16 - 1) : contour BLANC", pixel(ecran, 110, 25), BLANC)
    verifier("juste après la barre (x = 210) : rien dessiné", pixel(ecran, 210, 18), NOIR)
    verifier("juste sous la barre (y = 26) : rien dessiné", pixel(ecran, 110, 26), NOIR)


@groupe("3. Barre à moitié, barre vide")
def _():
    ecran = pygame.Surface((300, 50))
    ecran.fill(NOIR)
    perso = Personnage("Test", 50, 10, 2)
    perso.pv = 25
    dessiner_barre_pv(ecran, 10, 10, perso)
    verifier("25/50 : début de la barre ORANGE", pixel(ecran, 50, 18), ORANGE)
    verifier("25/50 : fin de la barre GRIS (PV perdus)", pixel(ecran, 170, 18), GRIS)

    ecran.fill(NOIR)
    perso.pv = 0
    dessiner_barre_pv(ecran, 10, 10, perso)
    verifier("0/50 : toute la barre GRIS", pixel(ecran, 50, 18), GRIS)
    verifier("0/50 : le contour reste BLANC", pixel(ecran, 10, 10), BLANC)


@groupe("4. dessiner_texte(ecran, police, texte, x, y, couleur=BLANC)")
def _():
    pygame.font.init()
    police = pygame.font.Font(None, 30)
    ecran = pygame.Surface((200, 60))
    ecran.fill(NOIR)
    dessiner_texte(ecran, police, "Test", 20, 10)
    couleurs = {pixel(ecran, x, y) for x in range(200) for y in range(60)}
    verifier_vrai("du texte a été dessiné", len(couleurs) > 1, "l'image est restée entièrement noire")
    verifier_vrai("couleur par défaut : BLANC", BLANC in couleurs)
    verifier_vrai("rien n'est dessiné à gauche de x = 20", all(pixel(ecran, x, y) == NOIR
                                                             for x in range(20) for y in range(60)))

    ecran.fill(NOIR)
    dessiner_texte(ecran, police, "Test", 20, 10, JAUNE)
    couleurs = {pixel(ecran, x, y) for x in range(200) for y in range(60)}
    verifier_vrai("avec couleur=JAUNE : texte JAUNE", JAUNE in couleurs and BLANC not in couleurs)


bilan()
