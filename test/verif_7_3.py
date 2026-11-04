"""Vérification de l'exercice 7.3 — lancer depuis la racine : python -m test.verif_7_3"""
from test.jeu_factice import JeuFactice
from test.verif import bilan, groupe, verifier, verifier_vrai

import pygame

from etats import ChoixClasse, Combat, Fin, TourJoueur, TourMonstre
from moteur.personnages import Guerrier, Monstre

pygame.init()


def nouveau_tour(pv_monstre=45):
    """Un TourJoueur prêt, sans esquive possible."""
    heros = Guerrier("Ednir")
    monstre = Monstre("Orc", 45, 11, 3)
    monstre.pv = pv_monstre
    heros.CHANCE_ESQUIVE = 0
    monstre.CHANCE_ESQUIVE = 0
    jeu = JeuFactice()
    jeu.etat = TourJoueur(jeu, Combat(heros, monstre))
    return jeu


def appuyer(jeu, *touches):
    for touche in touches:
        jeu.etat.gerer_touche(touche)


@groupe("1. Le menu de combat")
def _():
    jeu = nouveau_tour()
    verifier("options()", jeu.etat.options(), ["Attaquer", "Coup puissant", "Potion (3)", "Fuir"])
    avant = jeu.etat
    appuyer(jeu, pygame.K_DOWN)
    verifier_vrai("une flèche ne change pas d'état", jeu.etat is avant)
    verifier("... mais déplace la sélection", jeu.etat.menu.selection, 1)


@groupe("2. Action refusée : on reste dans le même état")
def _():
    jeu = nouveau_tour()
    avant = jeu.etat
    appuyer(jeu, pygame.K_DOWN, pygame.K_DOWN, pygame.K_RETURN)
    verifier_vrai("potion à PV max : toujours le même TourJoueur", jeu.etat is avant,
                  f"jeu.etat vaut {jeu.etat!r}")
    verifier("le refus est dans le journal", avant.combat.messages[-1], "Tu as déjà tous tes PV.")


@groupe("3. Fuite")
def _():
    jeu = nouveau_tour()
    appuyer(jeu, pygame.K_UP, pygame.K_RETURN)
    verifier_vrai("Fuir : passe en Fin", isinstance(jeu.etat, Fin), f"jeu.etat vaut {jeu.etat!r}")
    if isinstance(jeu.etat, Fin):
        verifier("titre", jeu.etat.titre, "FUITE !")
        verifier("journal", jeu.etat.combat.messages[-1], "Tu prends la fuite !")


@groupe("4. Victoire")
def _():
    jeu = nouveau_tour(pv_monstre=1)
    appuyer(jeu, pygame.K_RETURN)
    verifier_vrai("monstre à 1 PV, Attaquer : passe en Fin", isinstance(jeu.etat, Fin),
                  f"jeu.etat vaut {jeu.etat!r}")
    if isinstance(jeu.etat, Fin):
        verifier("titre", jeu.etat.titre, "VICTOIRE !")
        verifier("journal", jeu.etat.combat.messages[-1], "Orc est vaincu !")


@groupe("5. Le monstre survit")
def _():
    jeu = nouveau_tour()
    appuyer(jeu, pygame.K_RETURN)
    verifier_vrai("Attaquer, monstre vivant : passe en TourMonstre", isinstance(jeu.etat, TourMonstre),
                  f"jeu.etat vaut {jeu.etat!r}")


@groupe("6. Fin -> ChoixClasse")
def _():
    jeu = nouveau_tour()
    appuyer(jeu, pygame.K_UP, pygame.K_RETURN)
    if isinstance(jeu.etat, Fin):
        appuyer(jeu, pygame.K_a)
        verifier_vrai("une autre touche que R ne fait rien", isinstance(jeu.etat, Fin))
        appuyer(jeu, pygame.K_r)
        verifier_vrai("R : retour à ChoixClasse", isinstance(jeu.etat, ChoixClasse),
                      f"jeu.etat vaut {jeu.etat!r}")
    else:
        verifier_vrai("R : retour à ChoixClasse", False, "impossible à tester : la fuite ne mène pas à Fin")


bilan()
