import pygame
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
bright_red = (255,0,0)
bright_green = (0,255,0)

lifeline = "Health_Point"
car_width = 34



gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("MY GAME")
clock = pygame.time.Clock()
  
aimImg = pygame.image.load('aim1.png').convert()
aimImg.set_colorkey(white)

backgroundImg = pygame.image.load('fon.jpg').convert()
backgroundImg = pygame.transform.scale(backgroundImg , (display_width,display_height))

angarImg = pygame.image.load('angar.jpg').convert()
angarImg = pygame.transform.scale(angarImg , (display_width,display_height))


#tank_explosition = pygame.mixer.Sound('tank_explosition.mp3')
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=2048)
shoot_gun_sound = pygame.mixer.Sound('Shot.wav')

tank_height = 50
tank_weidth = 100

player_height = 50
player_weidth = 100

max_tanks = 10


class Tanks():
	def __init__(self , x , y ):
		self.x = x
		self.y = y
		self.health = 50
		self.max_health = 99
		self.speed = 0.3
		self.img_num = random.randint(0,0)
		self.image_filename = "tank_rotate2" + str(self.img_num) + ".png"
		self.image = pygame.image.load(self.image_filename).convert_alpha()
		self.image = pygame.transform.scale(self.image , (tank_weidth, tank_height))

		
	def move_tanks(self):
		self.x -= self.speed 
		if self.x < 0 : 
			self.x = display_width + tank_weidth
	def draw_tanks(self):
		gameDisplay.blit(self.image , (self.x , self.y))		
	
	def draw_health(self):
		pygame.draw.rect(gameDisplay , red , [self.x , self.y - 10, int(self.health) , 10])

	def hit(self, damage):
		self.health -= damage
		print("HEALTH =" , self.health)
	
	def crashed_tank(self):
		self.speed = 0
		gameDisplay.blit(self.image , (self.x , self.y))	
		

def initilize_tanks(max_tanks , tanks_list):
	for i in range(max_tanks):
		tank_x = random.randrange(  1024 , 2 *display_width)
		tank_y = random.randrange(0 , display_height - tank_height)
		tanks_list.append(Tanks(tank_x , tank_y))




def health_dodged(count):
	font = pygame.font.SysFont(None,25)
	text = font.render("Health_Point:" + str(count) , True , black )
	gameDisplay.blit(text,(display_width - 550,0))

def things_dodged(count):
	size = 25
	font = pygame.font.SysFont(None,size)
	text = font.render("Your assessment for exam:" + str(count) , True , red )
	gameDisplay.blit(text,(0,display_height - size ))
    
def things(thingx ,thingy , thingw , thingh , color) :
	pygame.draw.rect(gameDisplay, color , [thingx ,thingy , thingw , thingh]) 

def shalls(shallx , shally , radius , color): 
	pygame.draw.circle(gameDisplay,color , (shallx,shally) , radius)

	
def car(image ,x,y):
	gameDisplay.blit(image,(x,y))

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
	message_display("You lose")


def draw_angar():	
	
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
							image = pygame.transform.scale(image , (player_weidth, player_height)) 
							angar = False
							game_loop(image)		

						if  coord_x[1] < click_mouse[0] and click_mouse[0] < coord_x[1] + size_x and starty < click_mouse[1] and click_mouse[1] < starty + size_y : 
							image = pygame.image.load("Player_2.png")
							image = pygame.transform.scale(image ,(player_weidth, player_height)) 
							angar = False
							game_loop(image)		
						if  coord_x[2] < click_mouse[0] and click_mouse[0] < coord_x[2] + size_x and starty < click_mouse[1] and click_mouse[1] < starty + size_y : 
							image = pygame.image.load("Player_3.png")
							image = pygame.transform.scale(image , (player_weidth, player_height)) 
							angar = False
							game_loop(image)		

def button(msg,x,y,w,h,ic,ac,action = None):
	
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if (x + w > mouse[0] > x) and y + h > mouse[1] > y:
		pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
		if click[0] == 1 and  action != None:
			if action == "play":
				draw_angar()
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
					

def game_loop(image):




	
	x = tank_weidth * 0.01
	y = ((display_height) * 0.5)	

	x_change = 0 
	y_change = 0
	
	
	shall_startx = x + player_weidth
	shall_starty = (display_height * 0.5)
	shall_speed = 15
	radius = 3
	gold_radius = 10 
	shally_change = 0

	

	
	thing_startx = random.randrange(0, display_width)
	thing_starty = -600
	thing_speed = 5
	thing_width = 20
	thing_height = 30
	
	dodged = 0
	health = 100
	
	#shalls_list = []
	tanks_list = []
	shalls_list = []
	
	gold_catridge = 10
	
	norm_damage = 5
	gold_damage = 25
	
	gameExit = False
	
	initilize_tanks(max_tanks , tanks_list)
	

	
	while not gameExit:
		gameDisplay.fill(white)
		button("Norm",25,400,100,40,green,bright_green, "norm")
		button("Gold",25,500,100,40,gold,gold,"gold")

		def shot(radius , color):
			shalls_list.append([int(shall_startx),int(shall_starty),radius,color])
			shoot_gun_sound.play()
			print(shalls_list)
				
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()		
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					x_change -= 3
				elif event.key == pygame.K_d:
					x_change +=3
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:
					y_change += 3		 
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					y_change -= 3
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w or  event.key == pygame.K_s or event.key == pygame.K_a or  event.key == pygame.K_d:
					y_change = 0		
					x_change = 0 			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:		
					shot(radius , black)
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 and gold_catridge != 0:			
					shot(gold_radius , gold)
					gold_catridge -= 1

		x += x_change		
		y -= y_change
		#print("Y" , y)
		shall_startx = x + player_weidth 
		shall_starty = y + player_height/2
		
		
		
		things(thing_startx , thing_starty , thing_width , thing_height , red )
		thing_starty += thing_speed

		for i in tanks_list:
			i.move_tanks()			
			if i.health < 0 :
				i.crashed_tank()
			else:
				i.draw_tanks()
				i.draw_health()
		
		for shall in shalls_list:
			shalls(shall[0], shall[1], shall[2], shall[3])
			shall[0] += shall_speed
			#print(shall)
			if shall[0] > display_width +radius:
				shalls_list.pop(0)
				shalls_list = shalls_list	
			for tank in tanks_list:			
				if shall[0] > tank.x and shall[0] < tank.x + tank_weidth and shall[1] < tank.y + tank_height and shall[1] > tank.y:
					tank.hit(gold_damage if shall[3] == gold else norm_damage)
					shalls_list.pop(0)
					shalls_list = shalls_list
			print()
		
		
		car(image ,x,y)
		
		things_dodged(dodged)
		
		health_dodged(health)
		
		gameDisplay.blit(aimImg,pygame.mouse.get_pos())

		
		
		
		if thing_starty > display_height:
			thing_starty = 0 - display_height
			thing_startx = random.randrange(0,display_width)
			dodged += 1
			#thing_speed += 1
			#thing_width += 1
			health -= 1 
		
		if x < 0 :
			x = 0	
		if y < 0:
			y = 0
		if y > display_height - tank_height:
			y = display_height - tank_height
		if x > display_width - car_width or  x < 0:  
			if health >= 1 :
				health -= 1
			else:
				crash()	 
		
		
		#if x > thing_startx and x < thing_startx + thing_width or x + car_width >thing_startx and x + car_width < thing_startx + thing_width:
			#crash()
		#	dodged -= 20 
		
			
		pygame.display.update()
		clock.tick(50)
game_intro()
game_loop() 	
pygame.quit()
quit()
