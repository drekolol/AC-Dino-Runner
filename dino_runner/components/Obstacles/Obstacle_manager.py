import random

import pygame.time


from dino_runner.components.Obstacles.Cactus import Bird, LargeCactus, SmallCactus
from dino_runner.utils.constants import SMALL_CACTUS,LARGE_CACTUS,BIRD


class obstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):

        cactus_list = [1, 2, 3]
        if len(self.obstacles) == 0:
            cactus = random.choice(cactus_list)
            if cactus == 1:
                self.obstacles.append(SmallCactus(SMALL_CACTUS))
            elif cactus == 2:
                self.obstacles.append(LargeCactus(LARGE_CACTUS))
            elif cactus == 3:
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.shield:
                  self.obstacles.remove(obstacle)
                else:
                      if game.hearts_manager.hearts_counter > 1:
                         game.hearts_manager.hearts_counter -= 1
                         game.player.dino_rect.colliderect(obstacle.rect)
                         self.obstacles.remove(obstacle)


                      else:
                          game.playing = False
                          game.death_count += 1
                          break
            else:
                self.obstacles

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []