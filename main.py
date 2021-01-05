import pygame
import random
import math
from pygame import mixer

# Init the pygame
pygame.mixer.pre_init(frequency=22050, size=16, channels=2, buffer=4096)
pygame.init()

# Create screen (width * height)
screen = pygame.display.set_mode((800, 600))

# Add background music
# mixer.music.load("Bomb+1.wav")
# mixer.music.play(-1)

# Title and logo
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("space-invaders.png")
pygame.display.set_icon(icon)
# Set background image
background = pygame.image.load("background.jpeg")

# Space shooter settings
playerImage = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
player_x_change = 0
player_score = 0

# Display the player score
score_font = pygame.font.Font("freesansbold.ttf", 25)
fontX = 10
fontY = 10

# Game Over font
game_over = pygame.font.Font("freesansbold.ttf", 64)

# Alien settings
alienImage = pygame.image.load("ufo.png")
alienX = random.randint(0, 800)
alienY = random.randint(50, 250)
alien_x_change = 0.3
alien_y_change = 40

alien_images = []
alien_x_cords = []
alien_y_cords = []

# Create multiple enemies
for i in range(random.randint(1, 7)):
    # Set random image for the alien
    if i == 0:
        alien_images.append(pygame.image.load("alien.png"))
    elif i == 1:
        alien_images.append(pygame.image.load("alien_1.png"))
    else:
        alien_images.append(pygame.image.load("ufo.png"))
    # Set random cords
    alien_x_cords.append(random.randint(0, 790) + i)
    alien_y_cords.append(random.randint(50, 240) + i)

# Bullet settings
bulletImage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bullet_x_change = 0
bullet_y_change = 1
bullet_state = "READY"  # Can't see the bullet at ready state, SHOOT is when the bullet is in motion


# Function responsible for drawing the shooter
def player(x, y):
    # blit() is used for drawing things on the screen
    screen.blit(playerImage, (x, y))


# Function responsible for drawing the alien
def alien(image, x, y):
    screen.blit(image, (x, y))


# Function responsible for shooting the bullet
def fire(x, y):
    global bullet_state
    bullet_state = "SHOOT"
    screen.blit(bulletImage, (x + 5, y + 10))


# Function responsible for displaying the font
def show_score(x, y):
    score = score_font.render(f"Score {str(player_score)}", True, (255, 255, 255))
    screen.blit(score, (x, y))


# Function responsible for displaying game over
def show_game_over():
    game_over_text = game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


# Function responsible for detecting collusion
def is_there_collusion(alien_x, alien_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow((bullet_x - alien_x), 2) + math.pow((bullet_y - alien_y), 2))
    if distance < 27:
        return True
    else:
        return False


# Check for quite event (GAME LOOP)
running = True
while running:

    # Set screen color RGB format 0 - 255
    screen.fill((0, 0, 0))
    # background set image
    # screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.4  # subtract 0.1 from the current X position
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.4  # add 0.1 from the current X position
            if event.key == pygame.K_SPACE:
                # Check the state of the bullet and set to the playerX co-ordinate
                if bullet_state is "READY":
                    bulletX = playerX
                    fire(bulletX, bulletY)
                    # bullet sound
                    bullet_sound = mixer.Sound("RIKOSCHT.wav")
                    bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0  # stop moving when key is released
    # Call the player method for drawing
    playerX += player_x_change  # Update the current playerX position
    # alienX += alien_x_change  # Alien movement set

    # Set boundaries for the space ship
    if playerX < 0:
        playerX = 0
    elif playerX >= 770:
        playerX = 770

    # Loop through aliens
    for i in range(len(alien_images)):
        # Game over
        if alien_y_cords[i] > 440:
            for j in range(len(alien_x_cords)):
                alien_y_cords[i] = 2000
            show_game_over()
            break

        alien_x_cords[i] += alien_x_change
        if alien_x_cords[i] <= 0:
            alien_x_change = 0.3
            alien_y_cords[i] += alien_y_change
        elif alien_x_cords[i] >= 770:
            alien_x_change = -0.3
            alien_y_cords[i] += alien_y_change

        # Check for collusion
        if is_there_collusion(alien_x_cords[i], alien_y_cords[i], bulletX, bulletY):
            bulletY = 480
            bullet_state = "READY"
            player_score += 1
            alien_x_cords[i] = random.randint(0, 800)
            alien_y_cords[i] = random.randint(50, 250)
            # Collusion sound
            bomb_sound = mixer.Sound("Bomb+1.wav")
            bomb_sound.play()

    # Draw player on the window
    player(playerX, playerY)

    # Draw alien on the window
    # alien(alienX, alienY)
    for i in range(len(alien_images)):
        alien(alien_images[i], alien_x_cords[i], alien_y_cords[i])

    # Change bullet movement according to the state
    if bulletY <= 100:
        bulletY = 480
        bullet_state = "READY"
    if bullet_state is "SHOOT":
        fire(bulletX, bulletY)
        bulletY -= bullet_y_change

    # Display the score on the window
    show_score(fontX, fontY)

    pygame.display.update()  # Update the game screen after changes are made on the game window
