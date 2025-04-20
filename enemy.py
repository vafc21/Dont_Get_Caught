import pygame
import math

def group(shapes):
    shapess = []
    return shapess


class Enemy:
    def __init__(self, screen, name, pos, color, size, eye_color):
        self.screen = screen
        self.name = name
        self.pos = pos
        self.color = color
        self.size = size
        self.eye_color = eye_color
        self.left_eye = pygame.math.Vector2(pos.x - 5, pos.y - 5)
        self.right_eye = pygame.math.Vector2(pos.x + 5, pos.y - 5)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.size)
        pygame.draw.circle(self.screen, self.eye_color, self.left_eye, 3)
        pygame.draw.circle(self.screen, self.eye_color, self.right_eye, 3)
        pygame.draw.line(self.screen, "Black", (self.pos.x - 12, self.pos.y - 15), (self.pos.x - 2, self.pos.y - 9), width=3)
        pygame.draw.line(self.screen, "Black", (self.pos.x + 12, self.pos.y - 15), (self.pos.x + 2, self.pos.y - 9), width=3)

    def move_towards_target(self, target_pos, speed=2):
        direction = target_pos - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
        self.pos += direction * speed
        self.left_eye = pygame.math.Vector2(self.pos.x - 5, self.pos.y - 5)
        self.right_eye = pygame.math.Vector2(self.pos.x + 5, self.pos.y - 5)
        direction = target_pos - self.pos
        if direction.length() > 0:
            angle = math.degrees(math.atan2(-direction.y, direction.x))
            
            pygame.draw.arc(self.screen, "Black", (self.pos.x - 20, self.pos.y - 20, 40, 40), math.radians(angle - 65), math.radians(angle + 65), width=3)
        

    def draw_arc_towards_target(self, target_pos):
        direction = target_pos - self.pos
        if direction.length() > 0:
            angle = math.degrees(math.atan2(-direction.y, direction.x))
            
            pygame.draw.arc(self.screen, "Black", (self.pos.x - 20, self.pos.y - 20, 40, 40), math.radians(angle - 65), math.radians(angle + 65), width=3)
        
