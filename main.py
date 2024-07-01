import pygame
import win32api
import win32con
import win32gui
import random
import math
import numpy as np

from typing import Self

pygame.init()

class Character():
    MAX_SPEED = .005

    def __init__(self:Self) -> None:
        self.sprite:pygame.SurfaceType = pygame.Surface((50, 50))
        self.rect:pygame.Rect = self.sprite.get_rect()

        self.sprite.fill("red")

        self.velocity:pygame.Vector2 = pygame.Vector2()
        self.pos:pygame.Vector2 = pygame.Vector2(200, 500)

        self.display_setup()
        self.flags()
        self.window_handle()

        self.update_pos_to_grid()

    def display_setup(self:Self) -> None:
        self.screen:pygame.SurfaceType = pygame.display.set_mode(self.rect.size, pygame.NOFRAME)
        self.transparent_color:tuple = (255, 0, 128)

    def flags(self:Self) -> None:
        self.isWander:bool = True
        self.reachedDes:bool = True

    def window_handle(self:Self) -> None:
        # Create layered window
        self.hwnd:int = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE,
                            win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(*self.transparent_color), 0, win32con.LWA_COLORKEY)
        # Set window topmost
        win32gui.SetWindowPos(self.hwnd, -1, int(self.pos.x), int(self.pos.y), 0, 0, 1)

    def update_pos(self:Self) -> None:
        try:
            self.velocity.clamp_magnitude_ip(self.MAX_SPEED)
        except ValueError:
            pass
        self.pos += self.velocity

        # self.pos.x = abs(self.pos.x)
        # self.pos.y = abs(self.pos.y)

        win32gui.SetWindowPos(self.hwnd, -1, int(self.pos.x), int(self.pos.y), 0, 0, 1)
        if self.pos.distance_squared_to(self.destination) <= 100:
            self.reachedDes = True

    def update_pos_to_grid(self:Self) -> np.array:
        x:int
        y:int
        i:int
        j:int
        x, y = round(self.pos.x / screen_size.x * screen_grid_size.x), round(self.pos.y / screen_size.y * screen_grid_size.y)
        a:list = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                n:int = int(screen_grid_size.x * y + x + screen_grid_size.x * i + j)
                if n < screen_grid.__len__() and n > -1:
                    a.append(n)

        return np.delete(screen_grid, a)

    def wander(self:Self) -> None:
        a:np.array = self.update_pos_to_grid()
        c:int = random.choice(a)
        c_x:int
        c_y:int
        c_x, c_y = c//screen_grid_size.x, c%screen_grid_size.y

        self.destination:pygame.Vector2 = pygame.Vector2(
            random.randint(int(c_x / screen_grid_size.x * screen_size.x), int((c_x+1) / screen_grid_size.x * screen_size.x)),
            random.randint(int(c_y / screen_grid_size.y * screen_size.y), int((c_y+1) / screen_grid_size.y * screen_size.y))
        )

        self.velocity = (self.destination - self.pos).normalize()
        self.reachedDes = False

    def pos_to(self:Self, des:tuple|pygame.Vector2) -> None:
        pass

    def update(self:Self) -> None:
        for e in pygame.event.get():
            pass

        if self.isWander and self.reachedDes:
            self.wander()
        
        self.update_pos()
        
        self.screen.fill(self.transparent_color)  # Transparent background
        self.screen.blit(self.sprite, self.rect)
        
        pygame.display.update()



if __name__ == "__main__":
    screen_size = pygame.Vector2(pygame.display.get_desktop_sizes()[0])
    screen_grid_size = pygame.Vector2(5, 5)
    screen_grid = np.arange(int(screen_grid_size.x * screen_grid_size.y))

    # clock = pygame.time.Clock()
    a = Character()
    while True:
        a.update()
        # clock.tick(60)