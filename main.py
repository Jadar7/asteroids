import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    elapsed_time = pygame.time.get_ticks() / 1000
    dt = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable

    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    print(
        f"Starting Asteroids with pygame version: {pygame.version.ver}\n"
        f"Screen width: {SCREEN_WIDTH}\n"
        f"Screen height: {SCREEN_HEIGHT}"
    )

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        for a in asteroids:
            if a.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                print(
                    f"You destroyed {player.score} asteroids and survived {elapsed_time} seconds!"
                )
                sys.exit()

            for s in shots:
                if a.collides_with(s):
                    log_event("asteroid_shot")
                    player.score += 1
                    a.split()
                    s.kill()

        pygame.Surface.fill(screen, "black")
        for d in drawable:
            d.draw(screen)
        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
