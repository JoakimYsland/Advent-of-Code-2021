
# https://adventofcode.com/2021/day/8

# --------------------------------------------------------------------------------

# Test / Real – 26 / 456

# 0: 123-456 = 6
# 1: --3--5- = 2 *
# 2: 1-345-7 = 5
# 3: 1-34-67 = 5
# 4: -234-6- = 4 *
# 5: 12-4-67 = 5
# 6: 12-4567 = 6
# 7: 1-3--6- = 3 *
# 8: 1234567 = 7 *
# 9: 1234-67 = 6

def run(run_title, input_file):

	unique_segment_digits = 0

	for line in input_file:
		mapping = ['abcdefg'] * 7
		entry = line.split(' | ')
		signal_patterns = entry[0].split(' ')
		output_value = entry[1].strip().split(' ')

		for pattern in output_value:
			if len(pattern) in [2,4,3,7]:
				unique_segment_digits += 1

	print(run_title, "unique_segment_digits:", unique_segment_digits)

run("[Test]", open('input_test.txt', 'r').readlines())
run("[Real]", open('input.txt', 'r').readlines())
