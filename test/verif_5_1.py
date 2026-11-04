"""Vérification de l'exercice 5.1 — lancer depuis la racine : python -m test.verif_5_1"""
from test.verif import bilan, groupe, verifier, verifier_vrai

import pygame

from minuteur import Minuteur

pygame.init()


@groupe("1. Avant demarrer()")
def _():
    m = Minuteur(200)
    verifier("duree", m.duree, 200)
    verifier("actif (propriété)", m.actif, False)
    verifier("ecoule (propriété)", m.ecoule, False)
    verifier("progression (propriété)", m.progression, 0.0)


@groupe("2. Pendant (attente réelle de 100 ms sur 200)")
def _():
    m = Minuteur(200)
    m.demarrer()
    verifier("actif juste après demarrer()", m.actif, True)
    verifier("pas encore écoulé", m.ecoule, False)
    pygame.time.wait(100)
    verifier_vrai("progression vers 0.5 à mi-chemin", 0.4 <= m.progression <= 0.7,
                  f"progression : {m.progression}")
    verifier("toujours pas écoulé", m.ecoule, False)


@groupe("3. Après la durée (attente réelle de 250 ms sur 200)")
def _():
    m = Minuteur(200)
    m.demarrer()
    pygame.time.wait(250)
    verifier("écoulé", m.ecoule, True)
    verifier("progression plafonnée à 1.0", m.progression, 1.0)


@groupe("4. arreter() et redémarrer")
def _():
    m = Minuteur(200)
    m.demarrer()
    pygame.time.wait(250)
    m.arreter()
    verifier("inactif après arreter()", m.actif, False)
    verifier("plus écoulé après arreter()", m.ecoule, False)
    verifier("progression 0.0 après arreter()", m.progression, 0.0)
    m.demarrer()
    verifier("redémarré : pas écoulé", m.ecoule, False)
    m.duree = 50
    pygame.time.wait(80)
    verifier("on peut changer la durée en cours de route", m.ecoule, True)


bilan()
