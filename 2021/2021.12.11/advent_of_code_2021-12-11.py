
# https://adventofcode.com/2021/day/11

# import statistics
# from collections import deque
from collections import namedtuple

Vec2 = namedtuple("Vec2", ['x', 'y'])

def run(run_title, input_file):

	def get_adjacent(x, y):
		adjacent = []
		if x > 0: 					adjacent.append(Vec2(x - 1, y)) # W
		if x < grid_size.x - 1: 	adjacent.append(Vec2(x + 1, y)) # E
		if y > 0:
			adjacent.append(Vec2(x, y - 1)) # N
			if x > 0: 				adjacent.append(Vec2(x - 1, y - 1)) # NW
			if x < grid_size.x - 1: adjacent.append(Vec2(x + 1, y - 1)) # NE
		if y < grid_size.y - 1:
			adjacent.append(Vec2(x, y + 1)) # S
			if x > 0: 				adjacent.append(Vec2(x - 1, y + 1)) # SW
			if x < grid_size.x - 1: adjacent.append(Vec2(x + 1, y + 1)) # SE
		return adjacent

	def regen_energy(e):
		for x, _ in enumerate(octopi): 
			for y, _ in enumerate(octopi[x]): 
				octopi[x][y] += e

	# --------------------------------------------------------------------------------

	# Test / Real – 1656 / ???

	steps = 100
	flashes = 0
	octopi = []

	for line in input_file: 
		octopi.append([int(o) for o in line.strip()])

	octopi = [list(x) for x in zip(*octopi)] # Transpose <3
	grid_size = Vec2(len(octopi[0]), len(octopi))

	for step in range(0, steps):

		regen_energy(1)

		new_flash = True
		flashing_octopi = []
		while new_flash:
			new_flash = False
			for x, _ in enumerate(octopi): 
				for y, _ in enumerate(octopi[x]): 
					coords = Vec2(x,y)
					if octopi[x][y] > 9 and not coords in flashing_octopi:
						flashing_octopi.append(coords)
						adjacent = get_adjacent(x, y)
						for a in adjacent:
							octopi[a.x][a.y] += 1
						new_flash = True
		
		for c in flashing_octopi:
			octopi[c.x][c.y] = 0

		flashes += len(flashing_octopi)
	
	print(run_title, "flashes:", flashes)

run("[Test]", open('input_test.txt', 'r').readlines())
# run("[Real]", open('input.txt', 'r').readlines())