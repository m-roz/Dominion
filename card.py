import pygame

class Card():
    def __init__(self, name, cost):
        """Initialize card attributes."""
        self.name = name
        self.cost = cost
        self.image = pygame.image.load("Images/" + self.name + ".jpg")
        self.rect = self.image.get_rect()
        self.supply_rect = self.image.get_rect()
        
class TreasureCard(Card):
    def __init__(self, name, cost, value):
        super().__init__(name, cost)
        self.type = 'Treasure'
        self.value = value

class VictoryCard(Card):
    def __init__(self, name, cost, point_value):
        super().__init__(name, cost,)
        self.type = 'Victory'
        self.point_value = point_value

class CurseCard(VictoryCard):
    def __init__(self, name, cost, point_value):
        super().__init__(name, cost, point_value)
        self.type = 'Curse'

class ActionCard(Card):
    def __init__(self, name, cost):
        super().__init__(name, cost)
        self.type = 'Action'
