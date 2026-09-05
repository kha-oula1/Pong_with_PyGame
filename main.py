import pygame
import random

# Constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")

    # Players
    paddle_1_rect = pygame.Rect(30, 0, 7, 100)
    paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 50, 0, 7, 100)

    paddle_1_move = 0
    paddle_2_move = 0

    # Ball
    ball_rect = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 25, 25)

    ball_accel_x = random.randint(2, 4) * 0.1
    ball_accel_y = random.randint(2, 4) * 0.1

    if random.randint(1, 2) == 1:
        ball_accel_x *= -1

    if random.randint(1, 2) == 1:
        ball_accel_y *= -1

    clock = pygame.time.Clock()
    started = False

    while True:
        screen.fill(COLOR_BLACK)

        # Start screen
        if not started:
            font = pygame.font.SysFont("Consolas", 30)

            text = font.render(
                "Press Space to Start",
                True,
                COLOR_WHITE
            )

            text_rect = text.get_rect()
            text_rect.center = (
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2
            )

            screen.blit(text, text_rect)
            pygame.display.flip()

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        started = True

            continue

        delta_time = clock.tick(60)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:

                # Player 1
                if event.key == pygame.K_w:
                    paddle_1_move = -0.5

                if event.key == pygame.K_s:
                    paddle_1_move = 0.5

                # Player 2
                if event.key == pygame.K_UP:
                    paddle_2_move = -0.5

                if event.key == pygame.K_DOWN:
                    paddle_2_move = 0.5

            if event.type == pygame.KEYUP:

                if event.key in (pygame.K_w, pygame.K_s):
                    paddle_1_move = 0.0

                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    paddle_2_move = 0.0

        # Move paddles
        paddle_1_rect.top += paddle_1_move * delta_time
        paddle_2_rect.top += paddle_2_move * delta_time

        # Keep paddles on screen
        if paddle_1_rect.top < 0:
            paddle_1_rect.top = 0

        if paddle_1_rect.bottom > SCREEN_HEIGHT:
            paddle_1_rect.bottom = SCREEN_HEIGHT

        if paddle_2_rect.top < 0:
            paddle_2_rect.top = 0

        if paddle_2_rect.bottom > SCREEN_HEIGHT:
            paddle_2_rect.bottom = SCREEN_HEIGHT

        # Ball out of bounds
        if ball_rect.left <= 0 or ball_rect.left >= SCREEN_WIDTH:
            return

        # Top collision
        if ball_rect.top < 0:
            ball_accel_y *= -1
            ball_rect.top = 0

        # Bottom collision
        if ball_rect.bottom > SCREEN_HEIGHT - ball_rect.height:
            ball_accel_y *= -1
            ball_rect.top = SCREEN_HEIGHT - ball_rect.height

        # Paddle collisions
        if (
            paddle_1_rect.colliderect(ball_rect)
            and paddle_1_rect.left < ball_rect.left
        ):
            ball_accel_x *= -1
            ball_rect.left += 5

        if (
            paddle_2_rect.colliderect(ball_rect)
            and paddle_2_rect.left > ball_rect.left
        ):
            ball_accel_x *= -1
            ball_rect.left -= 5

        # Move ball
        if started:
            ball_rect.left += ball_accel_x * delta_time
            ball_rect.top += ball_accel_y * delta_time

        # Draw
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)
        pygame.draw.rect(screen, COLOR_WHITE, ball_rect)

        pygame.display.update()


if __name__ == "__main__":
    main()