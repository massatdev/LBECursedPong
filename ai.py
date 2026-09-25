import pygame

class Paddle:
    def __init__(self, x, y, width, height, speed, color, screen_height, screen_width, difficulty):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed * difficulty
        self.color = color
        self.screen_height = screen_height
        self.screen_width = screen_width

    def update(self, ball_y, ball_x):
        paddle_center = self.y + self.height // 2

        if ball_x > self.screen_width // 2:
            if paddle_center < ball_y:
                self.y += self.speed
            elif paddle_center > ball_y:
                self.y -= self.speed

        self.y = max(0, min(self.y, self.screen_height - self.height))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)