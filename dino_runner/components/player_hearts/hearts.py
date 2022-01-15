from pygame.sprite import Sprite
from dino_runner.utils.constants import HEART


class Heart(Sprite):
    POS_Y = 10

    def __init__(self,pos_x):
        self.image = HEART
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = self.POS_Y

    def draw(self,screen):

        screen.blit(self.image, self.rect)



