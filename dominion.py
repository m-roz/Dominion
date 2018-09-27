import pygame

import card
import game_functions as gf
from player import Player
from button import Button

pygame.init()

# Select number of players
num_players = 3


# Screen
screen_dimensions = (1920,1080)
screen = pygame.display.set_mode(screen_dimensions)
pygame.display.set_caption('Dominion')
screen_rect = screen.get_rect()
background_color = (255, 255, 255)

# Treasure cards
copper = card.TreasureCard('Copper', 0, 1)
silver = card.TreasureCard('Silver', 3, 2)
gold = card.TreasureCard('Gold', 6, 3)

# Number of cards in supply piles based on number of players
treasure_cards = [copper, silver, gold]
treasure_piles = {'Copper': (60-7*num_players), 'Silver': 40, 'Gold': 30}

# Victory cards
estate = card.VictoryCard('Estate', 2, 1)
duchy = card.VictoryCard('Duchy', 5, 3)
province = card.VictoryCard('Province', 8, 6)

# Curse card
# Group with victory cards
curse = card.CurseCard('Curse', 0, -1)    

victory_cards = [estate, duchy, province, curse]
victory_piles = {}
for victory_card in victory_cards:
    if num_players == 2:
        victory_piles[victory_card.name] = 8
    else:
        victory_piles[victory_card.name] = 12

victory_piles['Curse'] = 10*num_players - 10


# Action cards.
cellar = card.ActionCard('Cellar', 2)
moat = card.ActionCard('Moat', 2)
village = card.ActionCard('Village', 3)
workshop = card.ActionCard('Workshop', 3)
woodcutter = card.ActionCard('Woodcutter', 3)
smithy = card.ActionCard('Smithy', 4)
remodel = card.ActionCard('Remodel', 4)
militia = card.ActionCard('Militia', 4)
market = card.ActionCard('Market', 5)
mine = card.ActionCard('Mine', 5)

action_cards = [cellar, moat, village, workshop, woodcutter, 
    smithy, remodel, militia, market, mine]
action_piles = {}
for action_card in action_cards:
    action_piles[action_card.name] = 10

        
# All cards in game and corresponding supply piles
cards = treasure_cards + victory_cards + action_cards 
supply_piles = treasure_piles.copy()
supply_piles.update(victory_piles)
supply_piles.update(action_piles)

# Prepare supply piles to be blitted
gf.prep_supply_piles(treasure_cards, victory_cards, action_cards)

# Create players and set hand locations on screen
players = [] 
y = copper.supply_rect.height
for i in range(1, num_players+1):
    name = "Player " + str(i)
    player = Player(name)
    # Hand location on screen
    player.y = y
    players.append(player)
    y += 150

# Done button
done_button = Button(screen)

# Coins button
coins_button = Button(screen)

# Shuffle each player's starting deck and draw a hand of 5 cards
for player in players:
    player.deck = [copper]*7 + [estate]*3
    player.shuffle_deck()
    player.draw(5)
    
# Trash pile
trash_pile = []

game_over = False

# Main loop
while not game_over:
    for player in players:
        # Start turn
        player.turn += 1
        print("\n", player.name, "Turn", player.turn, "\n")

        # Begin the buy phase
        player.action_phase = True
        player.buy_phase = False
        
        while player.buy_phase or player.action_phase:
            if player.action_phase:
                # Skip action phase if no action cards in hand 
                # or no action points
                if player.hand[0].type != 'Action' or player.num_actions == 0:
                    player.action_phase = False
                    player.buy_phase = True
            if player.buy_phase:
                # Skip buy phase if no buy points
                if player.num_buys == 0:
                    player.buy_phase = False
                    player.clean_up()
            
            # Run event loop and check for mouse events
            gf.check_events(screen, background_color, coins_button, done_button, cards, supply_piles, trash_pile, player, players)
            
            # Update buttons
            gf.prep_buttons(player, coins_button, done_button)
            
            # Draw new screen
            gf.update_screen(screen, background_color, cards, supply_piles, player, players, done_button, coins_button)
                    

        # Check for game over at the end of each turn
        game_over = gf.check_game_over(supply_piles)
        if game_over:
            break

# When game over
print("Game Over")
gf.determine_winner(players)
