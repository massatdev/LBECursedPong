import pygame
import ai
import player
import eldritch
import random

pygame.init()
pygame.mixer.init()

# DELTA_MULTIPLIER = 0.25   (to be implemented)

WIDTH = 1600
HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

LEVEL = 1

curse_mngr = eldritch.CurseManager()

# ambient audio
pygame.mixer.music.load("CursedPong\\assets\\dk-fear.aif")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# curse trigger audio
curse_trigger_sound = pygame.mixer.Sound("CursedPong\\assets\\curse_trigger.wav")
curse_trigger_sound.set_volume(1)

# player variables
player_width = 20
player_height = 100

player_x = 100
player_y = HEIGHT // 2 - player_height // 2

player_speed = 10

player1 = player.Paddle(player_x, player_y, player_width, player_height, player_speed, CYAN, HEIGHT)

# ai variables

ai_width = 20
ai_height = 100

ai_x = WIDTH - 100
ai_y = HEIGHT // 2 - ai_height // 2

ai_speed = 5

aiplayer = ai.Paddle(ai_x, ai_y, ai_width, ai_height, ai_speed, ORANGE, HEIGHT, WIDTH, LEVEL)

# ball variables
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2

ball_true_speed_x = 5
ball_true_speed_y = 5
ball_speed_x = ball_true_speed_x
ball_speed_y = ball_true_speed_y

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cursed Pong")
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # curses
    player1.update_curses(curse_mngr)
    curse_mngr.update()

    # Input Handling
    keys = pygame.key.get_pressed()
    player1.handle_input(keys, curse_mngr)

    #ai update
    aiplayer.update(ball_y, ball_x)

    # Game Logic
    if curse_mngr.notice_timer == 0:
        ball_x -= ball_speed_x
        ball_y -= ball_speed_y
    
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
        ball_speed_y *= -1

    player_rect = player1.get_rect()
    ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)

    if player_rect.colliderect(ball_rect):
        ball_speed_x *= -1.2
        paddle_center_y = player1.y + (player1.height / 2)
        offset = (ball_y - paddle_center_y) / (player1.height / 2)
        random_noise = random.uniform(-2, 2)
        ball_speed_y = (offset * random_noise) + ball_speed_y
        ball_x = player1.x + player1.width + ball_radius

    if aiplayer.get_rect().colliderect(ball_rect):
        ball_speed_x *= -1.2
        paddle_center_y = aiplayer.y + (aiplayer.height / 2)
        offset = (ball_y - paddle_center_y) / (aiplayer.height / 2)
        random_noise = random.uniform(-2, 2)
        ball_speed_y = (offset * random_noise) + ball_speed_y

        ball_speed_y = ball_speed_y * random.uniform(0.8, 1.2)
        ball_x = aiplayer.x - ball_radius

    # Next Level Logic
    if ball_x - ball_radius >= WIDTH:
        LEVEL += 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_speed_x = ball_true_speed_x + (LEVEL * 0.5)
        ball_speed_y = ball_true_speed_y + (LEVEL * 0.5)

        # Trigger a new curse for the next level
        curse_mngr.trigger_random_curse(LEVEL)
        curse_trigger_sound.play()

    # Game Over Logic
    if ball_x + ball_radius <= 0:
        pygame.mixer.music.stop()
        curse_mngr.reset()    
        running = False

    # Victory logic
    if LEVEL > 6:
        curse_mngr.draw_menacing_text(screen, pygame.font.SysFont("impact", 32, bold=True), WIDTH, HEIGHT)
        pygame.mixer.music.stop()
        curse_mngr.reset()
        player1.draw(screen)
        aiplayer.draw(screen)
        pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)
        curse_mngr.draw_menacing_text(screen, pygame.font.SysFont("impact", 32), WIDTH, HEIGHT)    
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    # Draw Phase
    screen.fill(BLACK)
    if not curse_mngr.is_blackout():
        player1.draw(screen)
        aiplayer.draw(screen)
        pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)
        curse_mngr.draw_menacing_text(screen, pygame.font.SysFont("impact", 32, bold=True), WIDTH, HEIGHT)

    pygame.display.update()
    
    clock.tick(60)

pygame.quit()