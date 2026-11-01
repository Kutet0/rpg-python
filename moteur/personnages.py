from contextlib import AbstractContextManager


class Personnage(AbstractContextManager):
    def __init__(nom, pv_max, attaque, defense):
        