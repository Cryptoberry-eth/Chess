import pygame

from data.classes.Piece import Piece

# Class for Pawn Functionality
class Pawn(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		img_path = 'data/imgs/' + color[0] + '_pawn.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width - 35, board.tile_height - 35))

		self.notation = ' '


	def get_possible_moves(self, board):
		output = []
		moves = []

		# move forward
		if self.color == 'white':
			moves.append((0, -1))
			if not self.has_moved:
				moves.append((0, -2))

		elif self.color == 'black':
			moves.append((0, 1))
			if not self.has_moved:
				moves.append((0, 2))

		for move in moves:
			new_pos = (self.x, self.y + move[1])
			if new_pos[1] < 8 and new_pos[1] >= 0:
				output.append(
					board.get_square_from_pos(new_pos)
				)

		return output

# Function to check which squares a piece(Self) can move to out of possible moves
	def get_moves(self, board):
		output = []
		for square in self.get_possible_moves(board):
			# Check if move square is occupied
			if square.occupying_piece != None:
				break
			else:
				output.append(square)

		# ... (existing code)

# Check for en passant
		if board.last_move:
			start_pos, end_pos = board.last_move
			# Check if the last move was a two-square pawn move
			if abs(start_pos[1] - end_pos[1]) == 2 and isinstance(board.get_square_from_pos(end_pos).occupying_piece, Pawn):
				# Check if the pawn that made the move is adjacent to the current pawn
				if end_pos[1] == self.y and abs(end_pos[0] - self.x) == 1:
					capture_square = (end_pos[0], end_pos[1] + (1 if self.color == 'black' else -1))
					output.append(board.get_square_from_pos(capture_square))

# ... (existing code)

		# Check if Pawn can take a piece
		if self.color == 'white':
			if self.x + 1 < 8 and self.y - 1 >= 0:
				square = board.get_square_from_pos(
					(self.x + 1, self.y - 1)
				)
				if square.occupying_piece != None:
					if square.occupying_piece.color != self.color:
						output.append(square)
			if self.x - 1 >= 0 and self.y - 1 >= 0:
				square = board.get_square_from_pos(
					(self.x - 1, self.y - 1)
				)
				if square.occupying_piece != None:
					if square.occupying_piece.color != self.color:
						output.append(square)

		elif self.color == 'black':
			if self.x + 1 < 8 and self.y + 1 < 8:
				square = board.get_square_from_pos(
					(self.x + 1, self.y + 1)
				)
				if square.occupying_piece != None:
					if square.occupying_piece.color != self.color:
						output.append(square)
			if self.x - 1 >= 0 and self.y + 1 < 8:
				square = board.get_square_from_pos(
					(self.x - 1, self.y + 1)
				)
				if square.occupying_piece != None:
					if square.occupying_piece.color != self.color:
						output.append(square)

		return output
# Define Attacking Squares
	def attacking_squares(self, board):
		moves = self.get_moves(board)
		# return the diagonal moves 
		return [i for i in moves if i.x != self.x]