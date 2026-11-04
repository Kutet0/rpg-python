"""Vérification de l'exercice 4.2 — lancer depuis la racine : python -m test.verif_4_2"""
from test.verif import bilan, groupe, sans_affichage, verifier, verifier_vrai

import pygame

from affichage import JAUNE, Menu


@groupe("1. Création")
def _():
    menu = Menu(["Attaquer", "Coup puissant", "Potion", "Fuir"])
    verifier("options", menu.options, ["Attaquer", "Coup puissant", "Potion", "Fuir"])
    verifier("selection de départ", menu.selection, 0)
    verifier("choix de départ (propriété, sans parenthèses)", menu.choix, "Attaquer")


@groupe("2. descendre() et monter(), avec bouclage")
def _():
    menu = Menu(["A", "B", "C", "D"])
    menu.descendre()
    verifier("descendre une fois → 1", menu.selection, 1)
    menu.descendre()
    menu.descendre()
    verifier("descendre jusqu'en bas → 3", menu.selection, 3)
    menu.descendre()
    verifier("descendre depuis le bas → retour à 0", menu.selection, 0)
    menu.monter()
    verifier("monter depuis le haut → 3", menu.selection, 3)
    verifier("choix correspondant", menu.choix, "D")


@groupe("3. gerer_touche(touche)")
def _():
    menu = Menu(["A", "B", "C", "D"])
    verifier("K_DOWN renvoie False", menu.gerer_touche(pygame.K_DOWN), False)
    verifier("... et descend", menu.selection, 1)
    verifier("K_UP renvoie False", menu.gerer_touche(pygame.K_UP), False)
    verifier("... et monte", menu.selection, 0)
    verifier("K_a (autre touche) renvoie False", menu.gerer_touche(pygame.K_a), False)
    verifier("... et ne bouge rien", menu.selection, 0)
    verifier("K_RETURN renvoie True", menu.gerer_touche(pygame.K_RETURN), True)
    verifier("... et ne bouge rien", menu.selection, 0)
    _, texte = sans_affichage(menu.gerer_touche, pygame.K_DOWN)
    verifier("gerer_touche ne fait aucun print", texte, "")


@groupe("4. Changer les options en cours de route")
def _():
    menu = Menu(["Attaquer", "Potion (3)"])
    menu.descendre()
    menu.options = ["Attaquer", "Potion (2)"]
    verifier("choix suit la nouvelle liste", menu.choix, "Potion (2)")


@groupe("5. dessiner(ecran, police, x, y)")
def _():
    pygame.font.init()
    police = pygame.font.Font(None, 30)
    ecran = pygame.Surface((300, 200))
    ecran.fill((0, 0, 0))
    menu = Menu(["A", "B", "C"])
    menu.descendre()
    menu.dessiner(ecran, police, 10, 10)
    lignes_jaunes = {y for x in range(300) for y in range(200)
                     if tuple(ecran.get_at((x, y)))[:3] == JAUNE}
    verifier_vrai("l'option sélectionnée est en JAUNE", lignes_jaunes, "aucun pixel JAUNE")
    if lignes_jaunes:
        verifier_vrai("le JAUNE est sur la 2e ligne (y entre 50 et 80)",
                      50 <= min(lignes_jaunes) and max(lignes_jaunes) < 80,
                      f"pixels jaunes entre y = {min(lignes_jaunes)} et y = {max(lignes_jaunes)}")


bilan()
