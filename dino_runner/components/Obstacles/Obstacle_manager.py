import random

import pygame.time


from dino_runner.components.Obstacles.Cactus import Cactus,Bird_down,Bird
from dino_runner.utils.constants import SMALL_CACTUS,LARGE_CACTUS,BIRD


class obstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):

        list_obstacles = [1,2,3,4]

        if len(self.obstacles) == 0:

            cactusv = random.choice(list_obstacles)
            if cactusv == 1:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif cactusv == 2:
                self.obstacles.append(Cactus(LARGE_CACTUS))
            elif cactusv == 3:
                self.obstacles.append(Bird(BIRD))
            elif cactusv == 4:
                self.obstacles.append(Bird_down(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1)
                game.playing = False
                game.death_count += 1
                break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []