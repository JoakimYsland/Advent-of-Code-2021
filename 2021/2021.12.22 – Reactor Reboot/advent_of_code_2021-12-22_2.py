
# https://adventofcode.com/2021/day/22

import time
import math
import re
from copy import deepcopy

def my_print(*args, **kwargs):
	print(' '.join(map(str,args)), **kwargs)
	return

def run(run_title, input_file):

	def get_cube_list(cuboid): 
		cube_list = []
		c_min, c_max = cuboid[1], cuboid[2]
		for x in range(c_min[0], c_max[0] + 1): 
			for y in range(c_min[1], c_max[1] + 1): 
				for z in range(c_min[2], c_max[2] + 1): 
					cube_list.append((x,y,z))
		return cube_list

	def get_cuboid_volume(cuboid): 
		c_min, c_max = cuboid[1], cuboid[2]
		for i in range(0, 3):
			if (c_min[i] == None) or \
			   (c_max[i] == None): 
				return 0
		volume = (c_max[0] - c_min[0] + 1) * \
				 (c_max[1] - c_min[1] + 1) * \
				 (c_max[2] - c_min[2] + 1)
		return volume if volume > 0 else 0

	def get_intersection(cuboid_a, cuboid_b): 
		a_min, a_max = cuboid_a[1], cuboid_a[2]
		b_min, b_max = cuboid_b[1], cuboid_b[2]
		i_min = [None, None, None]
		i_max = [None, None, None]

		for i in range(0, 3):
			if a_max[i] >= b_min[i] and a_min[i] <= b_min[i]: 
				# i_max[i] = a_max[i]
				# i_min[i] = b_min[i]
				i_max[i] = min(a_max[i], b_max[i])
				i_min[i] = max(a_min[i], b_min[i])
			elif a_max[i] >= b_max[i] and a_min[i] >= b_min[i]: 
				# i_max[i] = b_max[i]
				# i_min[i] = a_min[i]
				i_max[i] = min(a_max[i], b_max[i])
				i_min[i] = max(a_min[i], b_min[i])
			elif a_max[i] <= b_max[i] and a_min[i] >= b_min[i]: 
				# i_max[i] = a_max[i]
				# i_min[i] = a_min[i]
				i_max[i] = min(a_max[i], b_max[i])
				i_min[i] = max(a_min[i], b_min[i])
			elif a_max[i] >= b_max[i] and a_min[i] <= b_min[i]: 
				# i_max[i] = b_max[i]
				# i_min[i] = b_min[i]
				i_max[i] = min(a_max[i], b_max[i])
				i_min[i] = max(a_min[i], b_min[i])

		return i_min, i_max

	def add_intersection_cuboids(target_name, new_cuboid_name): 
		init_length = len(cuboids)
		for i in range(0, init_length): 
			if cuboids[i][0] != target_name: 
				continue
			for j in range(i, init_length): 
				if cuboids[j][0] != target_name: 
					continue
				if i == j: 
					continue
					
				i_min, i_max = get_intersection(cuboids[i], cuboids[j])
				new_cuboid = [new_cuboid_name, i_min, i_max]
				i_volume = get_cuboid_volume(new_cuboid)
				if i_volume > 0: 
					cuboids.append(new_cuboid)
					my_print(new_cuboid)

	# --------------------------------------------------------------------------------

	# Test / Real – 2758514936282235 / ???

	start_time_ms = round(time.time() * 1000)
	
	cuboids = []
	init_procedure_area = ['init_procedure_area', [-50, -50, -50], [50, 50, 50]]

	for line in input_file: 
		split = [x for x in line.strip().replace('x=', '').replace(',y=', ' ').replace(',z=', ' ').replace('..', ' ').split(' ')]
		for i in range(1, len(split)): 
			split[i] = int(split[i])
		c_min = [split[1], split[3], split[5]]
		c_max = [split[2], split[4], split[6]]
		new_cuboid = [split[0], c_min, c_max]
		cuboids.append(new_cuboid)

	for c in cuboids: my_print(c)
	my_print('-----')

	# Replace OFFs with intersection OFFs
	cuboids.reverse()
	init_length = len(cuboids)
	for i in range(0, init_length): 
		if cuboids[i][0] == 'off': 
			cuboids[i][0] = 'original_off'
			for j in range(i+1, init_length):
				if cuboids[j][0] == 'on': 
					i_min, i_max = get_intersection(cuboids[i], cuboids[j])
					new_cuboid = ['replaced_off', i_min, i_max]
					i_volume = get_cuboid_volume(new_cuboid)
					if i_volume > 0: 
						cuboids.append(new_cuboid)
						my_print(new_cuboid)
	cuboids.reverse()

	# Add intersection ONs between replaced OFFs
	add_intersection_cuboids('replaced_off', 'replaced_off_int')
	
	# Add intersection OFFs between ONs
	add_intersection_cuboids('on', 'on_intersection')

	# # Add intersection ONs between OFFs
	# add_intersection_cuboids('on_intersection', 'off_intersection')
	
	# for c in [c for c in cuboids if c[0] == 'replaced_off']: 
	for c in cuboids: 
		if 	 c[0] == 'replaced_off': 	 c[0] = 'off'
		elif c[0] == 'replaced_off_int': c[0] = 'on'
		elif c[0] == 'on_intersection':  c[0] = 'off'
		elif c[0] == 'off_intersection': c[0] = 'on'
	
	my_print('-----')
	# for c in cuboids: 
	# 	print(c)
	# print('-----')

	reactor = {}
	for cuboid in cuboids: 
		instruction, c_min, c_max = cuboid
		if instruction == 'on': 
			cube_list = get_cube_list(cuboid)
			for cube in cube_list: 
				reactor.setdefault(cube, 0)
				reactor[cube] += 1
		elif instruction == 'off': 
			cube_list = get_cube_list(cuboid)
			for cube in cube_list: 
				reactor.setdefault(cube, 0)
				reactor[cube] -= 1

	print(reactor)
	print(len(reactor))

	cubes_on = 0
	for cuboid in cuboids: 
		instruction, c_min, c_max = cuboid
		if instruction == 'on': 
			cubes_on += get_cuboid_volume(cuboid)
		elif instruction == 'off': 
			cubes_on -= get_cuboid_volume(cuboid)

	end_time_ms = round(time.time() * 1000)
	total_time = end_time_ms - start_time_ms

	print(run_title, "cubes_on:", cubes_on, ('(' + str(total_time) + "ms)"))

run("[Test]", open('input_test.txt', 'r').readlines())
# run("[Real]", open('input.txt', 'r').readlines())