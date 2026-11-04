"""Un faux Jeu pour tester les états sans ouvrir de fenêtre."""


class JeuFactice:
    def __init__(self):
        self.etat = None
        self.police = None
        self.grande_police = None

    def changer_etat(self, nouvel_etat):
        self.etat = nouvel_etat
