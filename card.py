import player

class Card():
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        
class TreasureCard(Card):
    def __init__(self, name, cost, value):
        super().__init__(name, cost)
        self.type = 'Treasure'
        self.value = value


class VictoryCard(Card):
    def __init__(self, name, cost, point_value):
        super().__init__(name, cost)
        self.type = 'Victory'
        self.point_value = point_value


# Even though technically a curse type, might be unnecessary to create a 
# seperate class. Curse can just be its own instance of a VictoryCard?
class CurseCard(VictoryCard):
    def __init__(self, name, cost, point_value):
        super().__init__(name, cost, point_value)
        self.type = 'Curse'


# Create increase actions, increase coins, and increase buys classes so 
# printing is automatically done when the actions are played?
class ActionCard(Card):
    def __init__(self, name, cost):
        super().__init__(name, cost)
        self.type = 'Action'
    
    def play_action(self, player):
        print(player.name, "plays", self.name)
        player.num_actions -= 1
        if self.name == 'Village':
            player.draw(1)
            player.num_actions += 1
            print("+1 Actions")
        elif self.name == 'Woodcutter':
            player.num_buys +=1
            player.num_coins += 2  
            print("+1 Buys")
            print("+$2")
        elif self.name == 'Smithy':
            player.draw(3)
        elif self.name == 'Market':
            player.draw(1)
            player.num_actions += 1
            player.num_buys += 1
            player.num_coins += 1
            print("+1 Actions")
            print("+1 Buys")
            print("+$1")
        else:
            print(self.name)




# Dedicated functions for each card vs everything written in ActionCard class?

# ~ # First game kingdom cards:
# ~ def cellar():
    # ~ player.num_actions += 1
    # ~ # Discard x cards and draw x cards
    
# ~ def moat(): # Action-Reaction
    # ~ player.draw(2)
    # ~ # When attacked, you may reveal from hand. Unaffected by attack.
    
# ~ def village(player):
    # ~ player.draw(1)
    # ~ player.num_actions += 1

# ~ def workshop():
    # ~ # Gain a card costing up to $4
    
# ~ def woodcutter(player):
    # ~ player.num_buys +=1
    # ~ player.num_coins += 2

# ~ def smithy(player):
    # ~ player.draw(3)
    
# ~ def remodel():
    # ~ # Trash a card from your hand. Gain a card costing up to $2 more than trashed card.
    
# ~ def militia(): #Action-Attack
    # ~ player.num_coin += 2
    # ~ # Each other player discards down to 3 cards in their hand.
    
# ~ def market(player):
    # ~ player.draw(1)
    # ~ player.num_actions += 1
    # ~ player.num_buy += 1
    # ~ player.num_coin += 1
    
# ~ def mine():
    # ~ # Trash a treasure from your hand. Gain a treasure costing up to $3 more than trashed card. Put card in hand.
