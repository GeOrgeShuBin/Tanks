import pygame
from pygame import mixer
import random 
import time 
pygame.init()

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

class Tank():
	"""
	Create tanks
	
	Parametres:
	----------
	x : int
		X-coordinate of the tank
	y : int
		Y-coordinate of the tank
	health:int
		initial tank health
	speed : int
		tank speed
	image: picture
		tank image 
	"""
	def __init__(self , x , y ):
		self.x = x
		self.y = y
		self.distance = random.randint(display_width/3 , display_width - tank_width)
		self.health = 50
		self.max_health = 99
		self.speed = 1
		self.img_num = random.randint(0,0)
		self.image_filename = "tank_rotate2" + str(self.img_num) + ".png"
		self.image = pygame.image.load(self.image_filename).convert_alpha()
		self.image = pygame.transform.scale(self.image , (tank_width, tank_height))
		self.shell_x = x
		self.shell_y = y + tank_height/2
		self.shell_radius = 5
		self.shell_speed = 15
		
	def movement_tank(self):
		"""
		Defines the rule of the tank movement
		
		Parametres:
		----------
		"""
		self.x -= self.speed 
		if self.x < self.distance : 
			self.speed = 0
	def tank_shot(self):
		"""
		Draw a tank's shell 
		
		Parametres
		----------
		"""
		pygame.draw.circle(gameDisplay ,(0,0,0) , (self.shell_x , self.shell_y) , self.shell_radius )	
			
	def movement_shell(self):
		"""
		Defines the rule of the shell movement
		
		Parametres:
		----------
		
		"""
		self.shell_x -= self.shell_speed
		if self.shell_x < 0:
			self.shell_x = int(self.x)
	def draw_tank(self):
		"""
		Draws the tank 
		
		Parametres:
		
		----------
		image: picture
			preset image 
		x : int
			X-coordinate of the tank
		y : int
			Y-coordinate of the tank
		"""
		gameDisplay.blit(self.image , (self.x , self.y))		
	
	def draw_health(self):
		"""
		Draws a rectangle in proportion to our health
		"""
		pygame.draw.rect(gameDisplay , red , [self.x , self.y - 10, int(self.health) , 10])

	def hit(self, damage):
		"""
		Defines the rule of the tank health
		
		Parametres:
		
		----------
		
		damage: int
			number of health points occupied
		"""
		self.health -= damage
		print("HEALTH =" , self.health)
	def crashed_tank(self):
		"""
		Removes a tank with zero health
		
		Parametres:
		-----------
		"""
		self.speed = 0
		gameDisplay.blit(self.image , (self.x , self.y))	
		
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

def number_of_shell(norm_shell , gold_shell , health):
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
	gameDisplay.blit(norm_shells,(50 ,display_height - 50))
	gameDisplay.blit(gold_shells,(200 ,display_height - 50))
	gameDisplay.blit(health_point,(400 ,display_height - 50 ))

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

							image = pygame.image.load("Player_1.png")
							image = pygame.transform.scale(image , (player_width, player_height)) 
							angar = False
							game_loop(image)		

						if  coord_x[1] < click_mouse[0]  < coord_x[1] + size_x and starty < click_mouse[1]  < starty + size_y : 
							image = pygame.image.load("Player_2.png")
							image = pygame.transform.scale(image ,(player_width, player_height)) 
							angar = False
							game_loop(image)		

						if  coord_x[2] < click_mouse[0]  < coord_x[2] + size_x and starty < click_mouse[1]  < starty + size_y : 
							image = pygame.image.load("Player_3.png")
							image = pygame.transform.scale(image , (player_width, player_height)) 
							angar = False
							game_loop(image)		

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

def game_loop(image):
	
	global recharge
	
	x = tank_width * 0.01
	y = ((display_height) * 0.5)	

	x_change = 0 
	y_change = 0
		
	shell_startx = x + player_width
	shell_starty = (display_height * 0.5)
	shell_speed = 15
	radius = 3
	gold_radius = 10 
	shelly_change = 0
		
	bonus_startx = random.randrange(0, display_width)
	bonus_starty = -600
	bonus_speed = 1
	bonus_width = 75
	bonus_height = 150
	
	dodged = 0
	health = 100
	norm_shells = 1000
	gold_shells = 100
	
	tanks_list = []
	shells_list = []
	
	gold_catridge = 100
	
	
	
	norm_damage = 5
	gold_damage = 25
	
	gameExit = False

	global pause
	
	initilize_tank(max_tanks , tanks_list)
		
	while not gameExit:
		click_mouse = pygame.mouse.get_pos()
		gameDisplay.fill(white)

		def shot(radius , color):
			shells_list.append([int(shall_startx),int(shall_starty),radius,color])
			shoot_gun_sound.play()
			print(shells_list)
		if pygame.key.get_pressed()[pygame.K_g]:
			x += 3			
		if pygame.key.get_pressed()[pygame.K_a]:
			x += -3			
		if pygame.key.get_pressed()[pygame.K_s]:
			y += 3			
		if pygame.key.get_pressed()[pygame.K_w]:
			y -= 3			

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pause = True
					paused()			
				if event.key == pygame.K_SPACE and recharge < 0:							
					norm_shells -= 1
					shot(radius , black)
					recharge = 100
				if event.key == pygame.K_LSHIFT and gold_catridge != 0 and recharge < 0:		
					shot(gold_radius , gold)
					recharge = 100
					gold_catridge -= 1
					gold_shells -= 1	
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 :
					if  bonus_startx < click_mouse[0] < bonus_startx + bonus_width and bonus_starty < click_mouse[1] < bonus_starty + bonus_height : 
						health += 25
						bonus_starty = -display_height
						bonus_startx = random.randint(0 , display_width - bonus_width)
						
			


		for i in tanks_list:
			i.movement_tank()			
			if i.health < 0 :				
				i.crashed_tank()
			else:
				i.movement_shell()
				i.draw_tank()
				i.tank_shot()
				i.draw_health()

		i = -1
		k = -1
		for shell in shells_list:
			i += 1
			shells(shell[0], shell[1], shell[2], shell[3])
			shell[0] += shell_speed
			if shell[0] > display_width +radius:
				shells_list.pop(i)
				shells_list = shells_list	
			for tank in tanks_list:			
				if tank.x < shell[0] < tank.x + tank_width and tank.y < shell[1] < tank.y + tank_height :
					k = i
					tank.hit(gold_damage if shell[3] == gold else norm_damage)
					shells_list.pop(k)
					shells_list = shells_list
			
		if bonus_starty > display_height:
			bonus_starty =  - display_height
			bonus_startx = random.randrange(0,display_width)
								
		if x < 0 :
			x = 0	
		if y < 0:
			y = 0
		if y > display_height - tank_height:
			y = display_height - tank_height
		if x > display_width - player_width :
			x =  display_width - player_width 		

		player(image ,x,y)
		
		number_of_shell(norm_shells , gold_shells , health)
		
		gameDisplay.blit(aimImg,pygame.mouse.get_pos())


		shall_startx = x + player_width 
		shall_starty = y + player_height/2
		
		recharge -= 10
	
						
		bonus(bonus_startx , bonus_starty , bonus_width , bonus_height )
		bonus_starty += bonus_speed
		
		pygame.display.update()
		clock.tick(50)
game_intro()
game_loop() 	
pygame.quit()
quit()
