import random

import pygame

from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    POWERUP_GROWTH_RATE,
    POWERUP_MAX_RADIUS,
    POWERUP_RADIUS,
)


class Powerup(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, POWERUP_RADIUS)
        self.active = False

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "cyan", self.position, self.radius, LINE_WIDTH)

    def activate(self):
        self.active = True

    def update(self, dt: float) -> None:
        if self.active:
            self.radius += POWERUP_GROWTH_RATE * dt
        if self.radius >= POWERUP_MAX_RADIUS:
            self.kill()
        return
