import sys

import pygame

from player import Player 

def check_events(player, cards, supply_piles, done_rect, play_coins_rect):
    """Respond to mouse events."""
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    # Respond to mouse clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player.action_phase:
                if done_rect.collidepoint(mouse_pos):
                    player.action_phase = False
                    player.buy_phase = True
                else:
                    if player.num_actions > 0:
                        # Play actions
                        for card, card_rect in zip(
                        player.hand, player.hand_rects):
                            if card_rect.collidepoint(mouse_pos):
                                if card.type == 'Action':
                                    card.play_action(player)
            else:
                if done_rect.collidepoint(mouse_pos):
                    player.buy_phase = False
                    player.clean_up()
                else:
                    if player.num_buys > 0:
                        # Play all coins at once
                        if play_coins_rect.collidepoint(mouse_pos):
                            player.play_all_coins()
                            
                        # Play coins individually
                        for card, card_rect in zip(
                        player.hand, player.hand_rects):
                            if card_rect.collidepoint(mouse_pos):
                                if card.type == 'Treasure':
                                    player.play_coin(card)
                                    
                        # Buy cards
                        for card in cards:
                            if card.rect.collidepoint(mouse_pos):
                                player.buy_card(card, supply_piles)
                                
            # Print info after each click
            print_game_info(player, supply_piles)
        
def print_game_info(player, supply_piles):
    """Prints relevant game info for current player."""
    print("\n", player.name, "\n")
    print("Actions:", player.num_actions)
    print("Buys:", player.num_buys)
    print("$", player.num_coins, "\n")
    # Number of cards in deck should only be visible to player.
    print("Deck:", len(player.deck), "cards \n")
    for supply_pile in supply_piles:
        print(supply_pile,":", supply_piles[supply_pile])

    # ~ # Use to check that cards go where they need to
    # ~ print("hand:",player.hand)
    # ~ print("deck:",player.deck)
    # ~ print("discard pile:",player.discard_pile)
    # ~ print("played_cards:",player.played_cards)


def check_game_over(supply_piles):
    """Check for game over."""
    # Game ends when either the supply pile of province cards is empty or
    # any 3 supply piles are empty.
    
    # Needs a better way to keep track of empty piles
    # instead of reseting every check. 
    num_empty_piles = 0
    for pile in supply_piles.values():
        if pile == 0:
            num_empty_piles += 1
  
    if num_empty_piles >= 3 or supply_piles['Province'] == 0:
        game_over = True
    else:
        game_over = False
    
    return game_over


def determine_winner(players, player1, player2):
    """Determine winner at the end of the game."""
    # Improve so player1 and player2 not necessary as parameters
    for player in players:
        # Determines winner by counting victory points in each player's deck
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


def determine_winner(players):
    """Determine winner at the end of the game."""
    for player in players:
        # Counts victory points in each player's deck
        player.deck.extend(player.discard_pile + player.hand)
        player.hand = []
        player.discard_pile = []
        for card in player.deck:
            if card.type == 'Victory' or card.type == 'Curse':
                player.victory_points += card.point_value
        
        # Sorts players by most victory points and fewest turns
        def get_turns(player):
            return player.turn
        def get_victory_points(player):
            return player.victory_points
        players.sort(key=get_turns)
        players.sort(key=get_victory_points, reverse=True)
        
        # If multiple players share the highest score and fewest turns
        scores = list(player.victory_points for player in players)
        max_score = max(scores)
        count = scores.count(max_score)
        if count > 1:
            tied_players = players[0:count]
            turns = list(player.turn for player in tied_players)
            min_turns = min(turns)
            count = turns.count(min_turns)
            if count > 1:
                tied_players = tied_players[0:count]
        
        winner = players[0]
    
    if count > 1:
        # If tie
        print("Tie game", list(player.name for player in tied_players))
    else:
        # If single winner
        print(winner.name, "is the winner!")
        
    # Prints players and scores in order of victory
    for player in players:
        print(player.name, "has", player.victory_points, "victory points")


def blit_treasure_piles(screen, treasure_cards):
    """Draw treasure piles on screen."""
    y_location = 0
    for card in treasure_cards:
        card.rect.x = 0
        card.rect.y = y_location
        screen.blit(card.image, card.rect)
        y_location += card.rect.height
    
def blit_victory_piles(screen, victory_cards):
    """Draw victory piles on screen."""
    y_location = 0
    for card in victory_cards:
        card.rect.x = card.rect.width
        card.rect.y = y_location
        screen.blit(card.image, card.rect)
        y_location += card.rect.height

def blit_action_piles(screen, action_cards):
    """Draw action piles on screen."""
    y_location = 0
    for card in action_cards:
        card.rect.x = 2*card.rect.width
        card.rect.y = y_location
        screen.blit(card.image, card.rect)
        y_location += card.rect.height
        
def blit_hands(screen, players):
    """Draw player hands on screen."""
    for player in players:
        player.x = 600
        player.hand_rects = []
        for card in player.hand:
            hand_rect = card.image.get_rect()
            hand_rect.x = player.x
            hand_rect.y = player.y
            player.hand_rects.append(hand_rect)
            screen.blit(card.image, hand_rect)
            player.x += card.rect.width
                

def update_screen(screen, background_color, treasure_cards, victory_cards, action_cards, players, done_image, done_rect, play_coins_image, play_coins_rect):
    """Update images on the screen and flip to the new screen."""
    # Draws background, supply piles, hands, and buttons on screen
    screen.fill(background_color)
    blit_treasure_piles(screen, treasure_cards)
    blit_victory_piles(screen, victory_cards)
    blit_action_piles(screen, action_cards)
    blit_hands(screen, players)
    screen.blit(done_image, done_rect)
    screen.blit(play_coins_image, play_coins_rect)
    
    # Makes the most recently drawn screen visible
    pygame.display.flip()
