import pygame.font

class Button():

    def __init__(self, screen):
        """Initialize button attributes."""
        self.screen = screen
        
        self.button_color = (0,0,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)
        
        self.prep('', (0,0))
        
    def prep(self, msg, position):
        """Turn msg into a rendered image at specified location."""
        self.image = self.font.render(msg, True, self.text_color, self.button_color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
    
    def draw(self):
        """Draw button on screen."""
        self.screen.blit(self.image, self.rect)
