import pygame
import time
pygame.font.init()
from check_cell import *


class Grid:
	puzzle = [
				[3, 0, 6, 5, 0, 8, 4, 0, 0],
				[5, 2, 0, 0, 0, 0, 0, 0, 0],
				[0, 8, 7, 0, 0, 0, 0, 3, 1],
				[0, 0, 3, 0, 1, 0, 0, 8, 0],
				[9, 0, 0, 8, 6, 3, 0, 0, 5],
				[0, 5, 0, 0, 9, 0, 6, 0, 0],
				[1, 3, 0, 0, 0, 0, 2, 5, 0],
				[0, 0, 0, 0, 0, 0, 0, 7, 4],
				[0, 0, 5, 2, 0, 6, 3, 0, 0]
			]

	def __init__(self, rows, cols, width, height, win):
		self.rows = rows
		self.cols = cols
		self.cells = [[Cell(self.puzzle[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
		self.width = width
		self.height = height
		self.img = None
		self.update_img()
		self.selected = None
		self.win = win

	def update_img(self):
		self.img = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

	def position(self, val):
		row, col = self.selected
		if self.cells[row][col].value == 0:
			self.cells[row][col].set(val)
			self.update_img()

			if valid(self.img, val, (row, col)) and self.solve_sudoku():
				return True

			self.cells[row][col].set(0)
			self.cells[row][col].set_temp(0)
			self.update_img()
			return False

	def sketch(self, val):
		row, col = self.selected
		self.cells[row][col].set_temp(val)

	def draw(self):
		gap = self.width / 9  # distance b/w grid lines
		for x in range(self.rows + 1):
			if x % 3 == 0 and x != 0:  # for 3x3 cells
				thickness = 4
			else:  # for 1x1 cells
				thickness = 1
			pygame.draw.line(self.win, (0, 0, 0), (0, x * gap), (self.width, x * gap), thickness)
			pygame.draw.line(self.win, (0, 0, 0), (x * gap, 0), (x * gap, self.height), thickness)

		for i in range(self.rows):
			for j in range(self.cols):
				self.cells[i][j].draw(self.win)  # drawing cells

	def select_cell(self, row, col):
		for i in range(self.rows):
			for j in range(self.cols):
				self.cells[i][j].selected = False  # reset not selected cells

		self.cells[row][col].selected = True
		self.selected = (row, col)

	def clear_cell(self):
		row, col = self.selected
		if self.cells[row][col].value == 0:
			self.cells[row][col].set_temp(0)

	def click(self, pos):
		if pos[0] < self.width and pos[1] < self.height:
			gap = self.width / 9
			x = pos[0] // gap
			y = pos[1] // gap
			return (int(y), int(x))

		return None

	def complete(self):
		for i in range(self.rows):
			for j in range(self.cols):
				if self.cells[i][j].value == 0:
					return False
		return True  # GAME OVER

	def solve_sudoku(self):
		find = find_empty(self.img)
		if not find:
			return True

		row, col = find

		for i in range(1, 10):
			if valid(self.img, i, (row, col)):
				self.img[row][col] = i

				if self.solve_sudoku():
					return True

				self.img[row][col] = 0

		return False

	def solve_visual(self):
		find = find_empty(self.img)
		if not find:
			return True

		row, col = find

		for i in range(1, 10):
			if valid(self.img, i, (row, col)):
				self.img[row][col] = i
				self.cells[row][col].set(i)
				self.cells[row][col].draw_change(self.win, True)
				self.update_img()
				pygame.display.update()
				pygame.time.delay(10)

				if self.solve_visual():
					return True

				self.img[row][col] = 0
				self.cells[row][col].set(0)
				self.update_img()
				self.cells[row][col].draw_change(self.win, False)
				pygame.display.update()
				pygame.time.delay(10)

		return False


class Cell:
	rows = 9
	cols = 9

	def __init__(self, value, row, col, width, height):
		self.value = value
		self.temp = 0
		self.row = row
		self.col = col
		self.width = width
		self.height = height
		self.selected = False

	def draw(self, win):
		text_font = pygame.font.SysFont("poppins", 40)

		gap = self.width / 9
		x = self.col * gap
		y = self.row * gap

		if self.temp != 0 and self.value == 0:
			text = text_font.render(str(self.temp), 1, (128, 128, 128))
			win.blit(text, (x + 5, y + 5))
		elif not(self.value == 0):
			text = text_font.render(str(self.value), 1, (0, 0, 0))
			win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

		if self.selected:
			pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

	def draw_change(self, win, g=True):
		text_font = pygame.font.SysFont("poppins", 40)

		gap = self.width / 9
		x = self.col * gap
		y = self.row * gap

		pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

		text = text_font.render(str(self.value), 1, (0, 0, 0))
		win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
		if g:
			pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
		else:
			pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

	def set(self, val):
		self.value = val

	def set_temp(self, val):
		self.temp = val


def redraw_window(win, puzzle, time, strikes):
	win.fill((255,255,255))
	# win.blit(text, (540 - 160, 560))
	text_font = pygame.font.SysFont("poppins", 40)
	text = text_font.render("X " * strikes, 3, (255, 0, 0))
	win.blit(text, (20, 560))
	puzzle.draw()


def main():
	win = pygame.display.set_mode((540, 600))
	pygame.display.set_caption("Sudoku")
	puzzle = Grid(9, 9, 540, 540, win)
	key = None
	run = True
	start = time.time()
	strikes = 0
	while run:

		play_time = round(time.time() - start)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					key = 1
				if event.key == pygame.K_2:
					key = 2
				if event.key == pygame.K_3:
					key = 3
				if event.key == pygame.K_4:
					key = 4
				if event.key == pygame.K_5:
					key = 5
				if event.key == pygame.K_6:
					key = 6
				if event.key == pygame.K_7:
					key = 7
				if event.key == pygame.K_8:
					key = 8
				if event.key == pygame.K_9:
					key = 9
				if event.key == pygame.K_DELETE:
					puzzle.clear_cell()
					key = None
				if event.key == pygame.K_SPACE:
					puzzle.solve_visual()
				if event.key == pygame.K_RETURN:
					i, j = puzzle.selected
					if puzzle.cells[i][j].temp != 0:
						if puzzle.position(puzzle.cells[i][j].temp):
							print("Success")
						else:
							print("Wrong")
							strikes += 1
						key = None

						if puzzle.complete():
							print("Game over")
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				clicked = puzzle.click(pos)
				if clicked:
					puzzle.select_cell(clicked[0], clicked[1])
					key = None

		if puzzle.selected and key is not None:
			puzzle.sketch(key)

		redraw_window(win, puzzle, play_time, strikes)
		pygame.display.update()
