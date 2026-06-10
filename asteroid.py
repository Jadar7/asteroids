import random
from ssl import RAND_add
from types import new_class

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        rand_angle = random.uniform(20, 50)
        new_asteroid_1_velocity = self.velocity.rotate(rand_angle)
        new_asteroid_2_velocity = self.velocity.rotate(-rand_angle)
        new_asteroid_radius = self.radius - ASTEROID_MIN_RADIUS

        new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_asteroid_radius)
        new_asteroid_2 = Asteroid(self.position.x, self.position.y, new_asteroid_radius)

        new_asteroid_1.velocity = new_asteroid_1_velocity * 1.2
        new_asteroid_2.velocity = new_asteroid_2_velocity * 1.2

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
