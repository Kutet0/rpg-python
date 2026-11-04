"""Vérification de l'exercice 1.1 — lancer depuis la racine : python -m test.verif_1_1"""
from test.verif import bilan, groupe, sans_affichage, verifier, verifier_vrai

from moteur.exceptions import ActionImpossible
from moteur.personnages import Personnage


@groupe("1. L'exception ActionImpossible")
def _():
    verifier_vrai("ActionImpossible hérite d'Exception", issubclass(ActionImpossible, Exception))


@groupe("2. Création d'un personnage")
def _():
    p = Personnage("Test", 50, 10, 2)
    verifier("attribut nom", p.nom, "Test")
    verifier("attribut pv_max", p.pv_max, 50)
    verifier("attribut attaque", p.attaque, 10)
    verifier("attribut defense", p.defense, 2)
    verifier("les PV commencent à pv_max", p.pv, 50)
    verifier("la vraie valeur est rangée dans _pv", p._pv, 50)


@groupe("3. La propriété pv (getter + setter)")
def _():
    p = Personnage("Test", 50, 10, 2)
    p.pv -= 8
    verifier("pv -= 8 → 42", p.pv, 42)
    p.pv -= 999
    verifier("les PV ne descendent pas sous 0", p.pv, 0)
    p.pv += 999
    verifier("les PV ne dépassent pas pv_max", p.pv, 50)
    p.pv = 25
    verifier("pv = 25 → 25", p.pv, 25)


@groupe("4. Les propriétés est_vivant et ratio_pv")
def _():
    p = Personnage("Test", 50, 10, 2)
    verifier_vrai("est_vivant est une propriété (s'utilise sans parenthèses)",
                  isinstance(p.est_vivant, bool),
                  f"p.est_vivant donne {p.est_vivant!r} : il manque @property, ou un return ?")
    verifier("vivant à 50 PV", p.est_vivant, True)
    p.pv = 0
    verifier("mort à 0 PV", p.est_vivant, False)
    p.pv = 25
    verifier_vrai("ratio_pv est une propriété (s'utilise sans parenthèses)",
                  isinstance(p.ratio_pv, float),
                  f"p.ratio_pv donne {p.ratio_pv!r} : il manque @property, ou un return ?")
    verifier("ratio_pv à 25/50 → 0.5", p.ratio_pv, 0.5)


@groupe("5. Affichage avec __repr__")
def _():
    p = Personnage("Test", 50, 10, 2)
    p.pv = 0
    verifier("repr(p)", repr(p), "Personnage('Test', pv=0/50)")

    class Sorcier(Personnage):
        pass

    s = Sorcier("Zed", 30, 5, 1)
    verifier("le nom de la classe n'est pas écrit en dur (type(self).__name__)",
             repr(s), "Sorcier('Zed', pv=30/30)")


@groupe("6. Aucun print dans la classe")
def _():
    _, texte = sans_affichage(Personnage, "Test", 50, 10, 2)
    verifier("rien n'est affiché à la création", texte, "")


bilan()
