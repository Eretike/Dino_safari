# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

def resize(image, x, y, resolution): # Fonction qui permet de redimensionner les images pour qu'elle soit a la bonne échel
	return pygame.transform.scale(image, (int(resolution[0] / x), int(resolution[1] / y))) 

def nombre_dino(level): # Fonction qui détermine le nombre de dino et adapte la taille de la grille
	return 3 + (2 * (level - 1)), max(0, -3 + (2 * (level - 1))) # Retourne le nombre de dinosaures celon le niveau actuel

def son_pas(volume):
	pygame.mixer.init()
	son_pas = pygame.mixer.Sound("Ressource/son/son_pas.wav")
	
	son_pas.set_volume(float(volume) / 10) # On met le volume des pas a la bonne valeur

	
	son_pas.stop() # Stop le precedent son de pas si le joueur a jouer vite
	son_pas.play() # Joue le son de pas



"""def affichage_console(x, y, element): # Fonction qui affiche dans la console  la carte
	carte = []

	for creation_ligne in range(y): # On agrandit la liste precedement creer
		carte.append([0] * x) 

	for i in range(len(element)): # On parcourt tout les élément
		if element[i].mort == False: # On vériefie que l'un des dino n'est pas mort
			carte[element[i].y][element[i].x] = element[i].valeur # On affiche sur la carte la valeur de l'element
		else:
			carte[element[i].y][element[i].x] =- 1

	print # Saut d'une ligne pour differencier le print d'avant
	for ligne in range(0, y): # Selection des listes une par une
		print carte[ligne] # Code permetant d'afficher la carte dans la console"""

