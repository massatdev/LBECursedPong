import math
import pygame
import random

class Paddle:
    def __init__(self, x, y, width, height, speed, color, screen_height):
        self.true_x = x
        self.true_y = y
        self.x = x
        self.y = y
        self.width = width
        self.true_width = width 
        self.height = height
        self.true_height = height
        self.speed = speed
        self.color = color
        self.screen_height = screen_height
        self.curse_counter = 0

    def update_curses(self, curse_manager):
        self.old_center_y = self.y + (self.height // 2)
        self.old_center_x = self.x + (self.width // 2)

        if curse_manager.has_curse("PALPITATIONS") and self.curse_counter < 60:
            self.height = max(self.true_height + random.randint(-20, 20), 10)
            self.width = max(self.true_width + random.randint(-5, 5), 10)
        else:
            self.height = self.true_height
            self.width = self.true_width
            self.curse_counter = 0

        self.curse_counter += 1

        self.y = self.old_center_y - (self.height // 2)
        self.x = self.old_center_x - (self.width // 2)

        self.y = max(0, min(self.y, self.screen_height - self.height))
        
    def handle_input(self, keys, curse_manager):
        up = -1
        down = 1

        if curse_manager.has_curse("INVERT_CONTROLS"):
            up = 1
            down = -1

        if curse_manager.has_curse("FATIGUE"):
            up *= 0.8
            down *= 0.8

        if curse_manager.has_curse("STROKE_L"):
            up *= random.uniform(0.01, 0.75)

        if curse_manager.has_curse("STROKE_R"):
            down *= random.uniform(0.01, 0.75)

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            up *= 2
            down *= 2

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y += self.speed * up
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed * down
        self.y = max(0, min(self.y, self.screen_height - self.height))

        if curse_manager.has_curse("SHAKY_HANDS"):
            self.angle = math.sin(pygame.time.get_ticks() * 0.01) * 10
            if self.curse_counter > 60:
                self.x = self.true_x
                self.y = self.true_y
                self.curse_counter = 0
            self.x += random.randint(-5, 5)
            self.y += random.randint(-5, 5)

            self.y = max(0, min(self.y, self.screen_height - self.height))
        else:
            self.angle = 0
        
    def draw(self, screen):
        self.real_width = max(1, int(self.width))
        self.real_height = max(1, int(self.height))

        surface = pygame.Surface((self.real_width, self.real_height), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.color, (0, 0, self.real_width, self.real_height))
        rotated_surface = pygame.transform.rotate(surface, self.angle)
        new_rect = rotated_surface.get_rect(center=(self.x + self.real_width // 2, self.y + self.real_height // 2))
        screen.blit(rotated_surface, new_rect.topleft)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)