"""Vérification de l'exercice 7.4 — lancer depuis la racine : python -m test.verif_7_4

Attend vraiment le minuteur : ce test dure environ 3 secondes.
"""
from test.jeu_factice import JeuFactice
from test.verif import bilan, groupe, verifier, verifier_vrai

import pygame

from etats import Combat, Fin, TourJoueur, TourMonstre
from moteur.personnages import Guerrier, Monstre

pygame.init()


def nouveau_tour_monstre(pv_heros=60):
    """Un TourMonstre prêt : le monstre attaque toujours, personne n'esquive."""
    heros = Guerrier("Ednir")
    heros.pv = pv_heros
    monstre = Monstre("Orc", 45, 11, 3)
    heros.CHANCE_ESQUIVE = monstre.CHANCE_ESQUIVE = 0
    monstre.CHANCE_RUGIR = 0
    jeu = JeuFactice()
    jeu.etat = TourMonstre(jeu, Combat(heros, monstre))
    return jeu


@groupe("1. Le monstre attend 1 seconde")
def _():
    jeu = nouveau_tour_monstre()
    avant = jeu.etat
    jeu.etat.mettre_a_jour()
    verifier_vrai("tout de suite : rien ne se passe", jeu.etat is avant)
    pygame.time.wait(800)
    jeu.etat.mettre_a_jour()
    verifier_vrai("après 0,8 s : toujours rien", jeu.etat is avant)
    pygame.time.wait(300)
    jeu.etat.mettre_a_jour()
    verifier_vrai("après 1,1 s : le monstre a agi, retour à TourJoueur", isinstance(jeu.etat, TourJoueur),
                  f"jeu.etat vaut {jeu.etat!r}")
    verifier_vrai("le héros a perdu des PV", avant.combat.heros.pv < 60)
    verifier_vrai("l'action du monstre est dans le journal", "Orc inflige" in avant.combat.messages[-1],
                  f"dernier message : {avant.combat.messages[-1]!r}")


@groupe("2. Défaite")
def _():
    jeu = nouveau_tour_monstre(pv_heros=1)
    combat = jeu.etat.combat
    pygame.time.wait(1100)
    jeu.etat.mettre_a_jour()
    verifier_vrai("héros à 1 PV : passe en Fin", isinstance(jeu.etat, Fin), f"jeu.etat vaut {jeu.etat!r}")
    if isinstance(jeu.etat, Fin):
        verifier("titre", jeu.etat.titre, "DÉFAITE...")
    verifier("journal", combat.messages[-1], "Ednir est tombé au combat...")


@groupe("3. Chaque tour du monstre a son propre minuteur")
def _():
    jeu = nouveau_tour_monstre()
    pygame.time.wait(1100)
    jeu.etat.mettre_a_jour()
    if isinstance(jeu.etat, TourJoueur):
        jeu.etat.gerer_touche(pygame.K_RETURN)
        verifier_vrai("le joueur attaque : nouveau TourMonstre", isinstance(jeu.etat, TourMonstre))
        avant = jeu.etat
        jeu.etat.mettre_a_jour()
        verifier_vrai("le nouveau monstre attend à nouveau (pas d'action immédiate)", jeu.etat is avant)
    else:
        verifier_vrai("le nouveau monstre attend à nouveau", False, "le groupe 1 doit d'abord passer")


bilan()
