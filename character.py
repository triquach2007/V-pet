import pygame
import win32api
import win32con
import win32gui
import random
import numpy as np

from typing import Self
from types import FunctionType


class Character():
    MAX_SPEED = .005

    def __init__(self:Self, screen_data:dict) -> None:
        self.screen_data:dict = screen_data
        self.sprite:pygame.SurfaceType = pygame.Surface((50, 50))
        self.rect:pygame.Rect = self.sprite.get_rect()

        self.sprite.fill("red")

        self.velocity:pygame.Vector2 = pygame.Vector2()
        self.pos:pygame.Vector2 = pygame.Vector2(200, 500)
        self.destination: pygame.Vector2 = pygame.Vector2()

        self.hooks:list = []

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
        x, y = round(self.pos.x / self.screen_data["screen_size"].x * self.screen_data["grid_size"].x), round(self.pos.y / self.screen_data["screen_size"].y * self.screen_data["grid_size"].y)
        a:list = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                n:int = int(self.screen_data["grid_size"].x * y + x + self.screen_data["grid_size"].x * i + j)
                if n < self.screen_data["grid"].__len__() and n > -1:
                    a.append(n)

        return np.delete(self.screen_data["grid"], a)
    
    def pos_to(self:Self, des:tuple|pygame.Vector2) -> None:
        self.destination = des

        self.velocity = (self.destination - self.pos).normalize()
        self.reachedDes = False

    def wander(self:Self) -> None:
        a:np.array = self.update_pos_to_grid()
        c:int = random.choice(a)
        c_x:int
        c_y:int
        c_x, c_y = c//self.screen_data["grid_size"].x, c%self.screen_data["grid_size"].y

        self.pos_to(
            pygame.Vector2(
            random.randint(int(c_x / self.screen_data["grid_size"].x * self.screen_data["screen_size"].x), int((c_x+1) / self.screen_data["grid_size"].x * self.screen_data["screen_size"].x)),
            random.randint(int(c_y / self.screen_data["grid_size"].y * self.screen_data["screen_size"].y), int((c_y+1) / self.screen_data["grid_size"].y * self.screen_data["screen_size"].y))
        ))

    def hotkey_hook(self:Self, function:FunctionType, key:str, modifiers:tuple|list|None=(), external_args:tuple|list|None=(), internal_args:tuple|list|None=()):
        self.hooks.append({
            "modifiers": tuple(modifiers),
            "key": key,
            "function": function,
            "external_args":external_args,
            "internal_args":internal_args
        })

    # def event_handler(self:Self) -> None:
    #     for e in pygame.event.get():
    #         pass

    #     for h in self.hooks:
    #         if 
    #         internal_text = [f"self.{i}" for i in h["internal_args"]]
    #         exec(f"""\
    #         h['function'](external = h['external_args'], internal = interal_text) 
    #         """)

    def update(self:Self) -> None:
        self.event_handler()

        if self.isWander and self.reachedDes:
            self.wander()
        
        self.update_pos()
        
        self.screen.fill(self.transparent_color)  # Transparent background
        self.screen.blit(self.sprite, self.rect)
        
        pygame.display.update()