import pygame
from pygame import mixer
import random 
import time 
from classes import Tank, Shell, Bonus
import sys
pygame.init()

FPS = 60

display_width = 1324  
display_height = 600

numbers_of_tanks = 0
level = 1

black = (0,0,0)       
white = (255,255,255)
red = (200,0,0)
gold = (255,215,0)
green = (0,200,0)
grey = (133,133,133)
bright_red = (255,0,0)
bright_green = (0,255,0)
bright_grey= (84,84,84)

enemy_width = 50
enemy_height = 30

recharge = 0

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("MY GAME")

clock = pygame.time.Clock()

backgroundImg = pygame.image.load('fon.jpg').convert()
backgroundImg = pygame.transform.scale(backgroundImg , (display_width,display_height))

angarImg = pygame.image.load('angar.jpg').convert()
angarImg = pygame.transform.scale(angarImg , (display_width,display_height))

pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.mixer.init()
shot_sound = pygame.mixer.Sound('Shot.ogg')

player_height = 50
player_width = 100

pause = False
			
def draw_interface(norm_shell , gold_shell , health , level):
	"""
	Create a counter of player's heals, good and norm shells
		
	Parametres:
	-----------
		
	norm_shell: int
		Numbers of player's norm shells
	gold_shell: int
		Numbers of player's gold shells
	health: int
		Numbers of player's health_point
	"""
	
	font = pygame.font.SysFont(None, 50)
	health_point = font.render("Your health point:" + str(health) , True , red)
	norm_shells = font.render("" + str(norm_shell) , True ,black )
	gold_shells = font.render("" + str(gold_shell) , True ,gold )  
	level = font.render("LEVEL:" + str(level) , True , black ) 
	gameDisplay.blit(norm_shells,(50 ,display_height - 50))
	gameDisplay.blit(gold_shells,(200 ,display_height - 50))
	gameDisplay.blit(health_point,(400 ,display_height - 50 ))
	gameDisplay.blit(level , (100 , 0) ) 
	
def text_objects(text,font):
	textSurface = font.render(text,True,black)
	return textSurface , textSurface.get_rect()

def message_display(text):
	"""
	Draws text on the game_Display
	
	"""
	largeText = pygame.font.Font("11601.ttf" ,110)
	TextSurf , TextRect = text_objects(text,largeText)
	TextRect.center = ((display_width/2) , (display_height/2))
	gameDisplay.blit(TextSurf , TextRect)
	
	pygame.display.update()
	time.sleep(4)
	

def draw_angar():	
	"""
	Draws a hangar with tanks for the game, by clicking
	the mouse in one of the tanks begins the gameplay with
	the selected tank
	
	Parametres:
	-----------
	numbers_of_player: int
		numbers of different tanks
	
	start_x , xtart_y : int
		coords of first image at the Display
	
	size_x , size_y : int
		Sizes of images 	
	
	
	"""
	global shot_sound
	gameDisplay.blit(angarImg , [0,0])
	number_of_players = 3 
	startx = 150
	starty = 100
	size_x = 200
	size_y = 400 		
	coord_x = []

	for i in range(number_of_players):
		player_name = "Player" + str(i+1) + ".png"
		image = pygame.image.load(player_name).convert_alpha()
		image = pygame.transform.scale(image , (size_x, size_y)) 
		image = pygame.transform.rotate(image , 180)
		coord_x.append(startx)
		gameDisplay.blit(image , (startx , starty))	
		startx += size_x + 50
	pygame.display.update()
	clock.tick(10)
		
	angar = True

	while angar:
		click_mouse = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()			
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 :
						if  coord_x[0] < click_mouse[0] < coord_x[0] + size_x and starty < click_mouse[1]  < starty + size_y : 
							player = Tank(player_width // 2, display_height // 2, player_width, player_height,
							"Player_1.png", 0.7, 200, 20, 200, 1, gameDisplay, shot_sound)
							angar = False

						if  coord_x[1] < click_mouse[0]  < coord_x[1] + size_x and starty < click_mouse[1]  < starty + size_y :
							player = Tank(player_width // 2, display_height // 2, player_width, player_height,
							"Player_2.png", 0.55, 175, 40, 300, 1, gameDisplay , shot_sound)
							angar = False

						if  coord_x[2] < click_mouse[0]  < coord_x[2] + size_x and starty < click_mouse[1]  < starty + size_y : 
							player = Tank(player_width // 2, display_height // 2, player_width, player_height,
							"Player_3.png", 0.4, 100, 70, 400, 1, gameDisplay , shot_sound)
							angar = False

						game_loop(player)

						
						
		

def button(msg,x,y,w,h,ic,ac,action = None):
	"""
	Draws a rectangle with the text. At the click of a mouse, 
	this or that action takes place
	
	Parameters:
	-----------
	msg: str
		message, that will be in the rect
	
	x , y : int
		X and Y Coordinates of the upper-left corner of the rectangle
	
	w , h : int
		width and height of rect with message
		
	ic: str
		color of the rectangle when the mouse is not on it
	
	ac : str
		color of the rectangle when the mouse is on it
	"""
	
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if (x + w > mouse[0] > x) and y + h > mouse[1] > y:
		pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
		if click[0] == 1 and  action != None:
			if action == "play":
				draw_angar()
			elif action == "continue":
				unpaused()	
			elif action == "quit":
				pygame.quit()
				quit()
	else:
		pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
	
	smallText = pygame.font.Font("11601.ttf" ,20)
	textSurf , textRect = text_objects(msg,smallText)
	textRect.center = ((x + (w/2)) , (y + (h/2)))
	gameDisplay.blit(textSurf , textRect)
 	
def game_intro():
	"""
	Draw  menu
	"""
	intro = True
	
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.blit(backgroundImg , [0,0])
		largeText = pygame.font.Font("11601.ttf" ,80)
		TextSurf , TextRect = text_objects("Battle of tanks",largeText)
		TextRect.center = ((display_width/2) , (display_height/8))
		gameDisplay.blit(TextSurf , TextRect)
		 
		button("BEGIN THE GAME",25,400,300,50,green,bright_green, "play")
		button("QUIT THE GAME",25,500,300,50,red,bright_red,"quit")
						
		pygame.display.update()
		clock.tick(50)

def unpaused():
	global pause 
	pause = False
	 
def paused():

	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(white)
		largeText = pygame.font.Font("11601.ttf" ,100)
		TextSurf , TextRect = text_objects("PAUSE",largeText)
		TextRect.center = ((display_width/2) , (display_height/8))
		gameDisplay.blit(TextSurf , TextRect)
		
		button("CONTINUE THE GAME",(display_width/2) - 200,(display_height/4),400,80,grey,bright_grey, "continue")
		button("QUIT THE GAME",(display_width/2) - 200,(display_height/2),400,80,red,bright_red,"quit")
				
		pygame.display.update()
		clock.tick(50)					

def game_loop(player):
		
	game_over = False
	global pause
	enemies = []
	shells = []
	bonuses = []
	while not game_over:
		dt = clock.tick(60) / 100.0

		click_mouse = pygame.mouse.get_pos()
		gameDisplay.fill(white)

		if pygame.key.get_pressed()[pygame.K_d]:
			if player.x + player.width/2  <= display_width/3 :
				player.x += player.velo * dt
		if pygame.key.get_pressed()[pygame.K_a]:
			if player.x - player.width/2  >= 0 :
				player.x -= player.velo * dt
		if pygame.key.get_pressed()[pygame.K_s]:
			if player.y + player.height/2  <= display_height :	
				player.y += player.velo * dt
		if pygame.key.get_pressed()[pygame.K_w]:
			if player.y - player.height/2  >= 0 :		
				player.y -= player.velo * dt

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pause = True
					paused()			
				if event.key == pygame.K_SPACE:
					new_shell = player.shot("armour-piercing")
					if new_shell != None:
						shells.append(new_shell)
				if event.key == pygame.K_LSHIFT:
					new_shell = player.shot("cumulative")
					if new_shell != None:
						shells.append(new_shell)
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 :
					if bonuses != []:
						i = 0
						while i < len(bonuses):
							player.catch(bonuses[i], click_mouse)
							i += 1



		if shells != []:
			for i in range(len(shells)):
				shells[i].draw()
				shells[i].move(dt)
			i = 0
			while i < len(shells):
				if shells[i].is_destroyed:
					shells.pop(i)
				else:
					i += 1

		if enemies != []:	
			for i in range(len(enemies)):
				tank = enemies[i]
				shells = tank.check_hits(shells)
				new_shell = tank.shot("armour-piercing")
				if new_shell != None:
					shells.append(new_shell)
				tank.move(dt)
				tank.draw()
				
			i = 0	
			while i < len(enemies) :
				if enemies[i].is_destroyed:
					enemies.pop(i)
				else:
					i += 1
	
		if shells != []:
			shells = player.check_hits(shells)
		
		
		if random.randint(0, 100) > 98:
			global numbers_of_tanks
			global level
			numbers_of_tanks += 1
			if numbers_of_tanks <= level*3:
				enemies.append(Tank(display_width, random.randint(25, display_height - 25), 100, 50, "tank_rotate20.png", 
									0.9, 100, 10, 200, -1, gameDisplay , None)) 
			if len(enemies) == 0:
				level += 1
				numbers_of_tanks = 0

		if random.randint(0, 1000) > 990:
			bonuses.append(Bonus(random.randint(100, gameDisplay.get_width()), 0, 60, 60, 10, random.randint(1, 3), "bonus10.png", gameDisplay))
		
		i = 0		
		if bonuses != []:
			while i < len(bonuses) :
				if bonuses[i].is_lost:
					bonuses.pop(i)
				else:
					bonuses[i].move()
					bonuses[i].draw()
					i += 1
		player.draw()
		player.charge()
		draw_interface(player.APshells, player.Gshells, player.health , level)
		pygame.display.update()
		if player.health <= 0:
			message_display("GAME OVER")
			game_over = True
			
			
			
		clock.tick(50)
		
game_intro()
pygame.quit()
quit()
