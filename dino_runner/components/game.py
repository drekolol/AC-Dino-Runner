import pygame

from dino_runner.components.Obstacles.power_ups.powerup_manager import PowerUpManager
from dino_runner.components.player_hearts.heart_manager import hearts_manager

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, RUNNING, DINODEAD, GAME_OVER
from dino_runner.components.dinosaurio import dinosaur
from dino_runner.components.Obstacles.Obstacle_manager import obstacleManager
from dino_runner.components import text_utils


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = dinosaur()
        self.Obstacle_manager = obstacleManager()
        self.power_up_manager = PowerUpManager()
        self.hearts_manager = hearts_manager()
        self.points = 0
        self.running = True
        self.death_count = 0

    def run(self):
        # Game loop: events - update - draw
        self.Obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups(self.points,self.player)
        self.hearts_manager.reset_counter_hearts()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.Obstacle_manager.update(self)
        self.power_up_manager.update(self.game_speed, self.player,self.points)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.score()
        self.clock.tick(FPS)
        self.draw_background()
        self.player.draw(self.screen)
        self.Obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.hearts_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def score(self):
        self.points += 1

        if self .points % 100 == 0:
             self.game_speed += 1

        text,text_rect = text_utils.get_rect_score_element(self.points)
        self.screen.blit(text, text_rect)
        self.player.check_invincibility(self.screen)

    def print_menu_elements(self):
        half_screen_height = SCREEN_HEIGHT //2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            text, text_rect = text_utils.get_rect_centered_message('Press any key to start')
            self.screen.blit(text, text_rect)
            self.screen.blit(RUNNING[0], (half_screen_width - 30, half_screen_height - 140))


        else:
            text, text_rect = text_utils.get_rect_centered_message('Press any key to restart ')
            self.screen.blit(text, text_rect)
            self.screen.blit(DINODEAD, (half_screen_width -40, half_screen_height - 200))
            self.screen.blit(GAME_OVER, (half_screen_width - 190, half_screen_height - 250))

            score, score_max = text_utils.get_rect_centered_message('Points: ' +str(self.points),height = 450 )
            self.screen.blit(score, score_max)

            scores, scores_max = text_utils.get_rect_centered_message('Death: ' +str(self.death_count),height =500)
            self.screen.blit(scores, scores_max)

    def show_menu(self):
        self.running = True

        white_color = (255, 255, 255)
        self.screen.fill(white_color)

        self.print_menu_elements()

        pygame.display.update()

        self.handle_key_events_on_menu()

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               self.running = False
               self.playing = False
               pygame.display.quit()
               pygame.quit()
               exit()
            if event.type == pygame.KEYDOWN:
                self.run()
