"""Vérification de l'exercice 3.1 — lancer depuis la racine : python -m test.verif_3_1"""
from test.verif import bilan, groupe, verifier

import affichage


@groupe("1. hex_vers_rgb(code)")
def _():
    verifier('hex_vers_rgb("#E69628")', affichage.hex_vers_rgb("#E69628"), (230, 150, 40))
    verifier('hex_vers_rgb("E69628") (sans #)', affichage.hex_vers_rgb("E69628"), (230, 150, 40))
    verifier('hex_vers_rgb("#000000")', affichage.hex_vers_rgb("#000000"), (0, 0, 0))
    verifier('hex_vers_rgb("#FFFFFF")', affichage.hex_vers_rgb("#FFFFFF"), (255, 255, 255))
    verifier('hex_vers_rgb("#ff8000") (minuscules)', affichage.hex_vers_rgb("#ff8000"), (255, 128, 0))
    verifier("renvoie un tuple", type(affichage.hex_vers_rgb("#123456")).__name__, "tuple")


@groupe("2. La palette")
def _():
    attendu = {
        "FOND": (25, 25, 35), "BLANC": (240, 240, 240), "GRIS": (80, 80, 90),
        "JAUNE": (250, 210, 60), "BLEU": (70, 130, 220), "ROUGE": (200, 60, 60),
        "VERT": (60, 190, 90), "ORANGE": (230, 150, 40),
    }
    for nom, rgb in attendu.items():
        verifier(nom, getattr(affichage, nom), rgb)


bilan()
