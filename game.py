import pygame
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Monster")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Load image
monster = pygame.image.load("monster.png")
monster = pygame.transform.scale(monster, (50, 50))

# Load sounds
jump_sound = pygame.mixer.Sound("jump.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

# Fonts
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)

clock = pygame.time.Clock()

def reset_game():
    return {
        "x": 50,
        "y": HEIGHT // 2,
        "velocity": 0,
        "pipes": [[WIDTH, random.randint(150, 400)]],
        "passed": [False],
        "score": 0,
        "game_over": False
    }

game = reset_game()

gravity = 0.5
jump = -8
pipe_width = 60
gap = 150
pipe_speed = 3

running = True

while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game["game_over"]:
                game["velocity"] = jump
                jump_sound.play()

            if event.key == pygame.K_r and game["game_over"]:
                game = reset_game()

    if not game["game_over"]:
        # Gravity
        game["velocity"] += gravity
        game["y"] += game["velocity"]

        # Move pipes
        for pipe in game["pipes"]:
            pipe[0] -= pipe_speed

        # Add new pipe
        if game["pipes"][-1][0] < 200:
            game["pipes"].append([WIDTH, random.randint(150, 400)])
            game["passed"].append(False)

        # Remove old pipe
        if game["pipes"][0][0] < -pipe_width:
            game["pipes"].pop(0)
            game["passed"].pop(0)

        # Collision + scoring
        for i, pipe in enumerate(game["pipes"]):
            px, ph = pipe

            # Score
            if not game["passed"][i] and px + pipe_width < game["x"]:
                game["score"] += 1
                game["passed"][i] = True

            # Collision
            if game["x"] < px + pipe_width and game["x"] + 50 > px:
                if game["y"] < ph or game["y"] + 50 > ph + gap:
                    game["game_over"] = True
                    hit_sound.play()

        # Top/bottom collision
        if game["y"] > HEIGHT or game["y"] < 0:
            game["game_over"] = True
            hit_sound.play()

    # Draw player
    screen.blit(monster, (game["x"], game["y"]))

    # Draw pipes
    for pipe in game["pipes"]:
        px, ph = pipe
        pygame.draw.rect(screen, GREEN, (px, 0, pipe_width, ph))
        pygame.draw.rect(screen, GREEN, (px, ph + gap, pipe_width, HEIGHT))

    # Draw score
    score_text = font.render(f"Score: {game['score']}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Game over text
    if game["game_over"]:
        text = big_font.render("LOSER", True, RED)
        screen.blit(text, (110, 250))

        restart_text = font.render("Press R to Restart", True, (0, 0, 0))
        screen.blit(restart_text, (90, 320))

    pygame.display.update()

pygame.quit()