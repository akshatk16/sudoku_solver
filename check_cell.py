def find_empty(cell):
	for i in range(len(cell)):
		for j in range(len(cell[0])):
			if cell[i][j] == 0:
				return (i, j)

	return None


def possible(cell, num, pos):
	for i in range(len(cell[0])):
		if cell[pos[0]][i] == num and pos[1] != i:
			return False

	for i in range(len(cell)):
		if cell[i][pos[1]] == num and pos[0] != i:
			return False

	box_x = pos[1] // 3
	box_y = pos[0] // 3

	for i in range(box_y*3, box_y*3 + 3):
		for j in range(box_x * 3, box_x*3 + 3):
			if cell[i][j] == num and (i,j) != pos:
				return False

	return True
