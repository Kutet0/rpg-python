import pygame

pygame.init()
ecran = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mon RPG")
horloge = pygame.time.Clock()

en_cours = True
frame = 0
while en_cours:
    # 1. Événements
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    # 2. Mise à jour
    frame += 1
    pygame.display.set_caption(f"Mon RPG - {round(horloge.get_fps())} FPS")

    # 3. Dessin
    ecran.fill((frame % 256, 25, 35))
    pygame.display.flip()
    horloge.tick(60)

pygame.quit()