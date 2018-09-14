import pygame

from player import Player
from button import Button
import card
import game_functions as gf

pygame.init()

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
treasure_piles = {'Copper': 46, 'Silver': 40, 'Gold': 30}

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
    victory_piles[victory_card.name] = 8
victory_piles['Curse'] = 10


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


# Done button
done_button = Button("Done", screen, (1300,160))

# Coins button
coins_button = Button("+$", screen, (1200,160))

# Create players
player1 = Player('Player1')
player2 = Player('Player2')
players = [player1, player2]

# Shuffle each player's starting deck and draw a hand of 5 cards
for player in players:
    player.deck = [copper]*7 + [estate]*3
    player.shuffle_deck()
    player.draw(5)
    
# Trash pile
# Players should be able to look in trash pile
trash_pile = []

game_over = False

player1.y = copper.rect.height
player2.y = 3*copper.rect.height

# Main loop
while not game_over:
    for player in players:
        gf.update_screen(screen, background_color, treasure_cards, 
                        victory_cards, action_cards, supply_piles, players, done_button, coins_button)
                        
        # Start turn
        player.turn += 1
        print("\n", player.name, "Turn", player.turn, "\n")

        # Begin the buy phase
        player.action_phase = True
        player.buy_phase = False
        current_phase = "Action Phase"
        
        while player.buy_phase or player.action_phase:
            if player.action_phase:
                # Skips action phase if no action cards in hand 
                # or no action points
                if player.hand[0].type != 'Action' or player.num_actions == 0:
                    player.action_phase = False
                    player.buy_phase = True
                    current_phase = "Buy Phase"
            if player.buy_phase:
                # Skips buy phase if no buy points
                if player.num_buys == 0:
                    player.buy_phase = False
                    player.clean_up()
            
            # Run event loop and check for mouse events
            gf.check_events(player, cards, supply_piles,
                done_button, coins_button)
            
            # Update coins button 
            coins_button.prep_msg("+$"+ str(player.get_num_coins_in_hand()))
            
            gf.update_screen(screen, background_color, treasure_cards,
                            victory_cards, action_cards, supply_piles, players, done_button, coins_button)
                    

        # Check for game over.
        game_over = gf.check_game_over(supply_piles)
        if game_over:
            break

print("Game Over")
gf.determine_winner(players)
