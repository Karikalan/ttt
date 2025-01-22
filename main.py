import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 600, 600  # Adjusted height to fit the screen better
line_width = 15
board_rows, board_cols = 3, 3
square_size = width // board_cols
circle_radius = square_size // 3
circle_width = 15
cross_width = 25
space = square_size // 4

# Colors
bg_color = (28, 170, 156)
line_color = (23, 145, 135)
circle_color = (239, 231, 200)
cross_color = (84, 84, 84)
winning_line_color = (255, 0, 0)
font_color = (255, 255, 255)
button_color = (70, 130, 180)
button_hover_color = (100, 160, 200)
shadow_color = (50, 50, 50)

# Initialize the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(bg_color)

# Fonts
font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 40)

# Initialize board
def initialize_board():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]

board = initialize_board()
current_player = "X"

# Function to display the board
def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, line_color, (0, square_size), (width, square_size), line_width)
    pygame.draw.line(screen, line_color, (0, 2 * square_size), (width, 2 * square_size), line_width)
    # Vertical lines
    pygame.draw.line(screen, line_color, (square_size, 0), (square_size, square_size * 3), line_width)
    pygame.draw.line(screen, line_color, (2 * square_size, 0), (2 * square_size, square_size * 3), line_width)

def draw_figures():
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row * board_cols + col] == 'X':
                pygame.draw.line(screen, cross_color, 
                                 (col * square_size + space, row * square_size + square_size - space),
                                 (col * square_size + square_size - space, row * square_size + space), cross_width)
                pygame.draw.line(screen, cross_color, 
                                 (col * square_size + space, row * square_size + space),
                                 (col * square_size + square_size - space, row * square_size + square_size - space), cross_width)
            elif board[row * board_cols + col] == 'O':
                pygame.draw.circle(screen, circle_color, 
                                   (col * square_size + square_size // 2, row * square_size + square_size // 2), 
                                   circle_radius, circle_width)

# Function to check for a winner
def check_winner():
    win_conditions = [
        [board[0], board[1], board[2]],
        [board[3], board[4], board[5]],
        [board[6], board[7], board[8]],
        [board[0], board[3], board[6]],
        [board[1], board[4], board[7]],
        [board[2], board[5], board[8]],
        [board[0], board[4], board[8]],
        [board[2], board[4], board[6]]
    ]
    for condition in win_conditions:
        if condition[0] == condition[1] == condition[2]:
            return condition[0], win_conditions.index(condition)
    return None, None

# Draw the winning line
def draw_winning_line(index):
    if index < 3:  # Horizontal lines
        pos_y = (index + 1) * square_size - square_size // 2
        pygame.draw.line(screen, winning_line_color, (0, pos_y), (width, pos_y), line_width)
    elif index < 6:  # Vertical lines
        pos_x = (index - 3 + 1) * square_size - square_size // 2
        pygame.draw.line(screen, winning_line_color, (pos_x, 0), (pos_x, square_size * 3), line_width)
    elif index == 6:  # Top-left to bottom-right diagonal
        pygame.draw.line(screen, winning_line_color, (15, 15), (width - 15, square_size * 3 - 15), line_width)
    elif index == 7:  # Top-right to bottom-left diagonal
        pygame.draw.line(screen, winning_line_color, (width - 15, 15), (15, square_size * 3 - 15), line_width)

# Function to display the winning message
def display_winner(winner):
    # Blur effect (fill screen with semi-transparent layer)
    blur_surface = pygame.Surface((width, square_size * 3))
    blur_surface.set_alpha(128)  # Transparency
    blur_surface.fill((0, 0, 0))  # Black color
    screen.blit(blur_surface, (0, 0))

    # Draw winning message without background
    message = f"Player {winner} wins!"
    text = font.render(message, True, font_color)
    text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
    screen.blit(text, text_rect)

    # Draw Play Again button
    play_again_button = pygame.Rect(width // 3 - 60, height - 80, 120, 40)
    pygame.draw.rect(screen, shadow_color, play_again_button.move(2, 2))  # Draw shadow
    pygame.draw.rect(screen, button_color, play_again_button, border_radius=10)  # Draw button with rounded corners
    play_again_text = button_font.render("Play Again", True, font_color)
    screen.blit(play_again_text, play_again_text.get_rect(center=play_again_button.center))

    # Draw Quit button
    quit_button = pygame.Rect(2 * width // 3 - 60, height - 80, 120, 40)
    pygame.draw.rect(screen, shadow_color, quit_button.move(2, 2))  # Draw shadow
    pygame.draw.rect(screen, button_color, quit_button, border_radius=10)  # Draw button with rounded corners
    quit_text = button_font.render("Quit", True, font_color)
    screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

    return play_again_button, quit_button

# Reset the game
def reset_game():
    global board, current_player, game_over
    board = initialize_board()
    current_player = "X"
    game_over = False
    screen.fill(bg_color)
    draw_lines()
    draw_figures()

# Display the initial board
draw_lines()

# Main game loop
running = True
game_over = False
play_again_button = pygame.Rect(width // 3 - 60, height - 80, 120, 40)
quit_button = pygame.Rect(2 * width // 3 - 60, height - 80, 120, 40)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if game_over:
                if play_again_button.collidepoint(mouse_pos):
                    reset_game()
                elif quit_button.collidepoint(mouse_pos):
                    running = False
                    pygame.quit()
                    exit()  # Use exit() instead of sys.exit()
            else:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = mouseY // square_size
                clicked_col = mouseX // square_size
                clicked_cell = clicked_row * board_cols + clicked_col

                if clicked_cell < len(board) and isinstance(board[clicked_cell], int):
                    board[clicked_cell] = current_player

                    draw_figures()
                    winner, win_index = check_winner()
                    if winner:
                        print(f"Player {winner} wins!")
                        draw_winning_line(win_index)
                        play_again_button, quit_button = display_winner(winner)
                        game_over = True
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'

    pygame.display.update()

print("Thanks for playing! Goodbye!")