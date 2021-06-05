import pygame
import random
import sys

# General Setup:
pygame.mixer.pre_init(44100, -16, 2, 512)        # Game Sound Settings.
pygame.init()                                    # Initializing pygame.
Clock = pygame.time.Clock()                      # Intializing the FPS.

# Main Window (Size & Title):
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pong Game")

# Colors:
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
light_grey = (200,200,200)
grey = (31,31,31)

# Font:
game_Font = pygame.font.Font("freesansbold.ttf",25)

# Sound:
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

# Score Variables:
player_score = 0
opponent_score = 0

# Timer:
score_time = True

# Ball & Stick Movement/Animation Speeds (according to x and y axis):
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 10

# Game Rectangles:
# pygame.Rect(left, top, width, height)
ball = pygame.Rect(window_width/2 - 15, window_height/2 - 15, 30, 30)
player = pygame.Rect(window_width - 20, window_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, window_height/2 - 70, 10, 140)  

# Players stick boundary control function:
def player_movement():
    if player.top <= 0:
        player.top = 0
    if player.bottom >= window_height:
        player.bottom = window_height

# Opponent stick movement and boundary control function:
def opponent_AI():
    # Controls the movement:
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    # Controls the boundaries:
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= window_height:
        opponent.bottom = window_height

# Ball Movement/Animation Function:
def ball_movement():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    # Moving the ball by defined speed, at every frame:
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Controlling the bounce of the ball and Increment the score:
    if ball.top <= 0 or ball.bottom >= window_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1                        # Reverse the vertical crossover.

    # Player Score:
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1                         # Add the players score. 
        score_time = pygame.time.get_ticks()      # Tells how long the game was running since pygame was initiated.

    # Opponent Score:
    if ball.right >= window_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1                            
        score_time = pygame.time.get_ticks()      # Tells how long the game was running since pygame was initiated.

    # Ball collision with sticks:
    # If the ball collides with the player/opponent stick it reverses its direction.
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1
        
    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

# If the ball collides with the horizontal boundaries, the game restarts.
def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (window_width/2, window_height/2)

    if current_time - score_time < 700:
        number_three = game_Font.render("3",True,light_grey)
        screen.blit(number_three,(window_width/2 - 10, window_height/2 + 20))

    if 700 < current_time - score_time < 1400:
        number_two = game_Font.render("2",True,light_grey)
        screen.blit(number_two,(window_width/2 - 10, window_height/2 + 20))
    
    if 1400 < current_time - score_time < 2100:
        number_one = game_Font.render("1",True,light_grey)
        screen.blit(number_one,(window_width/2 - 10, window_height/2 + 20))
    
    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0,0
    else:
        ball_speed_y = 7 * random.choice((1,-1))
        ball_speed_x = 7 * random.choice((1,-1))
        score_time = None

# Main Game Loop:
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:         # Closes the window when user clicks the 'X' in the top right corner.
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:      # Key-presses defined.
            if event.key == pygame.K_DOWN:
                player_speed += 10
            elif event.key == pygame.K_UP:
                player_speed -= 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 10
            elif event.key == pygame.K_UP:
                player_speed += 10

    # Calling Functions/Game Logic:
    ball_movement() 
    player_movement()   
    opponent_AI()  

    player.y += player_speed                  # Increments the speed so the stick moves.
    
    # Drawings/Visuals:
    # The last line of code will be displayed on the top and vice versa. 
    screen.fill(grey)
    # pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(screen, light_grey, player) 
    pygame.draw.rect(screen, light_grey, opponent)    
    pygame.draw.ellipse(screen, light_grey, ball)     
    # Drawing the line on the middle of the screen:
    pygame.draw.aaline(screen, light_grey, (window_width/2, 0),(window_width/2, window_height))

    if score_time:
        ball_restart()

    # Displaying Players Score:
    player_text = game_Font.render(f"{player_score}", True, light_grey)
    screen.blit(player_text, (425,300))

    # Displaying Opponents Score:
    opponent_text = game_Font.render(f"{opponent_score}", True, light_grey)
    screen.blit(opponent_text, (360,300))

    pygame.display.flip()
    Clock.tick(60)            # FPS

