
# https://adventofcode.com/2021/day/9

# import re # Split string with multiple delimiters
from collections import namedtuple

Vec2 = namedtuple("Vec2", ['x', 'y'])

def get_adjacent(height_map, x, y, map_size):
	adjacent = {'left':None, 'right':None, 'up':None, 'down':None}
	if (x > 0): 				adjacent['left'] 	= height_map[y][x-1]
	if (x < map_size.x - 1): 	adjacent['right'] 	= height_map[y][x+1]
	if (y > 0): 				adjacent['up'] 		= height_map[y-1][x]
	if (y < map_size.y - 1):  	adjacent['down'] 	= height_map[y+1][x]
	return adjacent

def is_low_point(cell, adjacent): 
	for a in adjacent.values():
		if a != None and a <= cell: 
			return False
	return True

# --------------------------------------------------------------------------------

# Test / Real – 15 / 522

def run(run_title, input_file):

	height_map = []
	for line in input_file: 
		height_map.append([int(c) for c in line.strip()])

	risk_level = 0
	map_size = Vec2(len(height_map[0]), len(height_map))

	for y, row in enumerate(height_map): 
		for x, cell in enumerate(row): 
			adjacent = get_adjacent(height_map, x, y, map_size)
			if is_low_point(cell, adjacent):
				risk_level += cell + 1

	print(run_title, "risk_level:", risk_level)

run("[Test]", open('input_test.txt', 'r').readlines())
run("[Real]", open('input.txt', 'r').readlines())