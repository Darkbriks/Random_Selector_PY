import os
import pygame

from reel import reel

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)
ORANGE = (255, 130, 0)


def get_next_line(f):
    line = f.readline()
    while line and (line[0] == '#' or line == '\n'):
        if not line:
            return None
        line = f.readline()
    return line


class Window:
    def __init__(self, width, height, config):
        self.width = width
        self.height = height

        with open(config, 'r') as f:
            self.data_file = get_next_line(f).strip()
            self.icon = get_next_line(f).strip()

            self.title = get_next_line(f).strip()
            self.title_image = pygame.image.load(self.title.split("/!/")[0]) if os.path.splitext(self.title.split("/!/")[0])[1] in ['.jpg', '.png', '.jpeg'] else None
            if self.title_image:
                self.title_image_width = int(self.title.split("/!/")[1])
                self.title_image_height = int(self.title.split("/!/")[2])
                self.title_image = pygame.transform.scale(self.title_image, (self.title_image_width, self.title_image_height))

            self.second_title = get_next_line(f).strip()
            self.second_title_image = pygame.image.load(self.second_title.split("/!/")[0]) if os.path.splitext(self.second_title.split("/!/")[0])[1] in ['.jpg', '.png', '.jpeg'] else None
            if self.second_title_image:
                self.second_title_image_width = int(self.second_title.split("/!/")[1])
                self.second_title_image_height = int(self.second_title.split("/!/")[2])
                self.second_title_image = pygame.transform.scale(self.second_title_image, (self.second_title_image_width, self.second_title_image_height))

            self.categories_background = get_next_line(f).strip()
            self.categories_background_image = pygame.image.load(self.categories_background.split("/!/")[0]) if os.path.splitext(self.categories_background.split("/!/")[0])[1] in ['.jpg', '.png', '.jpeg'] else None
            if self.categories_background_image:
                self.categories_background_image_width = int(self.categories_background.split("/!/")[1])
                self.categories_background_image_height = int(self.categories_background.split("/!/")[2])
                self.categories_background_image = pygame.transform.scale(self.categories_background_image, (self.categories_background_image_width, self.categories_background_image_height))

            self.categories = []
            category = get_next_line(f).strip()
            while category:
                self.categories.append(category)
                category = get_next_line(f).strip()
            f.close()

        self.data = []
        with open(self.data_file, 'r') as f:
            for line in f:
                self.data.append(line.strip())
            f.close()

        self.reels = []
        for i, category in enumerate(self.categories):
            self.reels.append(reel(self.data, self.width // 2 + (300 * (i - len(self.categories) // 2)) + (150 if len(self.categories) % 2 == 0 else 0), 550, width=220, height=70, case_height=30, draw_border=False))

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_icon(pygame.image.load(self.icon))
        pygame.display.set_caption("Randomizer")
        self.title_font = pygame.font.Font("assets/fonts/TT Mussels Trial DemiBold.otf", 48)
        self.title_font.set_underline(True)
        self.font = pygame.font.SysFont('Arial', 28)
        self.small_font = pygame.font.SysFont('Arial', 16)
        self.running = True

        self.last_time = pygame.time.get_ticks()
        self.deltatime = 0

        self.loop()

    def loop(self):
        while self.running:
            current_time = pygame.time.get_ticks()
            self.deltatime = current_time - self.last_time
            self.last_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))
            self.draw()
            pygame.display.flip()

        pygame.quit()

    def draw(self):
        self.screen.fill((217, 217, 217))

        if not self.title_image:
            self.draw_text(self.title, 0, 250, self.title_font, ORANGE)
        else:
            self.draw_image(self.title_image, 0, 250, self.title_image_width, self.title_image_height)

        self.draw_button("Start", 0, 150, 100, 30, WHITE, LIGHT_GRAY, self.font, BLACK, self.start_spin, True, 2, LIGHT_GRAY)
        self.draw_text("-" * 150, 0, 100, self.font, BLACK)

        if not self.second_title_image:
            self.draw_text(self.second_title, 0, 25, self.title_font, ORANGE)
        else:
            self.draw_image(self.second_title_image, 0, 25, self.second_title_image_width, self.second_title_image_height)

        for i, category in enumerate(self.categories):
            self.draw_image(self.categories_background_image, 300 * (i - len(self.categories) // 2) + (150 if len(self.categories) % 2 == 0 else 0), -150, self.categories_background_image_width, self.categories_background_image_height)
            self.draw_text(category, (300 * (i - len(self.categories) // 2)) + (150 if len(self.categories) % 2 == 0 else 0), -100, self.font, BLACK)

        for reel in self.reels:
            reel.update(self.deltatime)
            reel.draw(self.screen)

        #pygame.draw.circle(self.screen, (255, 0, 0), (self.width // 2, self.height // 2), 2)

    def draw_text(self, text, x, y, font, color, x_align=0.5, y_align=0.5):
        x = self.width // 2 - (font.size(text)[0] * x_align) + x
        y = self.height // 2 - (font.size(text)[1] * y_align) - y
        self.screen.blit(font.render(text, True, color), (x, y))

    def draw_button(self, text, x, y, width, height, color, hover_color, font, text_color, action=None, draw_border=False, border_width=1, border_color=BLACK):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        mouse_x = mouse[0] - self.width // 2 + width // 2
        mouse_y = self.height // 2 - mouse[1] + height // 2

        if x < mouse_x < x + width and y < mouse_y < y + height:
            pygame.draw.rect(self.screen, hover_color, (x + self.width // 2 - width // 2, self.height // 2 - y - height // 2, width, height))
            if click[0] == 1 and action:
                action()
        else:
            pygame.draw.rect(self.screen, color, (x + self.width // 2 - width // 2, self.height // 2 - y - height // 2, width, height))

        if draw_border:
            pygame.draw.rect(self.screen, border_color, (x + self.width // 2 - width // 2 - border_width, self.height // 2 - y - height // 2 - border_width, width + 2 * border_width, height + 2 * border_width), border_width)

        self.draw_text(text, x, y, font, text_color, 0.5, 0.5)

    def draw_image(self, image, x, y, width, height):
        self.screen.blit(image, (self.width // 2 - width // 2 + x, self.height // 2 - height // 2 - y))

    def start_spin(self):
        for reel in self.reels:
            reel.start_spin()