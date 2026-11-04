from abc import ABC, abstractmethod

from moteur.exceptions import ArmeCassee

class Objet(ABC):
    def __init__(self, nom):
        self.nom = nom

    @abstractmethod
    def utiliser(self):
        ...

class Potion(Objet):
    def __init__(self, nom, soin):
        super().__init__(nom)
        self.soin = soin

    def utiliser(self):
        pass

class Arme(Objet):
    def __init__(self, nom, degats, durabilite_max):
        super().__init__(nom)
        self.degats = degats
        self.durabilite_max = durabilite_max
        self._durabilite = durabilite_max

    def __repr__(self):
        return f"Arme('{self.nom}', dégats={self.degats}, durabilité={self.durabilite}/{self.durabilite_max})"

    def utiliser(self):
        if self._durabilite == 0:
            raise ArmeCassee("Arme est cassée !")
        self.durabilite -= 1
        degats = self.degats
        return degats

    def reparer(self):
        self.durabilite = self.durabilite_max

    @property
    def durabilite(self):
        return self._durabilite

    @durabilite.setter
    def durabilite(self, valeur):
        self._durabilite = max(0, min(valeur, self.durabilite_max))

    @property
    def est_cassee(self):
        return self._durabilite == 0

    @classmethod
    def depuis_texte(cls, text):
        nom, degat, durabilite = text.strip().split(":")
        return cls(nom, int(degat), int(durabilite))

class ArmeMagique(Arme):
    def __init__(self, nom, degats, durabilite_max, bonus):
        super().__init__(nom, degats, durabilite_max)
        self.bonus = bonus

    def utiliser(self):
        if self._durabilite == 0:
            raise ArmeCassee("Arme est cassée !")
        self.durabilite -= 1
        degats = self.degats + self.bonus
        return degats
