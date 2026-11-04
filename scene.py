import pygame
from moteur.personnages import Guerrier, Monstre
from affichage import BLEU, ROUGE, GRIS, BLANC, FOND, dessiner_texte, dessiner_barre_pv

def rectangle(ecran, x, y, largeur, hauteur, couleur):
    pygame.draw.rect(ecran, couleur, (x, y, largeur, hauteur))

def main():
    pygame.init()
    ecran = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mon RPG")
    horloge = pygame.time.Clock()

    hero = Guerrier("Ednir")
    monstre = Monstre.aleatoire()

    en_cours = True
    frame = 0
    while en_cours:
        # 1. Événements
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False

        # 2. Mise à jour
        frame += 1
        if frame % 10 == 0:
            monstre.pv -= 1

        # 3. Dessin
        ecran.fill(FOND)

        rectangle(ecran, 150, 200, 80, 120, BLEU)
        rectangle(ecran, 550, 170, 80, 120, ROUGE)

        police = pygame.font.Font(None, 30)
        dessiner_texte(ecran, police, hero.nom,90, 120)
        dessiner_texte(ecran, police, monstre.nom,500, 90)

        dessiner_barre_pv(ecran,90, 150, hero)
        dessiner_barre_pv(ecran, 500, 120, monstre)

        dessiner_texte(ecran, police, f"{hero.pv}/{hero.pv_max}", 300, 148)
        dessiner_texte(ecran, police, f"{monstre.pv}/{monstre.pv_max}", 710, 118)

        rectangle(ecran, 0, 400, 800, 200, GRIS)
        pygame.draw.line(ecran, BLANC,(250,410), (250, 590), 2)

        pygame.display.flip()
        horloge.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()