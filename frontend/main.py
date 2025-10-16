import pygame as pg
import subprocess
import sys
import math

pg.init()
pg.mixer.init()

# Window
WIDTH, HEIGHT = 1000, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flappy Bird Menu")

# Load background
bg = pg.image.load("frontend/assets/new_image.png").convert()
bg = pg.transform.scale(bg, (WIDTH, HEIGHT))

# Fonts
title_font = pg.font.SysFont("Comic Sans MS", 80, bold=True)
button_font = pg.font.SysFont("Arial", 40, bold=True)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 180, 255)
BLACK = (0, 0, 0)

# Background Music
try:
    pg.mixer.music.load("frontend/assets/menu_music.mp3")
    pg.mixer.music.play(-1)
except:
    pass  # skip if not available


# ------------------ BUTTON CLASS ------------------
class Button:
    def __init__(self, text, y):
        self.text = text
        self.rect = pg.Rect(WIDTH // 2 - 100, y, 200, 60)

    def draw(self, surf, mouse_pos):
        color = GREEN if self.rect.collidepoint(mouse_pos) else BLUE
        pg.draw.rect(surf, color, self.rect, border_radius=15)
        text_surf = button_font.render(self.text, True, WHITE)
        surf.blit(text_surf, text_surf.get_rect(center=self.rect.center))


# ------------------ TITLE ANIMATION ------------------
def draw_title(time_elapsed):
    offset = math.sin(time_elapsed * 2) * 10
    title = title_font.render("FLAPPY BIRD", True, (255, 255, 0))
    shadow = title_font.render("FLAPPY BIRD", True, BLACK)
    x_shift = -260
    screen.blit(shadow, (WIDTH // 2 + x_shift - 2, 152 + offset))
    screen.blit(title, (WIDTH // 2 + x_shift, 150 + offset))


# ------------------ GRADIENT TEXT FUNCTION ------------------
def create_gradient_text(text, font, gradient_colors):
    """Creates a text surface with a left-to-right color gradient."""
    text_surface = font.render(text, True, (255, 255, 255))
    text_width, text_height = text_surface.get_size()

    gradient = pg.Surface((text_width, text_height)).convert_alpha()
    for x in range(text_width):
        ratio = x / text_width
        r = int(gradient_colors[0][0] * (1 - ratio) + gradient_colors[1][0] * ratio)
        g = int(gradient_colors[0][1] * (1 - ratio) + gradient_colors[1][1] * ratio)
        b = int(gradient_colors[0][2] * (1 - ratio) + gradient_colors[1][2] * ratio)
        pg.draw.line(gradient, (r, g, b), (x, 0), (x, text_height))
    gradient.blit(text_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
    return gradient


# ------------------ INSTRUCTIONS SCREEN ------------------
def show_instructions():
    running = True
    while running:
        screen.fill((178, 34, 34)) # Purple background

        lines = [
            "✨ HOW TO PLAY ✨",
            "🕹️ Press SPACEBAR to make the bird flap",
            "🚧 Avoid crashing into the pipes",
            "🏆 Earn points as you fly through gaps",
            "💡 Tip: Stay calm, time your flaps carefully!",
            "⬅️ Click anywhere to return to the main menu"
        ]

        y = 120
        for i, line in enumerate(lines):
            if i == 0:
                font = pg.font.SysFont("Comic Sans MS", 54, bold=True)
                colors = ((255, 0, 127), (0, 255, 255))  # Pink → Cyan
            else:
                font = pg.font.SysFont("Arial", 34, bold=False)
                colors = ((255, 255, 0), (255, 105, 180))  # Yellow → Hot Pink

            gradient_text = create_gradient_text(line, font, colors)
            text_rect = gradient_text.get_rect(center=(WIDTH // 2, y))
            screen.blit(gradient_text, text_rect)
            y += 60

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                running = False

        pg.display.update()


# ------------------ MAIN MENU LOOP ------------------
def main():
    clock = pg.time.Clock()
    running = True
    start_time = pg.time.get_ticks() / 1000

    start_btn = Button("PLAY", 320)
    help_btn = Button("HELP", 400)
    exit_btn = Button("EXIT", 480)

    while running:
        dt = clock.tick(60) / 1000
        mouse_pos = pg.mouse.get_pos()
        time_elapsed = pg.time.get_ticks() / 1000 - start_time

        screen.blit(bg, (0, 0))
        draw_title(time_elapsed)
        start_btn.draw(screen, mouse_pos)
        help_btn.draw(screen, mouse_pos)
        exit_btn.draw(screen, mouse_pos)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(); sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if start_btn.rect.collidepoint(mouse_pos):
                    pg.mixer.music.stop()
                    subprocess.run(["python", "game.py"])
                elif help_btn.rect.collidepoint(mouse_pos):
                    show_instructions()
                elif exit_btn.rect.collidepoint(mouse_pos):
                    pg.quit(); sys.exit()

        pg.display.update()


if __name__ == "__main__":
    main()
