import random

class Player():
    def __init__(self, name):
        """ Initialize player attributes."""
        self.name = name
        self.deck = []
        self.hand = []
        self.hand_rects = []
        self.discard_pile = []
        self.played_cards = []
        self.num_actions = 1
        self.num_buys = 1
        self.num_coins = 0
        self.victory_points = 0
        self.turn = 0
        self.action_phase = False
        self.buy_phase = False
        self.y = 0
        
    def shuffle_deck(self):
        """Shuffle deck."""
        self.deck.extend(self.discard_pile)
        self.discard_pile = []
        random.shuffle(self.deck)
        print(self.name, "shuffles.")

    def draw(self,num):
        """Draw a new card from the top of the deck."""
        for i in range(num):
            # Shuffle discard pile into deck if deck is empty
            if not self.deck:
                # If player does not have enough cards left to draw
                # after forming a new deck, draw as many as he can
                if self.discard_pile:
                    self.shuffle_deck()
                else:
                    print("No more cards to draw.")
                    break
            new_card = self.deck.pop()
            self.hand.append(new_card)
            print(self.name, "draws a", new_card.name)
            self.sort_hand()
            
    def sort_hand(self):
        """Sort hand by type and cost."""
        # Order: Action cards, treasure cards, victory cards - in descending cost
        def get_cost(card):
            return card.cost
        
        def get_type(card):
            return card.type
            
        self.hand.sort(key=get_cost, reverse=True)    
        self.hand.sort(key=get_type)
        
    def clean_up(self):
        """Perform clean up phase at the end of turn. 
        Player places all cards played during turn and 
        all remaining cards in hand into discard pile. 
        Then draws a new hand of 5 cards and ends his turn."""
        self.discard_pile.extend(self.played_cards + self.hand)
        self.played_cards = []
        self.hand = []
        self.draw(5)
        self.num_actions = 1
        self.num_buys = 1
        self.num_coins = 0

    def buy_card(self, card, supply_piles):
        """Buy a card from a non-empty supply pile."""
        if supply_piles[card.name] > 0:
            if self.num_coins >= card.cost:
                self.num_buys -= 1
                self.num_coins -= card.cost
                self.discard_pile.append(card)
                supply_piles[card.name] -= 1
                print(self.name, "buys a", card.name)
        else:
            print("No more", card.name, "cards.")

    def gain_card(self, card, supply_piles, in_hand = False):
        """Gain a card from a non-empty supply pile. If in_hand set to True, 
        card goes to player's hand, otherwise it goes into discard pile."""
        if supply_piles[card.name] > 0:
            if in_hand:
                self.hand.append(card)
                self.sort_hand()
            else:
                self.discard_pile.append(card)
            supply_piles[card.name] -= 1
            print(self.name, "gains a", card.name)
        else:
            print("No more", card.name, "cards.")
    
    def discard_card(self, card):
        """Discard a card from hand."""
        self.hand.remove(card)
        self.discard_pile.append(card)
        print(self.name, "discards a", card.name)

    def trash_card(self,card, trash_pile):
        """Trash a card from hand."""
        self.hand.remove(card)
        trash_pile.append(card)
        print(self.name, "trashes a", card.name)

    def get_num_coins_in_hand(self):
        """Gets the value of the unplayed coins in hand
         to be displayed on button."""
        coins_in_hand = 0
        for card in self.hand:
            if card.type == 'Treasure':
                coins_in_hand += card.value
        return coins_in_hand
        
    def play_coin(self, card):
        """Play coin from hand."""
        self.num_coins += card.value
        self.hand.remove(card)
        self.played_cards.append(card)
        print(self.name, "plays a", card.name)
        
    def play_all_coins(self):
        """Plays every coin in hand at once when button is pressed."""
        for card in self.hand[:]:
            if card.type == 'Treasure':
                self.play_coin(card)

    def plus_actions(self, num):
        """Increases number of actions player has for current turn."""
        self.num_actions += num
        print("+" + str(num) + " Actions")
            
    def plus_buys(self, num):
        """Increases number of buys player has for current turn."""
        self.num_buys += num
        print("+" + str(num) + " Buys")
        
    def plus_coins(self, num):
        """Increases number of coins player has for current turn."""
        self.num_coins += num
        print("+$" + str(num))

    def play_action(self, card):
        """Plays an action card."""
        print(self.name, "plays a", card.name)
        self.num_actions -= 1
        self.hand.remove(card)
        self.played_cards.append(card)
