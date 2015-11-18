# -*- coding: utf-8 -*-
"""
					Dinosaur Safari v3
		BELLION Bastien P2D Promotion JOSEPHSON ESEO 2015/2016
			Projet d'informatique Premier semestre
"""

global dev_mod 
dev_mod = True # Variable qui permet d'accèder a certaine fonctionaliter

import time		# Importation du module de temps
import random   # Importation de random pour les deplacements teleporteur
import pygame   # Importation de pygame pour l'affichage dans une fenetre
import classe   # Importation du fichier contenant les class
import Fonction # Importation du fichier contenant certaines fonctions


from math 		   import *
from classe 	   import *
from Fonction 	   import *
from pygame.locals import *

def setup(): # Fonction executer au demarage Declaration des global, et parametrage pygame
	
	pygame.init() # Initialisation pygame
	pygame.font.init() # Initialisation du module de police



	global dim_y # Variable qui contient le nombre de case en hauteur du terrain
	global dim_x # Variable qui contient le nombre de case en largeur du terrain
	global menu # Variable qui determine dans qu'elle menu on se trouve
	global niveau # Variable qui contient le niveau dans lequel est le perso en se moment
	global volume # Variable qui contient le volume de l'audio
	global resolution # Variable qui contient la resolution de l'écrans créer	

	dim_x = 16
	dim_y = 9
	menu = 1
	niveau = 1
	volume = 5 # valeur alant de 10 pour 100% a 0 pour 0%
	resolution=[1280, 720]


	global element # Variable qui contient les objet (personnage et dino) se deplacent sur la carte
	
	element = []
	element.append(Personnage(int(dim_x / 2), int(dim_y / 2))) 
	# Creation de l'objet personnage, on le place au milieu du terrain
	element[0].image = resize(element[0].image, dim_x, dim_y, resolution) # Redimension de l'image


	global fenetre

	fenetre = pygame.display.set_mode((resolution[0], resolution[1])) # On créer une fenetre de 1280 par 720 pixel
	
def initialisation(): # Fonciton qui réalise toute les actions a faire avant de lancer une partie
	setup()
	creation_dino(nombre_dino(niveau))
	fenetre.blit(element[0].image, (0, 0))
	affichage()
	pygame.display.flip()
	changement_volume()

def affichage(): # Fonction qui affiche dans la console le terrain
	
	fond =  pygame.image.load("Ressource/image/Pelouse.jpg") # Variable qui contient le background
	fond_score = pygame.image.load("Ressource/image/fond_score.jpg")
		
	fenetre.blit(fond, (0, 0)) # On affiche le fond
	fenetre.blit(fond_score, (0,resolution[1]))

	echel_x = float(resolution[0]) / float(dim_x + 1) # On cherche a quel échel on doit afficher nos dinos pour que les images ne se superpose pas
	echel_y = float(resolution[1]) / float(dim_y)


	for i in range(0, len(element)): # On parcourt tout les élément
		if element[i].mort == False: # On vériefie que l'un des dino n'est pas mort
			fenetre.blit(element[i].image, (element[i].x * echel_x,element[i].y * echel_y)) # On affiche les éléments vivants
		elif not i == 0:
			fenetre.blit(element[i].image_mort, (element[i].x * echel_x,element[i].y * echel_y)) # On affiche les éléments mort

	position = [120, 550, 885, 1200] # Position des différents score
	score = calcule_score() # On recupère le score
	font_score = pygame.font.Font("Ressource/texte/font/Score.ttf", 25) # On charge la police d'écritures pour le score

	for i in range(0, len(score)): # On parcourt les scores
		score_render = font_score.render(str(score[i]), 16,(0,0,0)) # On créer l'image de texte
		fenetre.blit(score_render, (position[i], resolution[1] + 3)) # On l'affiche sur la fenetre

	score_render = font_score.render(str(element[0].charge_stp), 16,(0,0,0)) # On créer l'image du nombre de charge stp
	fenetre.blit(score_render, (position[3], resolution[1] + 3)) # On affiche sur la fenetre le nombre de charge
	
	pygame.display.flip() # On actualise l'affichage

def tour_joueur(): # Fonction qui fait jouer le joeur
	
	tour_jouer = True # Variable qui permet de dire si le joueur a jouer
	valeur_touche = [K_KP8, K_KP2, K_KP6, K_KP4, K_KP9, K_KP7, K_KP3, K_KP1] # Liste qui contient le nom des touches

	while tour_jouer: # Tant que le joueur na pas jouer
		if pygame.mouse.get_pressed()[0]: # Si le joueur fait un clique souri
			stp() # On appel la fonction qui gère le teleporteur
			tour_jouer = False # Le joueur a jouer

		for event in pygame.event.get(): # On parcour les touches du clavier

			if event.type == QUIT: # Si touche "espace" 
				pygame.quit()

			if event.type == KEYDOWN: # Si une touche a ete enfoncer
				for touche in range(1, 9): # On parcour les touches pour savoir la quel
					if event.key == valeur_touche[touche-1] and deplacement_possible()[touche - 1]: # Si la touche a été appuyer
						deplacement(touche,0) # On appel la fonction déplacement qui va déplacer le personnage
						tour_jouer = False # Le joueur a appuyer sur une touches

				if event.key == K_KP5: # Le joueur recharge sont teleporteur
					element[0].charge_stp+=1 # On ajoute une charge au teleporteur
					tour_jouer = False # Le joueur a jouer

				if event.key == K_SPACE and dev_mod: 
				# Dispo uniquement en dev mode, si appuye espace relance la map avec les meme paramêtre
					reset()
					tour_jouer = False

	son_pas(volume)	

def deplacement(valeur_deplacement,i): # Fonction qui gere les deplacements

	if valeur_deplacement == 1 and element[i].y > 0: # Fait monter le personage d'une case
		element[i].y -= 1 

	if valeur_deplacement == 2 and element[i].y < dim_y - 1: # Fait descendre le personage d'une case
		element[i].y += 1 

	if valeur_deplacement == 3 and element[i].x < dim_x: # Deplace le perso a droite
		element[i].x += 1 

	if valeur_deplacement == 4 and element[i].x > 0: # Deplace le perso a gauche
		element[i].x -= 1 

	if valeur_deplacement == 5 and element[i].y > 0 and element[i].x < dim_x: # Deplace haut droite
		element[i].x += 1
		element[i].y -= 1

	if valeur_deplacement == 6 and element[i].y > 0 and element[i].x < dim_x: # Deplace haut gauche
		element[i].x -= 1
		element[i].y -= 1

	if valeur_deplacement == 7 and element[i].x < dim_x and element[i].y < dim_y - 1: # Deplace bas droite
		element[i].x += 1
		element[i].y += 1

	if valeur_deplacement == 8 and element[i].x > 0 and element[i].y < dim_y - 1: # Deplace bas gauche
		element[i].x -= 1
		element[i].y += 1

def spawn_dino(distance): # Fonction qui place un dino

	position_trouver = True # Variable permetant d'arreter de generer des position

	while position_trouver: # Tant qu'une position convenable n'a pas ete trouvé
		
		y = random.randint(0,dim_y-1) # Genere une position en y
		x = random.randint(0,dim_x-1) # Genere une position en x
		
		test_y = sqrt((y - element[0].y) ** 2) # On prend la distance absolue en y
		test_x = sqrt((x - element[0].x) ** 2) # On prend la distance absolue en x
		
		for i in range(0,len(element)):
			if not (x == element[i].x and y == element[i].y): # Si le dino n'est pas sur la même position qu'un autre
				if (sqrt(test_y ** 2 + test_x ** 2)) > distance: # Si le Dino n'est pas trop pres
					position_trouver = False # La position a ete trouver

	return x,y # Retourne la position qui été trouvé

def creation_dino(n_dino): # Fonction qui créé les dinos

	for repetition in range(n_dino[0]): # On fait rèpeter l'opération pour le nombre de acr
		
		x, y = spawn_dino(4) # On génère une position
		element.append(DinoAcr(x, y))
		# On les attributs a un nouvel objet

		element[len(element) - 1].image = resize(element[len(element) - 1].image, dim_x, dim_y, resolution)
		element[len(element) - 1].image_mort = resize(element[len(element) - 1].image_mort, dim_x, dim_y, resolution)
		# On redimensionne les images pour qu'elles rentre dans le cadre peut importe la taille de la carte

	for repetition in range(n_dino[1]): # On fait rèpeter l'opération pour le nombre de car
		
		x, y = spawn_dino(6) # On génère une position
		element.append(DinoCar(x, y))
		# On les attributs a un nouvel objet

		element[len(element) - 1].image = resize(element[len(element) - 1].image, dim_x, dim_y, resolution)
		element[len(element) - 1].image_mort = resize(element[len(element) - 1].image_mort, dim_x, dim_y, resolution)
		# On redimensionne les images pour qu'elles rentre dans le cadre peut importe la taille de la carte

def deplacement_dino(): # Fonction qui gère le déplacement des dinos

	equivalence = [1, 6, 4, 8, 2, 7, 3, 5, 1] # Tableau des équivalence deplacement dino/perso

	for i in range(1, len(element)): # On parcourt le tableau des élément a partir de l'index 1
		
		if element[i].mort == False: # Si le dino n'est pas mort on ne le fait plus bouger
			
			for plusieur_dep in range(0, element[i].porte): # Repetition en si le dino a plusieur deplacement
				angle = 0 # Création d'une variable qui contiendrat l'angle
		
				if element[i].x == element[0].x and element[i].y == element[0].y: # Si l'élément n'est pas deja sur le personnage
					plusieur_dep = element[i].porte - 1 # Si un dino qui a plusieur de porter est sur le perso il ne se redeplace pas
		
				else:

					vabs_y = sqrt((element[i].y - element[0].y) ** 2) # On prend la distance absolue en y
					vabs_x = sqrt((element[i].x - element[0].x) ** 2) # On prend la distance absolue en x
					angle = degrees(acos((element[i].y - element[0].y) / (sqrt(vabs_y ** 2 + vabs_x ** 2)))) # On calcule l'ange formule:
					""" angle = Arccos((distance en entre le dino et le perso/(la norme)"""
		
					if element[i].x < element[0].x: # Si le dino se trouve a gauche du personnage
						angle = 360 - angle # On ajuste l'angle

				for tranche in range(0, 9): # On parcour les differentes tranche de deplacement
						
					if 45 * tranche - 22.5 < angle < 22.5 + 45 * tranche: # On cherche dans quel tranche se trouve l'angle
						deplacement(equivalence[tranche], i) # On effectue le déplacement correspondant la tranche

def stp(): # Fonction qui gère le STP
	
	if element[0].charge_stp == 0: # Si il n'y a pas de charge STP

		while pygame.mouse.get_pressed()[0]: # Tant que le joueur n'a pas relaché le clique
			for event in pygame.event.get(): # On met a jour les informations d'événement
				pass

		element[0].x = random.randint(0, dim_x - 1) # On créer une nouvel position complètement aléatoire
		element[0].y = random.randint(0, dim_y - 1)

		son_pas(volume)

	else: # Si il y a une ou plusieur charge STP

		while pygame.mouse.get_pressed()[0]: # Tant que le joueur n'a pas relacher le clique

			for event in pygame.event.get(): # On met a jour les informations d'événement
				pass

			position_souri = pygame.mouse.get_pos()
			if position_souri[0] < dim_x * int(resolution[0] / dim_x + 1): # Si la souri ne sort pas du cadre
				if position_souri[1] < dim_y * int(resolution[1] / dim_y + 1):
					element[0].x = int(position_souri[0] / (resolution[0] / dim_x + 1)) # On change la position du peronnage
					element[0].y = int(position_souri[1] / (resolution[1] / dim_y + 1)) # par celle de la souri
			affichage() # On affiche le nouvel emplacement du personnage

		element[0].charge_stp -= 1 # On retire une charge du STP

def mort(): # Fonciton qui gère la mort des dinos et du joueur
	global menu
	global niveau

	for i in range(0, len(element)): # On parcour une première fois les éléments
		for j in range(0, len(element)): # On parcour une seconde fois les éléments
			if not element[0].mort and element[i].x == element[j].x and element[i].y == element[j].y and not i == j: 
			# Si deux éléments différents sont à la même position 
				
				if i == 0  or j == 0: # Si l'un des deux est le joueur
					if not (element[i].mort or element[j].mort): # Si le dino n'est pas mort
						menu = 0
						niveau = 1
						if dev_mod:

							print "mort"
			
						element[0].action_mort()


						j = len(element) - 1
						i = len(element) - 1


						while pygame.mixer.get_busy(): # Tant que le son est actif
							for event in pygame.event.get(): # On parcour les touches du clavier
								if event.type == QUIT: # Si touche "espace" 
									pygame.quit()

							affichage() # On affiche pour montrer que le personnage est sur la meme case qu'un dino

				else: # Sinon c'est deux dinos

					element[i].action_mort()
					element[j].action_mort()

def reset(): # Fonciton qui remet a zéros le niveau en cour

	del(element[:]) # Suppression de tout les objet contenu dans element
	element.append(Personnage(int(dim_x / 2), int(dim_y / 2))) # Creation de l'objet personnage, on le place au milieu du terrain
	element[0].image = resize(element[0].image, dim_x,dim_y, resolution) # Redimension de l'image
	creation_dino(nombre_dino(niveau)) # Fonction qui vient remettre a zéros tout les objets
	changement_volume()
	affichage()

def deplacement_possible(): # Fonction qui détermine ou le personnage peut se deplacer
	
	possible=[True,True,True,True,True,True,True,True] # Tableau qui contient quel deplacement est possible
	
	x = element[0].x # On enregistre la position actuel du personnage
	y = element[0].y

	for move in range(0, 8): # On parcourt les déplacement

		deplacement(move + 1, 0) # On réalise le deplacement

		for dino in range(1, len(element)): # On parcourt les dino
			if element[0].x == element[dino].x and element[0].y == element[dino].y and (not element[dino].mort):
				# On regarde si après le deplacement le personnage est sur la même case qu'un dino vivant
				possible[move] = False # Si c'est le cas on ne peut pas se deplacer sur cette case
		
		if element[0].x == x and element[0].y == y: # Si le joueur a fait un deplacement contre un mur
			possible[move] = False # Si c'est le cas ca ne compte pas
		
		element[0].x = x # On rement le personnage sur sa case avant le deplacement
		element[0].y = y

	return possible # On retourne la liste des deplacement possible

def calcule_score(): # Fonction qui calcule le score actuel du joueur

	score = [0,0,0] # Créer une variable locale
	
	for i in range(1,len(element)): # On parcourt les dinos
		if element[i].mort: # Si le dinos est mort

			score[element[i].valeur - 1] += 1 # On incrememente la variable du nombre de dino mort

	for type_dino in range(1,3): # On passe d'un type de dino a un autre
		for level in range(1,niveau): # On parcourt les différents niveau accomplit

			score[type_dino] += nombre_dino(level)[type_dino-1] # On incrémente les variables de dino mort correspondant

	score[0] = score[1] * 3 + score[2] * 5 # On calcule le score celon les dinos morts

	return score # On retourne le scort

def niveau_suivant(): # Détermine si on doit passer au niveau suivant
	global niveau # On fait appel aux variables pour pouvoir es modifiers
	global dim_x
	global dim_y

	next_level = False # Variable qui dit si on doit passer au prochain niveau
	compteur_mort = 0 # Variable qui compte le nombre de dino mort

	for i in range(1, len(element)): # On parcourt tout les dinos
		if element[i].mort: # Si le dino est mort
			compteur_mort += 1 # On increment le compteur

	if compteur_mort == len(element) - 1: # Si il y a autant de mort que de dino
		
		niveau += 1 # On passe au niveau suivant
		
		dim_x = 16 * int((10 + niveau) / 10) # Agrandit la grille pour faire passer tout les dinos
		dim_y = 9 * int((10 + niveau) / 10)

		reset() # On remet a zéros avec de nouveau paramètre
		affichage() # On affiche les nouveaux paramètres

def changement_volume(): # Fonction qui change le volume de tout les sons

	for i in range(0, len(element)): # On parcourt les éléments
		element[i].son_mort.set_volume(float(volume) / 10) # On met les sons des mort au bon volume

def menu_principale(): # Fonction 
	global menu # On fait appel a la variable pour pouvoir la modifier

	for event in pygame.event.get(): # On regarde les evenement
		if event.type == QUIT: # Si la croix est cliqué
			quit() # On quitte le programme

		if pygame.mouse.get_pressed()[0]:
			menu = 1

def animation_semple():
	global fenetre

	fin_animation = True
	couleur = [(0, 0, 0), (239, 216, 7)]

	animation = []

	objet_animation = open("Ressource/animation/lancement.txt", 'r')

	for ligne in objet_animation:
		animation.append(ligne[0:len(ligne) - 1])

	x = len(animation[0])
	y = len(animation)



	display = []
	
	for colonne in range(len(animation)):
		display.append([0] * len(animation[colonne]))

	debut = time.time() * 1000


	while fin_animation:
		for event in pygame.event.get():
			
			if event.type == QUIT: # Si touche "espace" 
				quit()
			
			if event.type == KEYDOWN:
				fin_animation = False

		intervalle = int((time.time() * 1000 - debut) / 50)

		for ligne in range(0, intervalle):
			
			if ligne >= y:
				ligne = y - 1
			
			for colonne in range(0, intervalle - ligne):
				if colonne >= x:
					colonne = x - 1
				display[ligne][colonne-1] = animation[ligne][colonne]

		echel_x = resolution[0] / x 
		echel_y = resolution[1] / y

		for ligne in range(0, y):
			for colonne in range(0, x):
				position = (echel_x * colonne, echel_y * ligne, echel_x, echel_x)
				pygame.draw.rect(fenetre, couleur[int(display[ligne][colonne - 1])], position)

		pygame.display.flip() # On actualise l'affichage

		if intervalle == x + y - 2:

			fin_animation = False




setup()

animation_semple()
fenetre = pygame.display.set_mode((resolution[0], resolution[1] + 30))
while 1:
	if menu ==0:
		menu_principale()
		
	if menu == 1:
		reset()
		while menu == 1:
			tour_joueur()
			deplacement_dino()
			mort()
			affichage()
			niveau_suivant()