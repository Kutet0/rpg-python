import pygame
from moteur.personnages import Personnage

def hex_vers_rgb(code):
    code = code.lstrip("#")
    r = code[0:2]
    g = code[2:4]
    b = code[4:6]
    return (int(r, 16), int(g, 16), int(b, 16))

FOND = hex_vers_rgb("#191923")
BLANC = hex_vers_rgb("#F0F0F0")
GRIS = hex_vers_rgb("#50505A")
JAUNE = hex_vers_rgb("#FAD23C")
BLEU = hex_vers_rgb("#4682DC")
ROUGE = hex_vers_rgb("#C83C3C")
VERT = hex_vers_rgb("#3CBE5A")
ORANGE = hex_vers_rgb("#E69628")

def dessiner_texte(ecran, police, texte, x, y, couleur=BLANC):
    image = police.render(texte, True, couleur)
    ecran.blit(image, (x, y))

def couleur_barre(ratio):
    if ratio > 0.50:
        return VERT
    elif 0.20 < ratio <= 0.50:
        return ORANGE
    else:
        return ROUGE

def dessiner_barre_pv(ecran, x, y, perso, largeur=200, hauteur=16):
    pygame.draw.rect(ecran, GRIS, (x, y, largeur, hauteur))
    barre_pv = largeur * perso.ratio_pv
    couleur_pv = couleur_barre(perso.ratio_pv)
    pygame.draw.rect(ecran, couleur_pv, (x, y, barre_pv, hauteur))
    pygame.draw.rect(ecran, BLANC, (x, y, largeur, hauteur), 2)


