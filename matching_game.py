import pygame
import random
import sys

# Initialize ui
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Card Matching Game")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GREEN = (144, 238, 144)
CARD_SIZE = 150  # card
PADDING = 20  # Space
ROWS, COLS = 4, 4  # card number

#image
food_images = [
    pygame.image.load("sib.jpg"),
    pygame.image.load("shir.jpg"),
    pygame.image.load("asal.jpg"),
    pygame.image.load("khorma.jpg"),
    pygame.image.load("gerdo.jpg"),
    pygame.image.load("badam.jpg"),
    pygame.image.load("esfenaj.jpg"),
    pygame.image.load("keshmesh.jpg"),
    pygame.image.load("pesteh.jpg"),
]

if len(food_images) * 2 > ROWS * COLS:
    food_images = food_images[:ROWS * COLS // 2]  #fit grid
    
food_images = [pygame.transform.scale(img, (CARD_SIZE, CARD_SIZE)) for img in food_images]

all_images = food_images * 2
random.shuffle(all_images)

cards = []
for i in range(ROWS):
    row = []
    for j in range(COLS):
        idx = i * COLS + j
        row.append(all_images[idx])
    cards.append(row)

# Card state: hidden (0), revealed (1), or matched (2)
card_states = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Game variables
revealed_cards = []  
clock = pygame.time.Clock()
FPS = 30

# Font
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 80)
def draw_board():
    """Draw the game board with cards."""
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            x = col * (CARD_SIZE + PADDING) + PADDING
            y = row * (CARD_SIZE + PADDING) + PADDING

            # Draw card background
            if card_states[row][col] == 0:  # Hidden
                pygame.draw.rect(screen, GRAY, (x, y, CARD_SIZE, CARD_SIZE))
            elif card_states[row][col] == 1:  # Revealed
                screen.blit(cards[row][col], (x, y))
            elif card_states[row][col] == 2:  # Matched
                pygame.draw.rect(screen, WHITE, (x, y, CARD_SIZE, CARD_SIZE))
    pygame.display.flip()

def check_match():
    """Check if the two revealed cards match."""
    global revealed_cards
    if len(revealed_cards) == 2:
        (row1, col1), (row2, col2) = revealed_cards
        if cards[row1][col1] == cards[row2][col2]:
            card_states[row1][col1] = card_states[row2][col2] = 2  # Mark as matched
        else:
            pygame.time.wait(1000)  # Pause for a moment
            card_states[row1][col1] = card_states[row2][col2] = 0  # Hide again
        revealed_cards = []

def is_game_over():
    """Check if all cards are matched."""
    for row in card_states:
        if 0 in row:
            return False
    return True

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position
            x, y = pygame.mouse.get_pos()
            col = x // (CARD_SIZE + PADDING)
            row = y // (CARD_SIZE + PADDING)

            # Check bounds
            if row < ROWS and col < COLS and card_states[row][col] == 0:
                card_states[row][col] = 1  # Reveal the card
                revealed_cards.append((row, col))

    # Check for matches
    if len(revealed_cards) == 2:
        draw_board()  # Update the board to show the second revealed card
        pygame.time.wait(500)  # Wait 500ms so the player can see both cards
        check_match()
      # Check for game over
    if is_game_over():
        screen.fill(LIGHT_GREEN)
        text=big_font.render("YOU WIN!", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        # Restart the game
        
        card_states = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        random.shuffle(all_images)
        revealed_cards = []


    # Draw the board
    draw_board()
    clock.tick(FPS)  
   
