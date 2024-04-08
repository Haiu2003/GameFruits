import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hứng hoa quả")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Định nghĩa các biến
player_width = 50
player_height = 50
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height
player_speed = 5

fruit_width = 50
fruit_height = 50
fruit_x = random.randint(0, screen_width - fruit_width)
fruit_y = -fruit_height
fruit_speed = 3

score = 0

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


# Hàm vẽ người chơi
def draw_player(x, y):
    pygame.draw.rect(screen, RED, [x, y, player_width, player_height])


# Hàm vẽ hoa quả
def draw_fruit(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, fruit_width, fruit_height])


# Hàm kiểm tra va chạm
def collision(player_x, player_y, fruit_x, fruit_y):
    if (player_x + player_width >= fruit_x and player_x <= fruit_x + fruit_width and
            player_y + player_height >= fruit_y and player_y <= fruit_y + fruit_height):
        return True
    return False


# Vòng lặp chính của trò chơi
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Di chuyển hoa quả xuống dưới
    fruit_y += fruit_speed
    if fruit_y > screen_height:
        fruit_x = random.randint(0, screen_width - fruit_width)
        fruit_y = -fruit_height
        score += 1

    # Kiểm tra va chạm
    if collision(player_x, player_y, fruit_x, fruit_y):
        fruit_x = random.randint(0, screen_width - fruit_width)
        fruit_y = -fruit_height
        score += 10

    # Vẽ người chơi và hoa quả
    draw_player(player_x, player_y)
    draw_fruit(fruit_x, fruit_y)

    # Hiển thị điểm số
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
