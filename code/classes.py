import pygame
class Tank:
	def __init__(self, x, y, width, height, image, recharge_time, max_health, velo, shell_velocity, side, gameDisplay):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.image = pygame.image.load(image).convert_alpha()
		self.image = pygame.transform.scale(self.image, (width, height))
		self.health = max_health
		self.max_health = max_health
		self.recharge_time = recharge_time * 60
		self.recharge = self.recharge_time
		self.velo = velo * side
		self.side = side
		self.shell_velocity = shell_velocity
		self.is_destroyed = False
		self.gameDisplay = gameDisplay
		self.APshells = 1000
		self.Gshells = 20
	
	def shot(self, shell_type):
		if self.recharge < 0:
			self.recharge = self.recharge_time
			if shell_type == "armour-piercing" and self.APshells != 0:
				self.APshells -= 1
			elif self.APshells == 0:
				return None
			if shell_type == "cumulative" and self.Gshells != 0:
				self.Gshells -= 1
			elif self.Gshells == 0:
				return None
			return Shell(self.x + self.width // 2 * self.side, self.y, self.shell_velocity * self.side, shell_type, self.gameDisplay)
		else:
			self.recharge -= 1
			
		
	def charge(self):
		self.recharge -= 1
			
	def move(self, dt):
		self.x += self.velo * dt
		if self.x + self.width < 0:
			self.is_destroyed = True
	
	def hit(self, shell):
		self.health -= shell.damage
		if self.health < 0:
			self.is_destroyed = True
			
	def draw(self):
		self.gameDisplay.blit(self.image, (int(self.x - self.width / 2), int(self.y - self.height / 2)))
		pygame.draw.rect(self.gameDisplay, (200,0,0), [int(self.x - self.width/2), int(self.y - self.height/2), int((self.health*0.1 * 10)/self.max_health * self.width), 10])

		
	def check_hits(self, shells):
		i = 0
		while i < len(shells):
			shell = shells[i]
			if shell.x < self.x + self.width / 2 and shell.x > self.x - self.width / 2 and shell.y > self.y - self.height / 2 and shell.y < self.y + self.height / 2:
				self.hit(shell)
				shells.pop(i)
				print("ypoH")
			else:
				i += 1
		return shells
		
	def catch(self, bonus, mouse_click):
		if mouse_click[0] < bonus.x + bonus.width / 2 and mouse_click[0] > bonus.x - bonus.width / 2 and mouse_click[1] > bonus.y - bonus.height / 2 and mouse_click[1] < bonus.y + bonus.height / 2:
			if bonus.type_c == 1:
				self.health += 50
				if self.health > self.max_health:
					self.health = self.max_health
			elif bonus.type_c == 2:
				self.APshells += 50
			elif bonus.type_c == 3:
				self.Gshells += 10
			bonus.is_lost = True

				
				
class Shell:
	def __init__(self, x, y, velo, kind, gameDisplay):
		self.x = x
		self.y = y
		self.gameDisplay = gameDisplay
		self.is_destroyed = False
		if kind == "armour-piercing":
			self.damage = 10
			self.velo = velo
			self.color = (0, 0, 0)
		elif kind == "cumulative":
			self.damage = 40
			self.velo = velo * 0.8
			self.color = (255,215,0)
			
	def move(self, dt):
		self.x += self.velo * dt
		if self.x < 0 and self.x > self.gameDisplay.get_width():
			self.is_destroyed = True
	
	def draw(self):
		pygame.draw.circle(self.gameDisplay, self.color, (int(self.x), int(self.y)), 3)
		
	
		
class Bonus:
	def __init__(self, x, y, width, height, velocity, type_c, image, gameDisplay):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.velocity = velocity
		self.type_c = type_c
		self.image = pygame.image.load(image)
		self.image = pygame.transform.scale(self.image, (width, height))
		self.gameDisplay = gameDisplay
		self.is_lost = False
		
	def move(self):
		self.y += self.velocity
		if self.y > self.gameDisplay.get_height() + self.height / 2:
			self.is_lost = True
	
	def draw(self):
		self.gameDisplay.blit(self.image, (int(self.x - self.width / 2), int(self.y - self.height / 2)))
		
		
		
		
		
