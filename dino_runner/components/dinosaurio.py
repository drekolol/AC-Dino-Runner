import pygame


from pygame.sprite import Sprite

from dino_runner.components.text_utils import get_rect_centered_message
from dino_runner.utils.constants import RUNNING, DUCKING, JUMPING, DEFAULT_TYPE, DUCKING_SHIELD, SHIELD_TYPE, \
     RUNNING_SHIELD, JUMPING_SHIELD


class dinosaur (Sprite):
    X_POS = 45
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 10

    def __init__(self):
        self.duck_img = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}
        self.run_img = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}
        self.jump_image = {DEFAULT_TYPE: JUMPING,SHIELD_TYPE: JUMPING_SHIELD}
        self.type = DEFAULT_TYPE
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect()
        self.shield = False
        self.shield_time_up = 0
        self.show_text = False
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.stop_index = 0
        # Salto del Dinno
        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        #self.setup_state_booleans()

    #def setup_state_booleans(self):
        #self.has_powerup = False
        #self.shield = False
        #self.show_text = False
        #self.shield_time_up =0

    def update(self, user_input):
        if self.dino_jump:
            self.jump()

        if self.dino_run:
            self.run()

        if self.dino_duck:
            self.duck()

        if user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False

        elif user_input[pygame.K_UP] and not self.dino_jump or user_input[pygame.K_DOWN]:
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
            self.jump_vel -= 1

        elif not self.dino_jump:
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False
        if self.stop_index >= 10:
            self.stop_index = 0

    def run(self):
        self.image = self.run_img[self.type][self.stop_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.stop_index += 1

    def jump(self):
        self.image = self.jump_image[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 1
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_rect.y = self.Y_POS
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def duck(self):
        self.image = self.duck_img[self.type][self.stop_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.stop_index += 1

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def check_invincibility(self, screen):
        if self.shield:
            time_to_show = round((self.shield_time_up - pygame.time.get_ticks()) / 1000, 1)
            if time_to_show < 0:
                self.shield = False
                if self.type == SHIELD_TYPE:
                    self.type = DEFAULT_TYPE
            else:
                if self.show_text:
                    text, text_rect = get_rect_centered_message("Shield: " + str(time_to_show),
                                                           width=550,
                                                           height=100,
                                                           )
                    screen.blit(text, text_rect)

    def update_to_default(self, current_type):
                if self.type == current_type:
                    self.type = DEFAULT_TYPE
