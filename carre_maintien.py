import pygame
from affichage import FOND

def main():
    pygame.init()
    ecran = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mon RPG")
    horloge = pygame.time.Clock()

    en_cours = True
    frame = 0
    x = 0
    y = 0
    while en_cours:
        # 1. Événements
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    en_cours = False
                elif evenement.key == pygame.K_RIGHT:
                    x += 10


        # 2. Mise à jour
        frame += 1

        # 3. Dessin
        ecran.fill(FOND)


        pygame.display.flip()
        horloge.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()