import pygame as pg
from random import randint

class Pipe:
    def __init__(self, scale_factor, move_speed, screen_height):
        self.img_up = pg.transform.scale_by(pg.image.load("assets/pipeup.png").convert_alpha(), scale_factor)
        self.img_down = pg.transform.scale_by(pg.image.load("assets/pipedown.png").convert_alpha(), scale_factor)
        self.rect_up = self.img_up.get_rect()
        self.rect_down = self.img_down.get_rect()

        # Adjust pipe positions dynamically to screen height
        self.pipe_distance = int(0.35 * screen_height)
        self.rect_up.y = randint(int(0.4 * screen_height), int(0.75 * screen_height))
        self.rect_up.x = screen_height  # pipes start from right edge
        self.rect_down.y = self.rect_up.y - self.pipe_distance - self.rect_up.height
        self.rect_down.x = self.rect_up.x
        self.move_speed = move_speed

    def drawPipe(self, win):
        win.blit(self.img_up, self.rect_up)
        win.blit(self.img_down, self.rect_down)

    def update(self, dt):
        self.rect_up.x -= int(self.move_speed * dt)
        self.rect_down.x -= int(self.move_speed * dt)