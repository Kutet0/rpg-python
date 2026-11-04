"""Vérification de l'exercice 1.4 — lancer depuis la racine : python -m test.verif_1_4"""
from test.verif import bilan, groupe, sans_affichage, verifier, verifier_vrai

from moteur.personnages import BESTIAIRE, Monstre, Personnage


class Boss(Monstre):
    pass


class JamaisRugir(Monstre):
    CHANCE_RUGIR = 0
    CHANCE_ESQUIVE = 0


class ToujoursRugir(Monstre):
    CHANCE_RUGIR = 1


@groupe("1. Monstre et BESTIAIRE")
def _():
    verifier_vrai("Monstre hérite de Personnage", issubclass(Monstre, Personnage))
    verifier("CHANCE_RUGIR", Monstre.CHANCE_RUGIR, 0.25)
    verifier("noms du BESTIAIRE", [d["nom"] for d in BESTIAIRE], ["Gobelin", "Loup", "Orc"])


@groupe("2. Monstre.depuis_dict(donnees)")
def _():
    m = Monstre.depuis_dict({"nom": "Troll", "pv": 80, "attaque": 14, "defense": 6})
    verifier_vrai("renvoie un Monstre", isinstance(m, Monstre), f"obtenu : {m!r}")
    verifier("nom, pv_max, attaque, defense", (m.nom, m.pv_max, m.attaque, m.defense),
             ("Troll", 80, 14, 6))
    b = Boss.depuis_dict({"nom": "Liche", "pv": 120, "attaque": 15, "defense": 5})
    verifier("utilise cls : Boss.depuis_dict fabrique un Boss", type(b).__name__, "Boss")


@groupe("3. Monstre.aleatoire()")
def _():
    noms = {Monstre.aleatoire().nom for _ in range(300)}
    verifier("tire les 3 monstres du BESTIAIRE", noms, {"Gobelin", "Loup", "Orc"})
    verifier("utilise cls : Boss.aleatoire() fabrique un Boss", type(Boss.aleatoire()).__name__, "Boss")


@groupe("4. agir(cible)")
def _():
    rugisseur = ToujoursRugir("Orc", 45, 11, 3)
    cible = Personnage("Ednir", 60, 12, 5)
    message = rugisseur.agir(cible)
    verifier("message quand il rugit", message, "Orc rugit... mais ne fait rien.")
    verifier("rugir ne fait aucun dégât", cible.pv, 60)

    attaquant = JamaisRugir("Orc", 45, 11, 3)
    message = attaquant.agir(cible)
    verifier_vrai("quand il ne rugit pas, il attaque (message de attaquer)",
                  "inflige" in message and cible.pv < 60, f"message : {message!r}")

    def compter():
        rugissements = 0
        for _ in range(4000):
            if "rugit" in Monstre("Orc", 45, 11, 3).agir(Personnage("Ednir", 60, 12, 5)):
                rugissements += 1
        return rugissements

    rugissements, texte = sans_affichage(compter)
    verifier("agir ne fait aucun print", texte, "")
    verifier_vrai("environ 25 % de rugissements", 0.22 <= rugissements / 4000 <= 0.28,
                  f"obtenu : {rugissements / 40:.1f} %")


bilan()
