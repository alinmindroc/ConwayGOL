#!/usr/bin/python

class Cell:
	def __init__(self, x = 0, y = 0):
		self.alive = True
		self.x = x
		self.y = y

	def __hash__(self):
		return hash(self.x) ^ hash(self.y)

	def die(self):
		self.alive = False

	def revive(self):
		self.alive = True

	def isalive(self):
		return self.alive

	def __eq__(self, c2):
		return self.x == c2.x and self.y == c2.y

	def neighbours(self):
		s = []
		x = self.x
		y = self.y
		s.append(Cell(x-1, y+1))
		s.append(Cell(x, y+1))
		s.append(Cell(x+1, y+1))
		s.append(Cell(x+1, y))
		s.append(Cell(x+1, y-1))
		s.append(Cell(x, y-1))
		s.append(Cell(x-1, y-1))
		s.append(Cell(x-1, y))

		for i in s:
			i.die()

		return s

	def setx(self, x):
		self.x = x

	def sety(self, y):
		self.y = y

	def getx(self):
		return self.x

	def gety(self):
		return self.y

	def __str__(self):
		res = (str)(self.x) + ":" + (str)(self.y)
		return res


def alive_neighbours(cell, seed):
	s = 0
	for i in seed:
		if neighbours(i, cell) and i.isalive() == True:
			s += 1
	return s


def neighbours(c1, c2):
	if c2.x == c1.x - 1 and c2.y == c1.y + 1:
		return True
	elif c2.x == c1.x and c2.y == c1.y + 1:
		return True
	elif c2.x == c1.x + 1 and c2.y == c1.y + 1:
		return True
	elif c2.x == c1.x + 1 and c2.y == c1.y:
		return True
	elif c2.x == c1.x + 1 and c2.y == c1.y - 1:
		return True
	elif c2.x == c1.x and c2.y == c1.y - 1:
		return True
	elif c2.x == c1.x - 1 and c2.y == c1.y - 1:
		return True
	elif c2.x == c1.x - 1 and c2.y == c1.y:
		return True
	else:
		return False


def evolve_universe(seed):
	halo = set()

	if len(seed) == 1:
		return set()

	#creez haloul
	for cell in seed:
		cell.revive()
		halo = halo.union(cell.neighbours())

	for i in seed:
		if i in halo:
			halo.remove(i)

	#ma uit prin halou sa vad daca invie ceva
	for hcell in halo:
		nr = 0
		for scell in seed:
			if neighbours(hcell, scell):
				nr += 1
		if nr == 3:
			hcell.revive()

	#ma uit prin seed sa vad daca moare ceva
	for scell in seed:
		nr = 0
		for ncell in seed:
			if neighbours(ncell, scell):
				nr += 1
		if nr < 2 or nr > 3:
			scell.die()

	#construiesc rezultatul din celulele vii
	result = set()
	for i in halo:
		if i.isalive():
			result.add(i)

	for i in seed:
		if i.isalive():
			result.add(i)

	return result

if __name__ == '__main__':
	c1 = Cell(0, 0)
	c2 = Cell(0, 2)
	c3 = Cell(1, 0)
	c4 = Cell(1, 1)
	c5 = Cell(2, 1)

	seed = set([c1, c2, c3, c4, c5])

	for i in seed:
		i.x += 10
		i.y -= 10

	while len(seed) > 0:
		for i in seed:
			print i,

		print
		seed = evolve_universe(seed)