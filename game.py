import pygame as pg
import sys, time
from bird import Bird
from pipe import Pipe

pg.init()
pg.mixer.init()

class Game:
    def __init__(self):  
        # 🔊 Soft continuous background music
        pg.mixer.music.load("assets/sfx/soft_bg_music.mp3")  # Path to your sound file
        pg.mixer.music.set_volume(0.15)  # 0.0 to 1.0 (adjust for softness)
        pg.mixer.music.play(-1)  # -1 means loop forever

        # Fullscreen setup
        self.win = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.width, self.height = self.win.get_size()

        self.scale_factor = self.width / 600  # auto-scale based on your screen width
        self.clock = pg.time.Clock()
        self.move_speed = 250
        self.bird = Bird(self.scale_factor)
        self.cracker_sound = pg.mixer.Sound("assets/sfx/cracker.wav")
        self.next_milestone = 25

        # Game states
        self.is_enter_pressed = False
        self.is_game_started = False
        self.pipes = []
        self.pipe_generate_counter = 71
        self.score = 0
        self.font = pg.font.SysFont("Arial", 50, bold=True)
        self.dead_sound_played = False

        # Texts
        self.start_img = self.font.render("START", True, (0, 0, 0))
        self.restart_img = self.font.render("RESTART", True, (0, 0, 0))
        self.start_rect = self.start_img.get_rect(center=(self.width // 2, self.height - 90))
        self.restart_rect = self.restart_img.get_rect(center=(self.width // 2, self.height - 90))

        self.setUpBgAndGround()
        self.gameLoop()

    def setUpBgAndGround(self):
        # Backgrounds
        self.bg_day = pg.image.load("assets/bg_day.png").convert()
        self.bg_day = pg.transform.scale(self.bg_day, (self.width, self.height))

        self.bg_night = pg.image.load("assets/bg_night.png").convert()
        self.bg_night = pg.transform.scale(self.bg_night, (self.width, self.height))

        self.bg_transition = 0
        self.is_day = True

        # Ground images (scaled to full width but half height)
        self.ground_img = pg.image.load("assets/ground.png").convert()
        original_ground_height = self.ground_img.get_height()
        ground_height = int(original_ground_height * self.scale_factor * 0.5)
        self.ground_img = pg.transform.scale(self.ground_img, (self.width, ground_height))

        # Two ground images for scrolling
        self.ground1_img = self.ground_img.copy()
        self.ground2_img = self.ground_img.copy()

        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = self.height - ground_height
        self.ground2_rect.y = self.height - ground_height

    def gameLoop(self):
        last_time = time.time()
        while True:
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    if event.key == pg.K_SPACE and self.is_enter_pressed:
                        self.bird.flap(dt)

                if event.type == pg.MOUSEBUTTONDOWN:
                    if not self.is_game_started and self.start_rect.collidepoint(event.pos):
                        self.startGame()
                    elif self.is_game_started and not self.is_enter_pressed and self.restart_rect.collidepoint(event.pos):
                        self.__init__()

            self.updateEverything(dt)
            self.checkCollisions()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

    def startGame(self):
        self.is_game_started = True
        self.is_enter_pressed = True
        self.bird.update_on = True
        self.score = 0
        self.dead_sound_played = False
        self.pipes.clear()
        self.bird.rect.center = (self.width // 5, self.height // 3)
        self.bird.y_velocity = 0
        self.bg_transition = 0
        self.is_day = True

    def checkCollisions(self):
        ground_y = self.height - self.ground1_rect.height
        if len(self.pipes):
            if self.bird.rect.bottom > ground_y:
                if not self.dead_sound_played:
                    self.bird.dead_sound.play()
                    self.dead_sound_played = True
                self.bird.update_on = False
                self.is_enter_pressed = False
            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
                self.bird.rect.colliderect(self.pipes[0].rect_up)):
                if not self.dead_sound_played:
                    self.bird.dead_sound.play()
                    self.dead_sound_played = True
                self.is_enter_pressed = False

    def updateEverything(self, dt):
        if self.is_enter_pressed:
            # Move ground
            self.ground1_rect.x -= int(self.move_speed * dt)
            self.ground2_rect.x -= int(self.move_speed * dt)

            if self.ground1_rect.right < 0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right < 0:
                self.ground2_rect.x = self.ground1_rect.right

            # Generate pipes dynamically
            if self.pipe_generate_counter > 80:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed, self.height))
                self.pipe_generate_counter = 0
            self.pipe_generate_counter += 1

            for pipe in self.pipes:
                pipe.update(dt)

            if len(self.pipes) != 0:
                if self.pipes[0].rect_up.right < 0:
                    self.pipes.pop(0)
                    self.score += 1 
                    if self.score == self.next_milestone:
                        self.cracker_sound.play()
                        self.next_milestone += 25
                        self.is_day = not self.is_day

            target = 0 if self.is_day else 1
            speed = 0.3
            if self.bg_transition < target:
                self.bg_transition = min(1, self.bg_transition + dt * speed)
            elif self.bg_transition > target:
                self.bg_transition = max(0, self.bg_transition - dt * speed)

        self.bird.update(dt)

    def drawEverything(self):
        blended_bg = pg.Surface(self.bg_day.get_size()).convert()
        blended_bg.blit(self.bg_day, (0, 0))
        night_overlay = self.bg_night.copy()
        night_overlay.set_alpha(int(self.bg_transition * 255))
        blended_bg.blit(night_overlay, (0, 0))
        self.win.blit(blended_bg, (0, 0))

        for pipe in self.pipes:
            pipe.drawPipe(self.win)

        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)

        font = pg.font.SysFont("Arial", 36, bold=True)
        score_text = font.render(f"SCORE: {self.score}", True, (0, 0, 0))  
        self.win.blit(score_text, (20, 20)) 

        if not self.is_game_started:
            pg.draw.rect(self.win, (255, 255, 0), self.start_rect.inflate(40, 20), border_radius=10)
            self.win.blit(self.start_img, self.start_rect)
        elif not self.is_enter_pressed:
            pg.draw.rect(self.win, (255, 0, 0), self.restart_rect.inflate(40, 20), border_radius=10)
            self.win.blit(self.restart_img, self.restart_rect)


if __name__ == "__main__":
    Game()
