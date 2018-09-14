import pygame.font

class Button():

    def __init__(self, msg, screen, position):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        self.x, self.y = position
        
        self.button_color = (0,0,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)
        
        self.prep_msg(msg)
        
    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.image = self.font.render(msg, True, self.text_color,
            self.button_color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw_button(self):
        """Draw button on screen."""
        self.screen.blit(self.image, self.rect)
