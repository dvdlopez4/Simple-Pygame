from Entity.entity import *

class Particle(Entity):
	def __init__(self, _input, _physics, _graphics):
		super(Particle, self).__init__(_input, _physics, _graphics)
		self.isDone = False
