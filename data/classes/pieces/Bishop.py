import pygame

from data.classes.Piece import Piece

#Class for Bishop Functionality
class Bishop(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)
		#Source Image from relevant folder
		img_path = 'data/imgs/' + color[0] + '_bishop.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

		self.notation = 'B'

# Define Possible Moves for Bishop
	def get_possible_moves(self, board):
		output = []
		#Possible Moves Northeast
		moves_ne = []
		for i in range(1, 8):
			if self.x + i > 7 or self.y - i < 0:
				break
			moves_ne.append(board.get_square_from_pos(
				(self.x + i, self.y - i)
			))
		output.append(moves_ne)

		#Possible Moves Southeast
		moves_se = []
		for i in range(1, 8):
			if self.x + i > 7 or self.y + i > 7:
				break
			moves_se.append(board.get_square_from_pos(
				(self.x + i, self.y + i)
			))
		output.append(moves_se)

		#Possible Moves SouthWest
		moves_sw = []
		for i in range(1, 8):
			if self.x - i < 0 or self.y + i > 7:
				break
			moves_sw.append(board.get_square_from_pos(
				(self.x - i, self.y + i)
			))
		output.append(moves_sw)

		#Possible Moves Northwest
		moves_nw = []
		for i in range(1, 8):
			if self.x - i < 0 or self.y - i < 0:
				break
			moves_nw.append(board.get_square_from_pos(
				(self.x - i, self.y - i)
			))
		output.append(moves_nw)

		return output