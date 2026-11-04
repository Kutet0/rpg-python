"""Vérification de l'exercice 1.2 — lancer depuis la racine : python -m test.verif_1_2"""
from test.verif import bilan, groupe, sans_affichage, verifier, verifier_vrai

from moteur.personnages import Personnage


class SansHasard(Personnage):
    """Un personnage qui n'esquive jamais et ne fait jamais de critique."""
    CHANCE_ESQUIVE = 0
    CHANCE_CRITIQUE = 0


class ToujoursEsquive(Personnage):
    CHANCE_ESQUIVE = 1


class ToujoursCritique(Personnage):
    CHANCE_ESQUIVE = 0
    CHANCE_CRITIQUE = 1


@groupe("1. Les constantes de classe")
def _():
    verifier("Personnage.CHANCE_ESQUIVE", Personnage.CHANCE_ESQUIVE, 0.15)
    verifier("Personnage.CHANCE_CRITIQUE", Personnage.CHANCE_CRITIQUE, 0.10)


@groupe("2. calculer_degats(cible)")
def _():
    a = Personnage("A", 50, 12, 0)
    cible = Personnage("C", 50, 0, 4)
    resultat, texte = sans_affichage(a.calculer_degats, cible)
    verifier("calculer_degats ne fait aucun print", texte, "")
    tirages = {a.calculer_degats(cible) for _ in range(2000)}
    verifier("attaque 12, défense 4 : tous les dégâts possibles sortent (6 à 10)",
             tirages, {6, 7, 8, 9, 10})
    faible = Personnage("Faible", 50, 3, 0)
    blinde = Personnage("Blindé", 50, 0, 8)
    tirages = {faible.calculer_degats(blinde) for _ in range(500)}
    verifier("attaque 3, défense 8 : toujours le minimum, 1", tirages, {1})
    verifier("calculer_degats ne touche pas aux PV de la cible", blinde.pv, 50)


@groupe("3. attaquer(cible) : coup normal")
def _():
    a = SansHasard("Ednir", 50, 12, 0)
    cible = Personnage("Orc", 100, 0, 4)
    message, texte = sans_affichage(a.attaquer, cible)
    perdu = 100 - cible.pv
    verifier_vrai("la cible perd entre 6 et 10 PV", 6 <= perdu <= 10, f"PV perdus : {perdu}")
    verifier("message renvoyé", message, f"Ednir inflige {perdu} dégâts à Orc.")
    verifier("attaquer ne fait aucun print", texte, "")


@groupe("4. attaquer(cible) : esquive")
def _():
    a = ToujoursEsquive("Ednir", 50, 12, 0)
    cible = Personnage("Orc", 100, 0, 4)
    message = a.attaquer(cible)
    verifier("message renvoyé", message, "Orc esquive l'attaque de Ednir !")
    verifier("la cible ne perd aucun PV", cible.pv, 100)


@groupe("5. attaquer(cible) : critique")
def _():
    a = ToujoursCritique("Ednir", 50, 12, 0)
    cible = Personnage("Orc", 100, 0, 4)
    message = a.attaquer(cible)
    perdu = 100 - cible.pv
    verifier_vrai("la cible perd le double (12 à 20 PV)", 12 <= perdu <= 20 and perdu % 2 == 0,
                  f"PV perdus : {perdu}")
    verifier("message renvoyé", message, f"CRITIQUE ! Ednir inflige {perdu} dégâts à Orc !")


@groupe("6. Les probabilités (sur 4000 attaques)")
def _():
    a = Personnage("Ednir", 50, 12, 0)

    def compter():
        esquives = critiques = 0
        for _ in range(4000):
            message = a.attaquer(Personnage("Orc", 100, 0, 4))
            if "esquive" in message:
                esquives += 1
            elif message.startswith("CRITIQUE"):
                critiques += 1
        return esquives, critiques

    (esquives, critiques), _ = sans_affichage(compter)
    verifier_vrai("environ 15 % d'esquives", 0.12 <= esquives / 4000 <= 0.18,
                  f"obtenu : {esquives / 40:.1f} %")
    verifier_vrai("environ 8,5 % de critiques (10 % des coups non esquivés)",
                  0.06 <= critiques / 4000 <= 0.11, f"obtenu : {critiques / 40:.1f} %")


@groupe("7. Les PV ne passent jamais sous 0")
def _():
    a = ToujoursCritique("Ednir", 50, 12, 0)
    cible = Personnage("Gobelin", 5, 0, 0)
    a.attaquer(cible)
    verifier("un coup énorme sur 5 PV → 0", cible.pv, 0)


bilan()
