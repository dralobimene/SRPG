# Fichier: classes/canvases/canvas00_base.py

from typing import Tuple
import pygame


class BaseCanvas:
    def __init__(self,
                 width: int,
                 height: int,
                 color: Tuple[int, int, int],
                 x: int,
                 y: int,
                 alpha: int) -> None:

        self.canvas: pygame.Surface = pygame.Surface((width, height))
        self.color = color
        self.canvas.fill(self.color)
        self.x: int = x
        self.y: int = y
        self.displayed: bool = False
        self.focused: bool = False
        self._alpha: int = alpha

    # Getter pour l'attribut displayed
    @property
    def is_displayed(self) -> bool:
        return self.displayed

    # Setter pour l'attribut displayed
    @is_displayed.setter
    def is_displayed(self, value: bool) -> None:
        self.displayed = value

    # Getter pour l'attribut focused
    @property
    def is_focused(self) -> bool:
        return self.focused

    # Setter pour l'attribut focused
    @is_focused.setter
    def is_focused(self, value: bool) -> None:
        self.focused = value

    # Getter pour l'attribut alpha
    @property
    def alpha(self) -> int:
        return self._alpha

    # Setter pour l'attribut alpha
    @alpha.setter
    def alpha(self, alpha_value: int) -> None:
        if 0 <= alpha_value <= 255:
            self.canvas.set_alpha(alpha_value)
            self._alpha = alpha_value
        else:
            raise ValueError("Alpha value must be between 0 and 255.")

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.canvas, (self.x, self.y))

    def get_rect(self, **kwargs) -> pygame.Rect:
        rect = self.canvas.get_rect()
        for key, value in kwargs.items():
            setattr(rect, key, value)
        return rect

    def get_height(self) -> int:
        return self.canvas.get_height()
