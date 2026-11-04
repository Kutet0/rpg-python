"""Vérification de l'exercice 7.2 — lancer depuis la racine : python -m test.verif_7_2"""
from test.jeu_factice import JeuFactice
from test.verif import bilan, groupe, verifier, verifier_erreur, verifier_vrai

import pygame

from etats import ChoixClasse, Combat, EtatCombat, TourJoueur
from moteur.personnages import Guerrier, Mage, Monstre


@groupe("1. Combat")
def _():
    heros = Guerrier("Ednir")
    monstre = Monstre("Orc", 45, 11, 3)
    combat = Combat(heros, monstre)
    verifier("combat.heros", combat.heros, heros)
    verifier("combat.monstre", combat.monstre, monstre)
    verifier("premier message", combat.messages, ["Un Orc sauvage apparaît !"])
    for i in range(1, 6):
        combat.journaliser(f"message {i}")
    verifier("journaliser ajoute à la fin", combat.messages[-1], "message 5")
    verifier("derniers_messages (propriété) : les 4 derniers", combat.derniers_messages,
             ["message 2", "message 3", "message 4", "message 5"])


@groupe("2. EtatCombat est abstraite")
def _():
    combat = Combat(Guerrier("Ednir"), Monstre("Orc", 45, 11, 3))
    verifier_erreur("EtatCombat(jeu, combat) lève TypeError (dessiner_panneau est abstraite)",
                    TypeError, EtatCombat, JeuFactice(), combat)


@groupe("3. ChoixClasse -> TourJoueur")
def _():
    jeu = JeuFactice()
    ChoixClasse(jeu).gerer_touche(pygame.K_RETURN)
    verifier_vrai("Entrée sur Guerrier : passe en TourJoueur", isinstance(jeu.etat, TourJoueur),
                  f"jeu.etat vaut {jeu.etat!r}")
    if isinstance(jeu.etat, TourJoueur):
        verifier_vrai("TourJoueur hérite d'EtatCombat", isinstance(jeu.etat, EtatCombat))
        verifier_vrai("le héros est un Guerrier nommé Ednir",
                      isinstance(jeu.etat.combat.heros, Guerrier) and jeu.etat.combat.heros.nom == "Ednir")
        verifier_vrai("le monstre est un Monstre", isinstance(jeu.etat.combat.monstre, Monstre))

    jeu = JeuFactice()
    choix = ChoixClasse(jeu)
    choix.gerer_touche(pygame.K_DOWN)
    choix.gerer_touche(pygame.K_RETURN)
    verifier_vrai("Bas puis Entrée : le héros est un Mage",
                  isinstance(jeu.etat, TourJoueur) and isinstance(jeu.etat.combat.heros, Mage))


bilan()
