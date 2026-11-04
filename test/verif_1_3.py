"""Vérification de l'exercice 1.3 — lancer depuis la racine : python -m test.verif_1_3"""
from test.verif import bilan, groupe, sans_affichage, verifier, verifier_erreur, verifier_vrai

from moteur.exceptions import ActionImpossible
from moteur.personnages import Guerrier, Heros, Mage, Personnage


@groupe("1. Heros est abstraite")
def _():
    verifier_vrai("Heros hérite de Personnage", issubclass(Heros, Personnage))
    verifier_erreur("Heros('x', 1, 1, 1) lève TypeError", TypeError, Heros, "x", 1, 1, 1)


@groupe("2. Guerrier")
def _():
    g = Guerrier("Ednir")
    verifier_vrai("Guerrier hérite de Heros", isinstance(g, Heros))
    verifier("nom", g.nom, "Ednir")
    verifier("pv_max, attaque, defense", (g.pv_max, g.attaque, g.defense), (60, 12, 5))
    verifier("PV de départ", g.pv, 60)
    verifier("potions de départ", g.potions, 3)
    verifier("NOM_CAPACITE", g.NOM_CAPACITE, "Coup puissant")
    verifier("repr (hérité de Personnage)", repr(g), "Guerrier('Ednir', pv=60/60)")


@groupe("3. Mage")
def _():
    m = Mage("Zed")
    verifier("pv_max, attaque, defense", (m.pv_max, m.attaque, m.defense), (40, 8, 2))
    verifier("mana de départ", m.mana, 30)
    verifier("COUT_SORT", m.COUT_SORT, 10)
    verifier("NOM_CAPACITE", m.NOM_CAPACITE, "Boule de feu")


@groupe("4. boire_potion()")
def _():
    g = Guerrier("Ednir")
    erreur = verifier_erreur("PV au max : lève ActionImpossible", ActionImpossible, g.boire_potion)
    if erreur:
        verifier("message de l'erreur", str(erreur), "Tu as déjà tous tes PV.")
    verifier("PV au max : aucune potion consommée", g.potions, 3)

    g.pv = 50
    message = g.boire_potion()
    verifier("à 50/60 : PV après la potion (bornés au max)", g.pv, 60)
    verifier("une potion consommée", g.potions, 2)
    verifier("message renvoyé", message, "Ednir boit une potion : 60/60 PV.")

    g.pv = 10
    g.boire_potion()
    verifier("à 10/60 : +20 PV", g.pv, 30)

    g.potions = 0
    erreur = verifier_erreur("plus de potion : lève ActionImpossible", ActionImpossible, g.boire_potion)
    if erreur:
        verifier("message de l'erreur", str(erreur), "Plus de potion !")
    verifier("plus de potion : PV inchangés", g.pv, 30)


@groupe("5. Coup puissant du Guerrier (sur 3000 essais)")
def _():
    def essayer():
        rates = 0
        degats = set()
        for _ in range(3000):
            g = Guerrier("Ednir")
            cible = Personnage("Orc", 100, 0, 0)
            message = g.capacite_speciale(cible)
            if message == "Ednir rate son coup puissant !":
                rates += 1
                if cible.pv != 100:
                    return rates, degats, "un coup raté a fait des dégâts"
            else:
                perdu = 100 - cible.pv
                degats.add(perdu)
                attendu = f"Coup puissant ! Ednir inflige {perdu} dégâts à Orc !"
                if message != attendu:
                    return rates, degats, f"message attendu {attendu!r}, obtenu {message!r}"
        return rates, degats, ""

    (rates, degats, probleme), _ = sans_affichage(essayer)
    verifier("messages corrects, aucun dégât sur un coup raté", probleme, "")
    verifier_vrai("environ 30 % de coups ratés", 0.26 <= rates / 3000 <= 0.34,
                  f"obtenu : {rates / 30:.1f} %")
    verifier("dégâts possibles contre défense 0 (10 à 14, × 3 // 2)", degats, {15, 16, 18, 19, 21})


@groupe("6. Boule de feu du Mage")
def _():
    m = Mage("Zed")
    cible = Personnage("Orc", 200, 0, 50)
    for mana_restant in (20, 10, 0):
        avant = cible.pv
        message = m.capacite_speciale(cible)
        perdu = avant - cible.pv
        verifier_vrai(f"15 à 20 dégâts, malgré une défense de 50 (mana → {mana_restant})",
                      15 <= perdu <= 20, f"PV perdus : {perdu}")
        verifier("message renvoyé", message,
                 f"Boule de feu ! {perdu} dégâts à Orc (mana : {mana_restant}).")
    avant = cible.pv
    erreur = verifier_erreur("sans mana : lève ActionImpossible", ActionImpossible,
                             m.capacite_speciale, cible)
    if erreur:
        verifier("message de l'erreur", str(erreur), "Pas assez de mana !")
    verifier("sans mana : la cible ne perd rien", cible.pv, avant)


bilan()
