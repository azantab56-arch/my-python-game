import pygame
import sys
import random

# Pygame init
pygame.init()

# Screen size (based on bg.png)
SCREEN_WIDTH = 401
SCREEN_HEIGHT = 601
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("Arial", 32)

# Load images
bg = pygame.image.load("assets/bg.png").convert()

bird_img = pygame.image.load("assets/man.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (50, 40))  # Resize bird

pipe_img = pygame.image.load("assets/bottompipe.png").convert_alpha()
pipe_img = pygame.transform.scale(pipe_img, (70, 400))  # Resize bottom pipe

pipe_top_img = pygame.image.load("assets/toppipe.png").convert_alpha()
pipe_top_img = pygame.transform.scale(pipe_top_img, (70, 400))  # Resize top pipe

front_img = pygame.image.load("assets/frontpic.png").convert_alpha()
front_img = pygame.transform.scale(front_img, (300, 200))  # Resize front image

# Bird settings
bird_rect = bird_img.get_rect(center=(100, SCREEN_HEIGHT//2))
gravity = 0.5
bird_movement = 0

# Pipe settings
pipe_gap = 160
pipe_speed = 3
pipe_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

# Score
score = 0
high_score = 0
can_score = True

# Game states
game_active = False   # main game running
start_screen = True   # show start screen first


# Functions ---------------------------
def create_pipe():
    height = random.randint(200, 400)
    bottom_pipe = pipe_img.get_rect(midtop=(500, height))
    top_pipe = pipe_top_img.get_rect(midbottom=(500, height - pipe_gap))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return [pipe for pipe in pipes if pipe.right > -50]


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:   # bottom pipe
            screen.blit(pipe_img, pipe)
        else:                              # top pipe
            screen.blit(pipe_top_img, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= SCREEN_HEIGHT:
        return False
    return True


def update_score(pipes):
    global score, can_score
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:  # only bottom pipes
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                can_score = False
        if pipe.centerx < 0:
            can_score = True


def score_display(state):
    if state == "main_game":
        score_surface = game_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH//2, 50))
        screen.blit(score_surface, score_rect)
    elif state == "game_over":
        score_surface = game_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH//2, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(high_score_surface, high_score_rect)


def start_screen_display():
    # Background
    screen.blit(bg, (0, 0))

    # Title text
    title_surface = game_font.render("Flappy Bird", True, (255, 255, 0))
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 150))
    screen.blit(title_surface, title_rect)

    # Get Ready text
    ready_surface = game_font.render("Get Ready!", True, (255, 255, 255))
    ready_rect = ready_surface.get_rect(center=(SCREEN_WIDTH//2, 220))
    screen.blit(ready_surface, ready_rect)

    # Front image
    front_rect = front_img.get_rect(center=(SCREEN_WIDTH//2, 350))
    screen.blit(front_img, front_rect)

    # Instruction
    inst_surface = game_font.render("Press SPACE to Start", True, (200, 200, 200))
    inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH//2, 500))
    screen.blit(inst_surface, inst_rect)


# Game loop ---------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start_screen:
                start_screen = False
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, SCREEN_HEIGHT//2)
                bird_movement = 0
                score = 0
                can_score = True

            elif event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8

            elif event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, SCREEN_HEIGHT//2)
                bird_movement = 0
                score = 0
                can_score = True

        if event.type == SPAWNPIPE and game_active:
            bottom_pipe, top_pipe = create_pipe()
            pipe_list.append(bottom_pipe)
            pipe_list.append(top_pipe)

    screen.blit(bg, (0, 0))

    if start_screen:
        start_screen_display()

    elif game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_img, bird_rect)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Collision
        game_active = check_collision(pipe_list)

        # Score
        update_score(pipe_list)
        score_display("main_game")

    else:
        if score > high_score:
            high_score = score
        score_display("game_over")

        pygame.display.update()
        clock .tick(60)
