from character import Character

from typing import Self
from pygame import Vector2, display
import numpy as np

class Game:
    def __init__(self:Self) -> None:
        self.screen_size:Vector2 = Vector2(display.get_desktop_sizes()[0])
        self.screen_grid_size:Vector2 = Vector2(5, 5)
        self.screen_grid:np.array = np.arange(int(self.screen_grid_size.x * self.screen_grid_size.y))

        self.character:Character = Character({"screen_size": self.screen_size, 
                                              "grid_size": self.screen_grid_size, 
                                              "grid": self.screen_grid})

    def run(self:Self) -> None:
        while True:
            self.character.update()