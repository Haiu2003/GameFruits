from typing import Tuple

from common import SCREEN_WIDTH,SCREEN_HEIGHT,FPS,WHITE

import random
import pygame

from pygame import Surface

screen: Surface = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
clock = pygame.time.Clock()

def scale_image(image:Surface, scale:int) -> Surface:
    """Resize image by a factor of input arg `scale`."""
    new_dimension: Tuple[int,int] =(
        int(image.get_width()*scale), int(image.get_height()*scale)
    )
    return pygame.transform.scale(image,new_dimension)


BACKGROUND_SPRITE: Surface = pygame.image.load("assets/background.jpg").convert_alpha()
BACKGROUND_SPRITE.set_alpha(128)
BACKGROUND_SPRITE = pygame.transform.scale(BACKGROUND_SPRITE,[SCREEN_WIDTH,SCREEN_HEIGHT])

APPLE_SPRITE: Surface = scale_image(pygame.image.load("assets/apple-5902283_960_720.webp"),0.15)
BOMB_SPRITE: Surface = scale_image(pygame.image.load("assets/assets/bomb-png-5a371a5a414438.7272917215135606662673-removebg-preview.png"),0.15)
BASKET_SPRITE: Surface = scale_image(pygame.image.load("assets/basket-removebg-preview.png"),0.15)


running: bool = True
while running:
    if pygame.event.peek(pygame.QUIT):
        running = False
        break
    screen.fill(WHITE)
    screen.blit(BACKGROUND_SPRITE,(0,0))
    screen.blit(APPLE_SPRITE, (20,  0))
    screen.blit(APPLE_SPRITE, (210, 0))
    screen.blit(APPLE_SPRITE, (400, 0))
    screen.blit(BASKET_SPRITE,(250,450))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()