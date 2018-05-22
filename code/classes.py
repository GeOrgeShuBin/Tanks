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
		self.destroy = False
		self.gameDisplay = gameDisplay
	
	def shot(self, shell_type, shells):
		if self.recharge < 0:
			shells.append(Shell(self.x + self.width // 2 * self.side, self.y, self.shell_velocity * self.side, shell_type, self.gameDisplay))
			self.recharge = self.recharge_time
		else:
			self.recharge -= 1
		return shells
		
	def charge(self):
		self.recharge -= 1
			
	def move(self, dt):
		self.x += self.velo * dt
		if self.x + self.width < 0:
			self.destroy = True
	
	def hit(self, shell):
		self.health -= shell.damage
		if self.health < 0:
			self.destroy = True
			
	def draw(self):
		self.gameDisplay.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
		pygame.draw.rect(self.gameDisplay, (200,0,0), [self.x - self.width//2, self.y - self.height//2, int(self.health), 10])

		
	def check_hits(self, shells):
		i = 0
		while i < len(shells) - 1:
			shell = shells[i]
			if shell.x < self.x + self.width / 2 and shell.x > self.x - self.width / 2 and shell.y > self.y - self.height / 2 and shell.y < self.y + self.height / 2:
				self.hit(shell)
				shells.pop(i)
			else:
				i += 1
		return shells
				
				
class Shell:
	def __init__(self, x, y, velo, kind, gameDisplay):
		self.x = x
		self.y = y
		self.gameDisplay = gameDisplay
		self.destroy = False
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
			self.destroy = True
	
	def draw(self):
		pygame.draw.circle(self.gameDisplay, self.color, (self.x, self.y), 3)
		
		
		
		
			
	

			
		
