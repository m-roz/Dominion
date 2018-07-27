import sys

import pygame

from player import Player
import card


pygame.init()

# Draw Screen
screen_dimensions = (1920,1080)
screen = pygame.display.set_mode(screen_dimensions)

pygame.display.set_caption('Dominion')

screen_rect = screen.get_rect()

background_color = (255, 255, 255)
screen.fill(background_color)

# All treasure cards.
copper = card.TreasureCard('Copper', 0, 1)
silver = card.TreasureCard('Silver', 3, 2)
gold = card.TreasureCard('Gold', 6, 3)

treasure_piles = {'Copper': 46, 'Silver': 40, 'Gold': 30}

# Draw treasure piles on screen.
copper_image = pygame.image.load("Images/Copper.jpg")
copper_rect = copper_image.get_rect()
copper_rect.left= screen_rect.left
copper_rect.top = screen_rect.top
screen.blit(copper_image, copper_rect)

silver_image = pygame.image.load("Images/Silver.jpg")
silver_rect = copper_image.get_rect()
silver_rect.left= screen_rect.left
silver_rect.top = copper_rect.bottom
screen.blit(silver_image, silver_rect)

gold_image = pygame.image.load("Images/Gold.jpg")
gold_rect = gold_image.get_rect()
gold_rect.left= screen_rect.left
gold_rect.top = silver_rect.bottom
screen.blit(gold_image, gold_rect)

# All victory cards.
estate = card.VictoryCard('Estate', 2, 1)
duchy = card.VictoryCard('Duchy', 5, 3)
province = card.VictoryCard('Province', 8, 6)

# Draw victory piles on screen.
estate_image = pygame.image.load("Images/Estate.jpg")
estate_rect = estate_image.get_rect()
estate_rect.left = copper_rect.right
estate_rect.top = screen_rect.top
screen.blit(estate_image, estate_rect)

duchy_image = pygame.image.load("Images/Duchy.jpg")
duchy_rect = duchy_image.get_rect()
duchy_rect.left= estate_rect.left 
duchy_rect.top = estate_rect.bottom
screen.blit(duchy_image, duchy_rect)

province_image = pygame.image.load("Images/Province.jpg")
province_rect = province_image.get_rect()
province_rect.left = estate_rect.left 
province_rect.top = duchy_rect.bottom
screen.blit(province_image, province_rect)

# Curse card.
curse = card.CurseCard('Curse', 0, -1)    

victory_piles = {'Estate': 8, 'Duchy': 8, 'Province': 8, 'Curse': 10}

# Draw curse pile on screen.
curse_image = pygame.image.load("Images/Curse.jpg")
curse_rect = curse_image.get_rect()
curse_rect.left = estate_rect.left 
curse_rect.top = province_rect.bottom
screen.blit(curse_image, curse_rect)

village = card.ActionCard('Village', 3)
woodcutter = card.ActionCard('Woodcutter', 3)
smithy = card.ActionCard('Smithy', 4)
market = card.ActionCard('Market', 5)

action_piles = {'Village': 1, 'Woodcutter': 1, 'Smithy': 1, 'Market': 8}

# Draw kingdom piles on screen.
cellar_image = pygame.image.load("Images/Cellar.jpg")
cellar_rect = cellar_image.get_rect()
cellar_rect.left = estate_rect.right
cellar_rect.top = screen_rect.top
screen.blit(cellar_image, cellar_rect)

moat_image = pygame.image.load("Images/Moat.jpg")
moat_rect = moat_image.get_rect()
moat_rect.left= estate_rect.right 
moat_rect.top = cellar_rect.bottom
screen.blit(moat_image, moat_rect)

village_image = pygame.image.load("Images/Village.jpg")
village_rect = village_image.get_rect()
village_rect.left = estate_rect.right 
village_rect.top = moat_rect.bottom
screen.blit(village_image, village_rect)

workshop_image = pygame.image.load("Images/Workshop.jpg")
workshop_rect = workshop_image.get_rect()
workshop_rect.left = estate_rect.right 
workshop_rect.top = village_rect.bottom
screen.blit(workshop_image, workshop_rect)

woodcutter_image = pygame.image.load("Images/Woodcutter.jpg")
woodcutter_rect = woodcutter_image.get_rect()
woodcutter_rect.left = estate_rect.right 
woodcutter_rect.top = workshop_rect.bottom
screen.blit(woodcutter_image, woodcutter_rect)

smithy_image = pygame.image.load("Images/Smithy.jpg")
smithy_rect = smithy_image.get_rect()
smithy_rect.left = estate_rect.right 
smithy_rect.top = woodcutter_rect.bottom
screen.blit(smithy_image, smithy_rect)

remodel_image = pygame.image.load("Images/Remodel.jpg")
remodel_rect = remodel_image.get_rect()
remodel_rect.left = estate_rect.right 
remodel_rect.top = smithy_rect.bottom
screen.blit(remodel_image, remodel_rect)

militia_image = pygame.image.load("Images/Militia.jpg")
militia_rect = militia_image.get_rect()
militia_rect.left = estate_rect.right 
militia_rect.top = remodel_rect.bottom
screen.blit(militia_image, militia_rect)

market_image = pygame.image.load("Images/Market.jpg")
market_rect = market_image.get_rect()
market_rect.left = estate_rect.right 
market_rect.top = militia_rect.bottom
screen.blit(market_image, market_rect)

mine_image = pygame.image.load("Images/Mine.jpg")
mine_rect = mine_image.get_rect()
mine_rect.left = estate_rect.right 
mine_rect.top = market_rect.bottom
screen.blit(mine_image, mine_rect)

# Draw Done button.
x_coordinate = 1300
y_coordinate = duchy_rect.bottom
msg = "Done"
msg_color = (255, 255, 255)
bg_color = (0, 0, 0)
f = pygame.font.SysFont(None, 48)
done_image = f.render(msg, True, msg_color, bg_color)
done_box_rect = done_image.get_rect()
done_box_rect.topleft = (x_coordinate,y_coordinate)
screen.blit(done_image, done_box_rect)


# Create players.
player1 = Player('Player1')
player2 = Player('Player2')
players = [player1, player2]

# Shuffle each player's starting deck and draw a new hand of 5 cards.
for player in players:
    player.deck = [copper]*7 + [estate]*3
    player.shuffle_deck()
    player.draw(5)
    
# Trash pile.
trash_pile = []

game_over = False

# Player hand y-coordinates.
player1.y = silver_rect.top
player2.y = curse_rect.top

def print_game_info():
    """Prints relevant game info for current player."""
        print("\n", player.name, "\n")
        print("Actions:", player.num_actions)
        print("Buys:", player.num_buys)
        print("$:", player.num_coins, "\n")
        
        for pile,num in list(
        treasure_piles.items()) + list(
        victory_piles.items()) + list(
        action_piles.items()):
            print(pile,":", num)
        
def draw_hand(player):
        """Draw player hand on screen."""
        # Probably has to be redone. 
        hand_images = []
        hand_rects = []
        for card in player.hand:
            hand_images.append(
            pygame.image.load("Images/" + card.name + ".jpg"))
        for image in hand_images:
            hand_rects.append(image.get_rect())

        player.x = 600
        for image, rect in zip(hand_images, hand_rects):
            rect.left = player.x
            rect.top = player.y
            screen.blit(image,rect)
            player.x += rect.width
        
        return hand_rects
        
for player in players:
    draw_hand(player)

# Main loop.
while not game_over:
    for player in players:
        hand_rects = draw_hand(player)
        pygame.display.flip()
        # Start turn.
        player.turn += 1
        print("\n", player.name, "\n")

        # Begin the buy phase.
        action_phase = True
        buy_phase = False
        
        while buy_phase or action_phase:
            # Get mouse position.
            mouse_pos = pygame.mouse.get_pos()
            # Respond to mouse clicks.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if action_phase:
                        if done_box_rect.collidepoint(mouse_pos):
                            action_phase = False
                            buy_phase = True
                        else:
                            if player.num_actions > 0:
                                # Play actions.
                                for card, card_rect in zip(
                                player.hand, hand_rects):
                                    if card_rect.collidepoint(mouse_pos):
                                        if card.type == 'Action':
                                            card.play_action(player)
                                            player.hand.remove(card)
                                            player.played_cards.append(card)
                                            card.play_action(player)
                    else:
                        if done_box_rect.collidepoint(mouse_pos):
                            buy_phase = False
                            player.clean_up()
                            draw_hand(player)
                        else:
                            if player.num_buys > 0:
                                # Play coins.
                                for card, card_rect in zip(
                                player.hand, hand_rects):
                                    if card_rect.collidepoint(mouse_pos):
                                        if card.type == 'Treasure':
                                            player.num_coins += card.value
                                            player.hand.remove(card)
                                            player.played_cards.append(card)
                                # If player buys a card.
                                # Could be done better.
                                if copper_rect.collidepoint(mouse_pos):
                                    player.buy_card(copper, treasure_piles)
                                elif silver_rect.collidepoint(mouse_pos):
                                    player.buy_card(silver, treasure_piles)
                                elif gold_rect.collidepoint(mouse_pos):
                                    player.buy_card(gold, treasure_piles)
                                elif estate_rect.collidepoint(mouse_pos):
                                    player.buy_card(estate, victory_piles)
                                elif duchy_rect.collidepoint(mouse_pos):
                                    player.buy_card(duchy, victory_piles)
                                elif province_rect.collidepoint(mouse_pos):
                                    player.buy_card(province, victory_piles)
                                elif curse_rect.collidepoint(mouse_pos):
                                    player.buy_card(curse, victory_piles)
                                elif village_rect.collidepoint(mouse_pos):
                                    player.buy_card(village, action_piles)
                                elif woodcutter_rect.collidepoint(mouse_pos):
                                    player.buy_card(woodcutter, action_piles)
                                elif smithy_rect.collidepoint(mouse_pos):
                                    player.buy_card(smithy, action_piles)
                                elif market_rect.collidepoint(mouse_pos):
                                    player.buy_card(market, action_piles)
                                    
                    hand_rects = draw_hand(player)            
                    pygame.display.flip()
                    print_game_info()
                    
        # Check for game over.
        # Needs a better way to keep track of empty piles
        # instead of reseting every check.
        num_empty_piles = 0
        for pile in action_piles.values():
            if pile == 0:
                num_empty_piles += 1
                
        if num_empty_piles >= 3 or victory_piles['Province'] == 0:
            game_over = True
            break


print("Game Over")

# Determine winner
for player in players:
    # Determines winner by counting victory points in each player's deck.
    player.deck.extend(player.hand + player.discard_pile)
    player.hand = []
    player.discard_pile = []
    for card in player.deck:
        if card.type == 'Victory' or card.type == 'Curse':
            player.victory_points += card.point_value
    print(player.name, " has", player.victory_points, "points.")

if player1.victory_points == player2.victory_points:
    # In the event of a tie, player who took fewest turns wins.
    if player1.turn < player2.turn:
        print(player1.name, "is the winner!")
    elif player1.turn > player2.turn:
        print(player2.name, "is the winner!")
    else:
        print("Tie game!")
elif player1.victory_points > player2.victory_points:
    print(player1.name, "is the winner!")
elif player1.victory_points < player2.victory_points:
    print(player2.name, "is the winner!")
