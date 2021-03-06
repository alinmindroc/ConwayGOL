#!/usr/bin/python

#generates the coordinates for a CGOL instance. There are two default structures: fighter and explosion
#These are infinite figures, at no point in the simulation all their cells are dead

import sys

#the smallest component in the structure of a CGOL figure
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

#check if c1 and c2 are neighbours
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

#the method which generates the next state of the universe based on the current state and the survival/death rules
#seed = set of alive cells at current time
#halo = set of cells around the seed which may be revived in the next step 
def evolve_universe(seed):
	halo = set()

	if len(seed) == 1:
		return set()

	#create a halo consisting of alive neighbours for each cell
	for cell in seed:
		cell.revive()
		halo = halo.union(cell.neighbours())

	for i in seed:
		if i in halo:
			halo.remove(i)

	#check if any cell in the halo revives at the next step
	for hcell in halo:
		nr = 0
		for scell in seed:
			if neighbours(hcell, scell):
				nr += 1
		if nr == 3:
			hcell.revive()

	#check the seed to see if a cell dies at the next step
	for scell in seed:
		nr = 0
		for ncell in seed:
			if neighbours(ncell, scell):
				nr += 1
		if nr < 2 or nr > 3:
			scell.die()

	#generate a result based only on the alive cells
	result = set()
	for i in halo:
		if i.isalive():
			result.add(i)

	for i in seed:
		if i.isalive():
			result.add(i)

	return result

if __name__ == '__main__':
	#two infinite structures
	#fighter
	c1 = Cell(0, 0)
	c2 = Cell(0, 2)
	c3 = Cell(1, 0)
	c4 = Cell(1, 1)
	c5 = Cell(2, 1)

	fighter = set([c1, c2, c3, c4, c5])

	#explosion
	c1 = Cell(0, 0)
	c2 = Cell(0, 1)
	c3 = Cell(0, 5)
	c4 = Cell(0, 6)
	c5 = Cell(1, 2)
	c6 = Cell(1, 3)
	c7 = Cell(1, 4)
	c8 = Cell(2, 1)
	c9 = Cell(2, 5)
	c10 = Cell(3, 2)
	c11 = Cell(3, 4)
	c12 = Cell(4, 3)

	explosion = set([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12])

	seed = explosion

	if len(sys.argv) > 1:
		if sys.argv[1] == 'fighter':
			seed = fighter

	for i in seed:
		i.x += 30
		i.y -= 30

	while len(seed) > 0:
		for i in seed:
			print i,

		print
		seed = evolve_universe(seed)
