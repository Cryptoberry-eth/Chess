import pygame

#Class for Piece Positioning and Functionality
class Piece:
#Define Color, Position, and whether piece has moved
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.has_moved = False
    

#Functionality for Special Moves and Updating position after move
    def move(self, board, square, force=False):			
        for i in board.squares:
            i.highlight = False
        
        #Update piece position if selected move in valid moves
        if square in self.get_valid_moves(board) or force:
            if self.__class__.__name__ == 'Pawn' and board.last_move:
                start_pos, end_pos = board.last_move
                
                if abs(start_pos[1] - end_pos[1]) == 2 and board.get_square_from_pos(end_pos).occupying_piece.__class__.__name__ == 'Pawn':
                    if end_pos[1] == self.y and abs(end_pos[0] - self.x) == 1:
                        en_passant_capture_square = (end_pos[0], end_pos[1] + (1 if self.color == 'black' else -1))
                        if square == board.get_square_from_pos(en_passant_capture_square):
                            board.get_square_from_pos(end_pos).occupying_piece = None
            
            board.last_move = (self.pos, square.pos)
            prev_square = board.get_square_from_pos(self.pos)
            self.pos, self.x, self.y = square.pos, square.x, square.y

            prev_square.occupying_piece = None
            square.occupying_piece = self
            board.selected_piece = None
            self.has_moved = True

            # Pawn promotion
            if self.notation == ' ':
                #Check if pawn has reached final rank
                if self.y == 0 or self.y == 7:
                    choice = board.promotion_choice_ui(self.color)

                    if choice == "Queen":
                        from data.classes.pieces.Queen import Queen
                        square.occupying_piece = Queen(
                            (self.x, self.y),
                            self.color,
                            board
                        )
                    elif choice == "Knight":
                        from data.classes.pieces.Knight import Knight
                        square.occupying_piece = Knight(
                            (self.x, self.y),
                            self.color,
                            board
                        )
                    elif choice == "Bishop":
                        from data.classes.pieces.Bishop import Bishop
                        square.occupying_piece = Bishop(
                            (self.x, self.y),
                            self.color,
                            board
                        )
                    elif choice == "Rook":
                        from data.classes.pieces.Rook import Rook
                        square.occupying_piece = Rook(
                            (self.x, self.y),
                            self.color,
                            board
                        )

            # Move rook if king castles
            if self.notation == 'K':
                #Check to see whether castling long or short
                if prev_square.x - self.x == 2:
                    rook = board.get_piece_from_pos((0, self.y))
                    rook.move(board, board.get_square_from_pos((3, self.y)), force=True)
                elif prev_square.x - self.x == -2:
                    rook = board.get_piece_from_pos((7, self.y))
                    rook.move(board, board.get_square_from_pos((5, self.y)), force=True)

            return True
        else:
            board.selected_piece = None
            return False

#Function to check which squares a piece(Self) can move to out of possible moves
    def get_moves(self, board):
        output = []
        for direction in self.get_possible_moves(board):
            for square in direction:
                #Check to see whether destination square is empty, if not then what is the color of the piece in the square
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == self.color:
                        break
                    else:
                        output.append(square)
                        break
                else:
                    output.append(square)
        return output

#Function to see if board is in check to see valid moves for a Piece(Self)
    def get_valid_moves(self, board):
        output = []
        for square in self.get_moves(board):
            if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                output.append(square)

        return output


    # True for all pieces except pawn
    def attacking_squares(self, board):
        return self.get_moves(board)