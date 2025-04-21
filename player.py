import pygame

### Player Class ###


class Player:
    def __init__(self,screen,name,color, pos, size, eye_color, eyebrows, eyebrowsUpOrDown):
        self.screen = screen
        self.name = name
        self.pos = pos
        self.color = color
        self.size = size
        self.eye_color = eye_color
        self.eyebrows = eyebrows
        self.eyebrowsUpOrDown = eyebrowsUpOrDown
        self.left_eye = pygame.math.Vector2(pos.x - 5, pos.y - 5)
        self.right_eye = pygame.math.Vector2(pos.x + 5, pos.y - 5)
    def draw(self):
        left_eye = pygame.math.Vector2(self.pos.x - 5, self.pos.y - 5)
        right_eye = pygame.math.Vector2(self.pos.x + 5, self.pos.y - 5)
        pygame.draw.circle(self.screen, self.color, self.pos, self.size)
        pygame.draw.circle(self.screen, self.eye_color, left_eye, 3)
        pygame.draw.circle(self.screen, self.eye_color, right_eye, 3)
        if self.eyebrows == True:
            if self.eyebrowsUpOrDown == "up":
                pygame.draw.line(self.screen, "Black", (self.pos.x - 12, self.pos.y - 9), (self.pos.x - 2, self.pos.y - 15), width=3)
                pygame.draw.line(self.screen, "Black", (self.pos.x + 12, self.pos.y - 9), (self.pos.x + 2, self.pos.y - 15), width=3)
            elif self.eyebrowsUpOrDown == "down":
                pygame.draw.line(self.screen, "Black", (self.pos.x - 12, self.pos.y - 15), (self.pos.x - 2, self.pos.y - 9), width=3)
                pygame.draw.line(self.screen, "Black", (self.pos.x + 12, self.pos.y - 15), (self.pos.x + 2, self.pos.y - 9), width=3)


        