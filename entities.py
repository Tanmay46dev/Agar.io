import pygame

# Entities
class Blob:
    def __init__(self, pos, radius, color):
        self.radius = radius
        self.color = color
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.center = pos

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.rect.center, self.radius)

    def is_colliding(self, obj):
        return self.rect.colliderect(obj.rect)

class Player(Blob):
    def __init__(self, pos, radius, color):
        super().__init__(pos, radius, color)
        self.move_speed = 5

    def move(self, dir, vertical=False):
        if vertical:
            self.rect.centery += dir * self.move_speed
        else:
            self.rect.centerx += dir * self.move_speed
