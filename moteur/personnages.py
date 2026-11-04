from abc import ABC, abstractmethod
from moteur.exceptions import ActionImpossible
import random

BESTIAIRE = [
    {"nom": "Gobelin", "pv": 30, "attaque": 9, "defense": 2},
    {"nom": "Loup", "pv": 35, "attaque": 11, "defense": 1},
    {"nom": "Orc", "pv": 45, "attaque": 11, "defense": 3},
]

class Personnage(ABC):
    CHANCE_ESQUIVE = 0.15
    CHANCE_CRITIQUE = 0.10

    def __init__(self, nom, pv_max, attaque, defense):
        self.nom = nom
        self.pv_max = pv_max
        self._pv = pv_max
        self.attaque = attaque
        self.defense = defense

    def __repr__(self):
        return f"{type(self).__name__}('{self.nom}', pv={self._pv}/{self.pv_max})"

    @property
    def est_vivant(self):
        return self._pv > 0

    @property
    def ratio_pv(self):
        ratio = self._pv / self.pv_max
        return ratio

    @property
    def pv(self):
        return self._pv

    @pv.setter
    def pv(self, valeur):
        self._pv = max(0, min(valeur, self.pv_max))

    def attaquer(self, cible):
        if random.random() < self.CHANCE_ESQUIVE:
            return f"{cible.nom} esquive l'attaque de {self.nom} !"
        if random.random() < self.CHANCE_CRITIQUE:
            degats = self.calculer_degats(cible) * 2
            cible.pv -= max(0, min(degats, cible.pv_max))
            return f"CRITIQUE ! {self.nom} inflige {degats} dégâts à {cible.nom} !"
        degats = self.calculer_degats(cible)
        cible.pv -= max(0, min(degats, cible.pv_max))
        return f"{self.nom} inflige {degats} dégâts à {cible.nom}."

    def calculer_degats(self, cible):
        degats = (self.attaque + random.randrange(-2, 3, 1)) - cible.defense
        if degats < 1:
            degats = 1
        return degats

class Heros(Personnage):
    NOM_CAPACITE = ""
    SOIN_POTION = 20

    def __init__(self, nom, pv_max, attaque, defense, potions=3):
        super().__init__(nom, pv_max, attaque, defense)
        self.potions = potions

    def boire_potion(self):
        if self.potions == 0:
            raise ActionImpossible("Plus de potion !")
        elif self._pv == self.pv_max:
            raise ActionImpossible("Tu as déjà tous tes PV.")
        else:
            self.potions -= 1
            self.pv += self.SOIN_POTION

        return f"{self.nom} boit une potion : {self._pv}/{self.pv_max} PV."

    @abstractmethod
    def capacite_speciale(self, cible):
        ...

class Guerrier(Heros):
    NOM_CAPACITE = "Coup puissant"
    def __init__(self, nom):
        super().__init__(nom, pv_max=60, attaque=12, defense=5)

    def capacite_speciale(self, cible):
        if random.random() < 0.30:
            return f"{self.nom} rate son coup puissant !"
        else:
            degats = self.calculer_degats(cible) * 3 // 2
            cible.pv -= max(0, min(degats, cible.pv_max))
            return f"{self.NOM_CAPACITE} ! {self.nom} inflige {degats} dégâts à {cible.nom} !"


class Mage(Heros):
    NOM_CAPACITE = "Boule de feu"
    COUT_SORT = 10
    def __init__(self, nom):
        super().__init__(nom, pv_max=40, attaque=8, defense=2)
        self.mana = 30

    def capacite_speciale(self, cible):
        if self.mana < self.COUT_SORT:
            raise ActionImpossible("Pas assez de mana !")
        else:
            self.mana -= self.COUT_SORT
            degats = random.randrange(15, 21)
            cible.pv -= max(0, min(degats, cible.pv_max))
            return f"{self.NOM_CAPACITE} ! {degats} dégâts à {cible.nom} (mana : {self.mana})."

class Monstre(Personnage):
    CHANCE_RUGIR = 0.25

    def agir(self, cile):
        if random.random() < self.CHANCE_RUGIR:
            return f"{self.nom} rugit... mais ne fait rien."
        else:
            return self.attaquer(cile)

    @classmethod
    def depuis_dict(cls, donnees):
        return cls(donnees["nom"], donnees["pv"], donnees["attaque"], donnees["defense"])

    @classmethod
    def aleatoire(cls):
        choix = cls.depuis_dict(random.choice(BESTIAIRE))
        return choix