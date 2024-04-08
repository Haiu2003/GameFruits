import enum
from typing import Tuple, List

import random
import pygame
import sys
from common import SCREEN_WIDTH,SCREEN_HEIGHT,WHITE,RED,BLUE,FPS

# Khởi tạo Pygame
pygame.init()

# Tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hứng hoa quả")
clock = pygame.time.Clock()

# Load các sprite và scale chúng
BACKGROUND_SPRITE = pygame.image.load("assets/c550ba8f791e8b559ac51285648a47d6.jpg").convert_alpha()
BACKGROUND_SPRITE.set_alpha(128)
BACKGROUND_SPRITE = pygame.transform.scale(BACKGROUND_SPRITE, [SCREEN_WIDTH, SCREEN_HEIGHT])

APPLE_SPRITE = pygame.transform.scale(pygame.image.load("assets/apple-5902283_960_720.webp"), (50, 50))
STRAWBERRY_SPRITE = pygame.transform.scale(pygame.image.load("assets/strawberry-7895270_960_720.webp"), (50, 50))
BOMB_SPRITE = pygame.transform.scale(pygame.image.load("assets/bomb-png-5a371a5a414438.7272917215135606662673-removebg-preview.png"), (70, 50))
BASKET_SPRITE = pygame.transform.scale(pygame.image.load("assets/basket-removebg-preview.png"), (150, 150))


# Khai báo lớp giỏ
class Basket:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: pygame.Surface = BASKET_SPRITE
        self.move_speed = 6  # Adjust speed as needed
        self.move_left_pressed = False
        self.move_right_pressed = False


    def handle_event(self, event): #Hàm di chuyển để hứng quả
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left_pressed = True
            elif event.key == pygame.K_RIGHT:
                self.move_right_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move_left_pressed = False
            elif event.key == pygame.K_RIGHT:
                self.move_right_pressed = False

    def update(self):
        if self.move_left_pressed:
            self.move_left()
        elif self.move_right_pressed:
            self.move_right()

    def move_left(self) -> None:
        self.x -= self.move_speed
        if self.x < 0:
            self.x = 0

    def move_right(self) ->None:
        self.x += self.move_speed
        if self.x > SCREEN_WIDTH - self.image.get_width():
            self.x = SCREEN_WIDTH - self.image.get_width()
# Khai báo enum loại hoa quả
class ItemType(enum.Enum):
    APPLE = 0
    STRAWBERRY = 1
    BOMB = 2


# Khai báo lớp quả
class FruitItem:
    def __init__(self, x: float, y: float, type: ItemType) -> None:
        self.x: float = x
        self.y: float = y
        self.type: ItemType = type

        if type == ItemType.APPLE:
            self.image = APPLE_SPRITE
        elif type == ItemType.STRAWBERRY:
            self.image = STRAWBERRY_SPRITE
        else:
            self.image = BOMB_SPRITE
        self.fall_speed = 4

    def update(self) -> None:
        # Cập nhật vị trí của quả
        self.y += self.fall_speed

        # Kiểm tra nếu quả rơi xuống dưới cùng màn hình
        if self.y > SCREEN_HEIGHT:
            self.reset()

    def reset(self) -> None:
        # Đặt lại vị trí của quả khi rơi xuống dưới cùng màn hình
        self.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())  # Vị trí ngẫu nhiên
        self.y = random.randint(-200, -100)  # Vị trí ở trên đỉnh màn hình
        self.fall_speed = random.randint(2, 5)  # Tốc độ rơi ngẫu nhiên mới


# Khởi tạo giỏ
basket = Basket(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

# Khởi tạo danh sách các quả
list_items: List[FruitItem] = [
    FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-300, -100), ItemType.APPLE),
    FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-390, -100), ItemType.STRAWBERRY),
    FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-500, -100), ItemType.APPLE),
    FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-200, -100), ItemType.STRAWBERRY),
    FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-250, -100), ItemType.BOMB),
    FruitItem(random.randint(0, SCREEN_WIDTH - 50), random.randint(-350, -100), ItemType.BOMB),
]

def collision(basket, fruit):
    basket_rect = pygame.Rect(basket.x, basket.y, basket.image.get_width(), basket.image.get_height())
    fruit_rect = pygame.Rect(fruit.x, fruit.y, fruit.image.get_width(), fruit.image.get_height())
    return basket_rect.colliderect(fruit_rect)


def calculate_score(basket, item, score, collision_handled):
    if not collision_handled and collision(basket, item):
        collision_handled = True
        if item.type == ItemType.APPLE or item.type == ItemType.STRAWBERRY:
            score += 10
        else:
            score = 0
        item.reset()
    else:
        collision_handled = False
    return score, collision_handled

score = 0
font = pygame.font.SysFont(None, 36)
PLAY_TIME = 10
WINNING_SCORE = 50
time_remaining = PLAY_TIME * FPS
# Khởi tạo biến cờ để kiểm tra va chạm
collision_handled = False
game_over = False

# Vòng lặp chính của trò chơi
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            basket.handle_event(event)
    basket.update()
    # Xóa màn hình
    screen.fill(WHITE)

    # Hiển thị hình nền
    screen.blit(BACKGROUND_SPRITE, (0, 0))

    # Cập nhật và hiển thị các quả
    for item in list_items:
        item.update()
        screen.blit(item.image, (item.x, item.y))

        # Tính điểm
        score, collision_handled = calculate_score(basket, item, score, collision_handled)

        # Kiểm tra va chạm giữa giỏ và quả
        if collision(basket, item):
            print("Collision occurred!")

    # Hiển thị giỏ
    screen.blit(basket.image, (basket.x, basket.y))

    # Hiển thị điểm số
    text = font.render("Score: " + str(score), True, RED)
    screen.blit(text, (10, 10))

    # Hiển thị thời gian còn lại
    time_text = font.render("Time: " + str(max(0, time_remaining // FPS)), True, BLUE)
    screen.blit(time_text, (350, 10))

    # Cập nhật màn hình
    pygame.display.flip()

    # Đặt tốc độ khung hình
    clock.tick(FPS)
    if game_over:
        # Hiển thị kết quả
        result_text = font.render("Time's up! Your score: " + str(score), True, WHITE)
        screen.blit(result_text, (150, 200))
        # Hiển thị lựa chọn chơi lại
        restart_text = font.render("Press Y to play again", True, WHITE)
        screen.blit(restart_text, (150, 250))
        # Kiểm tra lựa chọn của người chơi
        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            # Reset trò chơi để chơi lại từ đầu
            score = 0
            time_remaining = PLAY_TIME * FPS
            game_over = False
    # Giảm thời gian còn lại sau mỗi khung hình
    if not game_over:
        time_remaining -= 1

    # if time_remaining <= 0:
    #     game_over = True
    #     screen.fill(WHITE)
    #
    #     score_text = font.render("Your score: " + str(score), True,RED)
    #     score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 -100))
    #
    #     game_over_text = font.render("Game Over",True,BLUE)
    #     game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 -100))
    #
    #     screen.blit(game_over_text,game_over_rect)
    #
    #     pygame.display.flip()
    #     pygame.time.wait(5000)
    #
    #     score = 0
    #     time_remaining = PLAY_TIME * FPS
    #     game_over = False
    # Kiểm tra va chạm với biên của màn hình
    if basket.x < 0:
        basket.x = 0
    elif basket.x > SCREEN_WIDTH - basket.image.get_width():
        basket.x = SCREEN_WIDTH - basket.image.get_width()
# Kết thúc Pygame
pygame.quit()
