"""Vérification de l'exercice 1.5 — lancer depuis la racine : python -m test.verif_1_5

Lance console.py en tapant les réponses à ta place, puis lit ce qu'il affiche.
"""
import subprocess
import sys

from test.verif import bilan, groupe, verifier_vrai


def jouer(saisies):
    """Lance console.py avec ces saisies clavier, renvoie tout ce qui s'est affiché."""
    resultat = subprocess.run([sys.executable, "console.py"], input="\n".join(saisies) + "\n",
                              capture_output=True, text=True, timeout=20)
    return resultat.stdout + resultat.stderr


@groupe("1. Choix du héros, potion refusée, fuite")
def _():
    sortie = jouer(["Ednir", "9", "1", "3", "x", "4"])
    print("         --- début de ce que console.py a affiché ---")
    for ligne in sortie.strip().splitlines():
        print(f"         | {ligne}")
    print("         --- fin ---")
    verifier_vrai("pas de plantage", "Traceback" not in sortie, "console.py a planté : lis le Traceback ci-dessus")
    verifier_vrai("classe '9' refusée : affiche 'Choix invalide.'", "Choix invalide." in sortie)
    verifier_vrai("un monstre apparaît : 'sauvage apparaît !'", "sauvage apparaît !" in sortie)
    verifier_vrai("barre du Guerrier plein : '[##########] 60/60'", "[##########] 60/60" in sortie)
    verifier_vrai("menu : '2. Coup puissant' et 'Potion (3)'",
                  "2. Coup puissant" in sortie and "Potion (3)" in sortie)
    verifier_vrai("potion à PV max : 'Tu as déjà tous tes PV.'", "Tu as déjà tous tes PV." in sortie)
    verifier_vrai("action 'x' : 'Choix invalide.' deux fois en tout", sortie.count("Choix invalide.") == 2)
    verifier_vrai("le monstre n'a jamais joué (aucun tour n'a été consommé)",
                  "inflige" not in sortie and "rugit" not in sortie and "esquive" not in sortie)
    verifier_vrai("fuite : 'Tu prends la fuite !'", "Tu prends la fuite !" in sortie)
    verifier_vrai("après une fuite : ni victoire ni défaite annoncée",
                  "Victoire" not in sortie and "Défaite" not in sortie and "Defaite" not in sortie,
                  "le héros a fui : le combat n'est ni gagné ni perdu")


@groupe("2. Le Mage")
def _():
    sortie = jouer(["Zed", "2", "4"])
    verifier_vrai("pas de plantage", "Traceback" not in sortie)
    verifier_vrai("barre du Mage : '[##########] 40/40'", "[##########] 40/40" in sortie)
    verifier_vrai("menu : '2. Boule de feu'", "2. Boule de feu" in sortie)


bilan()
