from moteur.personnages import Monstre, Guerrier, Mage
from moteur.exceptions import ActionImpossible
import time

def creation_hero():
    nom = input("Nom du hero : ")
    print("1. Guerrier  2. Mage")
    choix = input("choix : ")

    while choix != "1" and choix != "2":
        print("Choix invalide.")
        choix = input("choix : ")

    if choix == "1":
        hero = Guerrier(nom)
    elif choix == "2":
        hero = Mage(nom)
    return hero

def barre(personnage):
    pleine = round(personnage.ratio_pv * 10)
    vide = 10 - pleine
    return f"{personnage.nom} [{'#' * pleine}{'-' * vide}] {personnage.pv}/{personnage.pv_max}"

def combat(hero, monstre):
    while hero.est_vivant and monstre.est_vivant:
        print(barre(hero))
        print(barre(monstre))
        print(f"1. Attaquer  2. {hero.NOM_CAPACITE}  3. Potion ({hero.potions})  4. Fuir")
        choix = input("choix  : ")

        if choix == "4":
            print("Tu prends la fuite !")
            break

        try:
            if choix == "1":
                message = hero.attaquer(monstre)
            elif choix == "2":
                message = hero.capacite_speciale(monstre)
            elif choix == "3":
                message = hero.boire_potion()
            else:
                raise ActionImpossible("Choix invalide.")
        except ActionImpossible as e:
            print(e)
            continue

        print(message)

        if monstre.est_vivant:
            time.sleep(1)
            attaque = monstre.agir(hero)
            print(attaque)

    if hero.est_vivant and not monstre.est_vivant:
        print(f"Victoire ! {monstre.nom} est vaincu.")
    elif not hero.est_vivant and monstre.est_vivant:
        print(f"Defaite... {hero.nom} est tombé au combat.")


def main():
    hero = creation_hero()

    monstre = Monstre.aleatoire()
    print(f"Un {monstre.nom} sauvage apparaît !")

    combat(hero, monstre)

if __name__ == "__main__":
    main()