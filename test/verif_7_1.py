"""Vérification de l'exercice 7.1 — lancer depuis la racine : python -m test.verif_7_1"""
from test.jeu_factice import JeuFactice
from test.verif import bilan, groupe, verifier, verifier_erreur, verifier_vrai

import pygame

from etats import ChoixClasse, Etat


@groupe("1. Etat est abstraite")
def _():
    verifier_erreur("Etat(jeu) lève TypeError (dessiner est abstraite)", TypeError, Etat, JeuFactice())


@groupe("2. ChoixClasse")
def _():
    jeu = JeuFactice()
    etat = ChoixClasse(jeu)
    verifier_vrai("ChoixClasse hérite d'Etat", isinstance(etat, Etat))
    verifier("garde le jeu dans self.jeu", etat.jeu, jeu)
    verifier("son menu propose les classes", etat.menu.options, ["Guerrier", "Mage"])
    etat.gerer_touche(pygame.K_DOWN)
    verifier("K_DOWN déplace la sélection du menu", etat.menu.selection, 1)
    verifier("mettre_a_jour() existe et ne fait rien", etat.mettre_a_jour(), None)


bilan()
