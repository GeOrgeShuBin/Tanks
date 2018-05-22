import pygame
from pygame import mixer
import random 
import time 
from classes import Tank, Shell
pygame.init()

FPS = 60

display_width = 1324  
display_height = 600

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
  
aimImg = pygame.image.load('aim1.png').convert()
aimImg.set_colorkey(white)

backgroundImg = pygame.image.load('fon.jpg').convert()
backgroundImg = pygame.transform.scale(backgroundImg , (display_width,display_height))

angarImg = pygame.image.load('angar.jpg').convert()
angarImg = pygame.transform.scale(angarImg , (display_width,display_height))

pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.mixer.init()
shoot_gun_sound = pygame.mixer.Sound('Shot.ogg')

tank_height = 50
tank_width = 100

player_height = 50
player_width = 100

bonus_height = 100
bonus_width = 200

max_tanks = 5

pause = False
					
def initilize_tank(max_tanks , tanks_list):
	"""
	Define start coord of tanks
	Parametres:
	
	----------
	
	max_tanks: int
		maximum number of tanks at this level
	
	tanks_list: list
		list of size max_tanks, which adds the created tanks 
	"""	
	
	for i in range(max_tanks):
		tank_x = random.randrange(  1024 , 2 *display_width)
		tank_y = random.randrange(0 , display_height - tank_height)
		tanks_list.append(Tank(tank_x , tank_y))

def number_of_shell(norm_shell , gold_shell , health , score , level):
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
	score = font.render("Score:" + str(score) , True , black )  
	level = font.render("LEVEL:" + str(level) , True , black ) 
	gameDisplay.blit(norm_shells,(50 ,display_height - 50))
	gameDisplay.blit(gold_shells,(200 ,display_height - 50))
	gameDisplay.blit(health_point,(400 ,display_height - 50 ))
	gameDisplay.blit(score,(600 , 0))
	gameDisplay.blit(level , (100 , 0) ) 
	
def bonus(bonus_x , bonus_y , bonus_width , bonus_height):
	"""
	Create a bonus 
	
	Parametres:
	----------
	img_num : int
		Number of image name
	
	"""
	img_num = random.randint(0,0)
	image_filename = "bonus1" + str(img_num) + ".png"
	image = pygame.image.load(image_filename).convert_alpha()
	image = pygame.transform.scale(image , (bonus_width, bonus_height))	
	gameDisplay.blit(image,(bonus_x , bonus_y))

def shells(shellx , shelly , radius , color): 
	"""
	Create players shell
	"""
	pygame.draw.circle(gameDisplay,color , (shellx,shelly) , radius)
	
def player(image ,x,y):
	"""
	Draw a player at game_Display
	
	Parametrs:
	---------
	
	image: picture
		player image
	"""
	global recharge
	gameDisplay.blit(image,(x,y))
	if recharge > 0 :		
		pygame.draw.rect(gameDisplay , red , [ x , y - 10, int(recharge) , 10])

	
	
def text_objects(text,font):
	textSurface = font.render(text,True,black)
	return textSurface , textSurface.get_rect()

def message_display(text):
	largeText = pygame.font.Font("11601.ttf" ,110)
	TextSurf , TextRect = text_objects(text,largeText)
	TextRect.center = ((display_width/2) , (display_height/2))
	gameDisplay.blit(TextSurf , TextRect)
	
	pygame.display.update()
	time.sleep(4)
	game_loop()
	
def crash():
	"""
	This function writes a message about the loss
	"""
	message_display("You lose")

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
				pygame.quit()
				quit()			
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 :
						if  coord_x[0] < click_mouse[0] < coord_x[0] + size_x and starty < click_mouse[1]  < starty + size_y : 
							player = Tank(player_width // 2, display_height // 2, player_width, player_height,
							"Player_1.png", 1, 200, 2, 20, 1, gameDisplay)
							angar = False
							game_loop(player)		

						if  coord_x[1] < click_mouse[0]  < coord_x[1] + size_x and starty < click_mouse[1]  < starty + size_y :
							player = Tank(player_width // 2, display_height // 2, player_width, player_height,
							"Player_2.png", 0.7, 175, 4, 30, 1, gameDisplay)
							angar = False
							game_loop(player)		

						if  coord_x[2] < click_mouse[0]  < coord_x[2] + size_x and starty < click_mouse[1]  < starty + size_y : 
							player = Tank(player_width // 2, display_height // 2, player_width, player_height,
							"Player_3.png", 0.5, 100, 7, 40, 1, gameDisplay)
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
		button("ENTER THE GAME",25,500,300,50,red,bright_red,"quit")
						
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
		
	gameExit = False
	global pause
	enemies = []
	shells = []
	while not gameExit:
		dt = clock.tick(60) / 10

		click_mouse = pygame.mouse.get_pos()
		gameDisplay.fill(white)

		if pygame.key.get_pressed()[pygame.K_d]:
			player.x += player.velo * dt
		if pygame.key.get_pressed()[pygame.K_a]:
			player.x -= player.velo * dt
		if pygame.key.get_pressed()[pygame.K_s]:
			player.y += player.velo * dt
		if pygame.key.get_pressed()[pygame.K_w]:
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
					shells = player.shot("armour-piercing", shells)	
					print("shooting")				
				if event.key == pygame.K_LSHIFT:
					shells = player.shot("cumulative", shells)	
			"""	
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 :
					if bonuses != []:
						for i in range(len(bonuses)):
							bonus = bonuses[i]
							if (click_mouse[0] < bonus.x + bonus.width and click_mouse[0] > bonus.x
								and click_mouse[1] < bonus.y and click_mouse[1] > bonus.y + bonus.height):
								player.use_bonus(bonus.kind)
			"""
				
		if enemies != []:	
			for i in range(len(enemies)):
				tank = enemies[i]
				shells = tank.shot("armour-piercing", shells)
				tank.move(dt)
				shells = tank.check_hits(shells)
				tank.draw()
			i = 0	
			while i < len(enemies) - 1:
				if enemies[i].destroy:
					enemies.pop(i)
				else:
					i += 1
		if shells != []:
			for i in range(len(shells)):
				shells[i].draw()
				shells[i].move(dt)
			i = 0
			while i < len(shells):
				if shells[i].destroy:
					shells.pop(i)
				else:
					i += 1
		#if random.randint(0, 100) > 95:
			#bonuses.append(Bonus(x, ""))
		
		if random.randint(0, 100) > 99:
			enemies.append(Tank(display_width, random.randint(0, display_height), 100, 50, "tank_rotate20.png", 
								2, 100, 1, 20, -1, gameDisplay)) 
		player.draw()
		player.charge()
		if shells != []:
			shells = player.check_hits(shells)
		pygame.display.update()
		clock.tick(50)
		
game_intro()
pygame.quit()
quit()
