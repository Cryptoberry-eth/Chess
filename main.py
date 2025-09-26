import pygame

from data.classes.Board import Board



def promotion_choice_ui(screen, color):
    # Define colors
    WHITE = (255, 255, 255)
    
    # Load images
    piece_color = 'w' if color == 'white' else 'b'
    queen_img = pygame.image.load(f'data/imgs/{piece_color}_queen.png')
    knight_img = pygame.image.load(f'data/imgs/{piece_color}_knight.png')
    bishop_img = pygame.image.load(f'data/imgs/{piece_color}_bishop.png')
    rook_img = pygame.image.load(f'data/imgs/{piece_color}_rook.png')

    # Scale images to fit buttons if necessary
    button_size = (100, 100)  # Example button size
    queen_img = pygame.transform.scale(queen_img, button_size)
    knight_img = pygame.transform.scale(knight_img, button_size)
    bishop_img = pygame.transform.scale(bishop_img, button_size)
    rook_img = pygame.transform.scale(rook_img, button_size)
    
    buttons = {
        'Queen': (pygame.Rect(150, 150, *button_size), queen_img),
        'Knight': (pygame.Rect(350, 150, *button_size), knight_img),
        'Bishop': (pygame.Rect(150, 350, *button_size), bishop_img),
        'Rook': (pygame.Rect(350, 350, *button_size), rook_img)
    }
    
    chosen_piece = None
    while chosen_piece is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # Handle quit gracefully
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for piece, (button, img) in buttons.items():
                    if button.collidepoint(pos):
                        chosen_piece = piece
                        break  # Exit the loop since we've made a selection
        
        # Clear the screen and draw the background
        screen.fill(WHITE)
        
        # Draw buttons and images
        for piece, (button, img) in buttons.items():
            screen.blit(img, button)  # Blit the image
        
        pygame.display.flip()  # Update the full display
    
    return chosen_piece


pygame.init()

# Set pygame Window Size and initiate process
WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1], screen, promotion_choice_ui)
board.promotion_choice_ui = lambda color: promotion_choice_ui(screen, color)

def draw(display):
    display.fill('white')
    board.draw(display)
    pygame.display.update()




if __name__ == '__main__':
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Quit the game if the user presses the close button
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                   # If the mouse is clicked
                if event.button == 1:
                    board.handle_click(mx, my)
        if board.is_in_checkmate('black'): # If black is in checkmate
            print('White wins!')
            running = False
        elif board.is_in_checkmate('white'): # If white is in checkmate
            print('Black wins!')
            running = False
        # Draw the board
        draw(screen)