import random
import sys
from random import Random

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import (
    POWERUP_MAX_COUNT,
    POWERUP_SPAWN_COOLDOWN,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from logger import log_event, log_state
from player import Player
from powerup import Powerup
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0

    powerup_cooldown = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Powerup.containers = (powerups, updatable, drawable)
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

        elapsed_time = pygame.time.get_ticks() / 1000

        updatable.update(dt)

        if (
            player.score > 0
            and player.score % 5 == 0
            and len(powerups) < POWERUP_MAX_COUNT
            and powerup_cooldown <= elapsed_time
        ):
            Powerup(
                random.uniform(10, SCREEN_WIDTH - 10),
                random.uniform(10, SCREEN_HEIGHT - 10),
            )
            powerup_cooldown = elapsed_time + POWERUP_SPAWN_COOLDOWN

        for p in powerups:
            if p.collides_with(player):
                log_event("powerup_collected")
                p.activate()

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

            for p in powerups:
                if a.collides_with(p) and p.active:
                    log_event("asteroid_destroyed")
                    player.score += 1
                    a.split()

        pygame.Surface.fill(screen, "black")
        for d in drawable:
            d.draw(screen)
        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
