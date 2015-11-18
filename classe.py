# -*- coding: utf-8 -*-

import pygame   # Importation de pygame pour l'affichage dans une fenetre
from pygame.locals import *

class principal:

    """Classe principal qui va être mère des dinos et du personnage 
    Elle contient:
    - position en x
    - position en y
    - mort ou non"""
    def __init__ (self,position_x,position_y):
        self.x = position_x
        self.y = position_y
        self.mort = False

class Personnage(principal):

    """Classe définissant le personnage caractérisée par :
    - sa position en x
    - sa position en y
    - sa valeur sur le terrain
    - son nombre de charge STP
    - l'image sur le terrain"""

    def __init__(self, position_x, position_y):

        principal.__init__(self, position_x, position_y)
        self.valeur = 1
        self.charge_stp = 0
        self.image = pygame.image.load("Ressource/image/Gardien.jpg")
        self.son_mort = pygame.mixer.Sound("Ressource/son/son_perso_mort.wav")
        self.son_mort.set_volume(0.5)

    def action_mort(self):                   
        self.son_mort.play() # On joue le son de la mort du personnage
        self.mort = True

class mere_dino(principal):

    def __init__(self,position_x,position_y):

        principal.__init__(self, position_x, position_y)

        self.image_mort = pygame.image.load("Ressource/image/dino_mort1.png")  
        self.son_mort = pygame.mixer.Sound("Ressource/son/son_dino_mort.wav")  
        self.son_mort.set_volume(0.5)

    def action_mort(self):
        if not self.mort:
            self.mort = True

            self.son_mort.stop()
            self.son_mort.play()

class DinoAcr(mere_dino):

    """Classe définissant le dinosaure acrocanthosaurus caractérisée par:
    - sa position en x
    - sa position en y
    - sa portee en caractérisée
    - sa valeur sur le terrain"""
    
    def __init__(self,position_x,position_y):

        mere_dino.__init__(self, position_x, position_y)
        self.valeur = 2
        self.point = 3
        self.porte = 1
        self.image = pygame.image.load("Ressource/image/acr.png")

class DinoCar(mere_dino):

    """Classe définissant le dinosaure Carnotaurus caractérisée par:
    - sa position en x
    - sa position en y
    - sa portee en caractérisée
    - sa valeur sur le terrain"""
    
    def __init__(self,position_x,position_y):

        mere_dino.__init__(self, position_x, position_y)
        self.valeur = 3
        self.point = 5
        self.porte = 2
        self.image = pygame.image.load("Ressource/image/car.png")