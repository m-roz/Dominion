import sys
import pygame

import actions

def check_events(screen, background_color, coins_button, done_button, cards, 
        supply_piles, trash_pile, player, players):
    """Respond to mouse events."""
    
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    # Respond to mouse clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player.action_phase:
                if done_button.rect.collidepoint(mouse_pos):
                    player.action_phase = False
                    player.buy_phase = True
                else:
                    if player.num_actions > 0:
                        # Play actions
                        for card, card_rect in zip(
                        player.hand, player.hand_rects):
                            if card_rect.collidepoint(mouse_pos):
                                if card.type == 'Action':
                                    player.play_action(card)
                                    update_screen(screen, background_color, cards, supply_piles, player, players, done_button, coins_button)
                                    
                                    # Messy
                                    if card.name == 'Cellar':
                                        actions.cellar(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button)
                                    elif card.name == 'Moat':
                                        actions.moat(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button)
                                    elif card.name == 'Village':
                                        actions.village(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button)
                                    elif card.name == 'Workshop':
                                        actions.workshop(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button)
                                    elif card.name == 'Woodcutter':
                                        actions.woodcutter(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button)
                                    elif card.name == 'Smithy':
                                        actions.smithy(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button)
                                    elif card.name == 'Remodel':
                                        actions.remodel(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button)
                                    elif card.name == 'Militia':
                                       actions.militia(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button)
                                    elif card.name == 'Market':
                                        actions.market(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button)
                                    elif card.name == 'Mine':
                                        actions.mine(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button)
            else:
                if done_button.rect.collidepoint(mouse_pos):
                    player.buy_phase = False
                    player.clean_up()
                else:
                    if player.num_buys > 0:
                        # Play all coins at once
                        if coins_button.rect.collidepoint(mouse_pos):
                            player.play_all_coins()
                            
                        # Play coins individually
                        for card, card_rect in zip(
                        player.hand, player.hand_rects):
                            if card_rect.collidepoint(mouse_pos):
                                if card.type == 'Treasure':
                                    player.play_coin(card)
                                    
                        # Buy cards
                        for card in cards:
                            if card.supply_rect.collidepoint(mouse_pos):
                                player.buy_card(card, supply_piles)

def prep_buttons(player, coins_button, done_button):
    """Updates coins and done buttons."""
    # Update coins button 
    coins_button.prep("+$"+ str(player.get_num_coins_in_hand()), 
        (1200, player.y + 90))
    # Update done button location
    done_button.prep("Done", (1300, player.y + 90))

def prep_supply_piles(treasure_cards, victory_cards, action_cards):
    """Prepare supply pile rects to be blitted. Only done once at the start."""   
    # Treasure piles
    y_location = 0
    for card in treasure_cards:
        card.supply_rect.x = 0
        card.supply_rect.y = y_location
        y_location += card.supply_rect.height + 24
     
    # Victory piles
    y_location = 0
    for card in victory_cards:
        card.supply_rect.x = card.supply_rect.width + 20
        card.supply_rect.y = y_location
        y_location += card.supply_rect.height + 24
       
    # Action piles
    y_location = 0 
    for card in action_cards:
        card.supply_rect.x = 2*card.supply_rect.width + 40
        card.supply_rect.y = y_location
        y_location += card.supply_rect.height + 24

    

def blit_supply_piles(screen, cards, supply_piles):
    """Draw supply piles with names, costs, and quantities on screen."""
    
    font = pygame.font.SysFont(None, 24)
    text_color = (0, 0, 0)
    
    for card in cards:
        screen.blit(card.image, card.supply_rect)
        
        name_str = card.name
        cost_str = " $" + str(card.cost)
        quantity_str = " (" + str(supply_piles[name_str]) + ")"
        info_str = name_str + cost_str + quantity_str
        
        name_image = font.render(info_str, True, text_color)
        name_rect = name_image.get_rect()
        name_rect.center = card.supply_rect.center
        name_rect.top = card.supply_rect.bottom + 2
        screen.blit(name_image, name_rect)
    
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

def blit_turn_info(screen, player):
    """Draw turn info for current player on screen."""
    font = pygame.font.SysFont(None, 24)
    text_color = (0, 0, 0)
    
    name_str = player.name
    # -> indicates current phase
    if player.action_phase:
        num_actions_str = "->Actions: " + str(player.num_actions)
    else:
        num_actions_str = "  Actions: " + str(player.num_actions)
    if player.buy_phase:
        num_buys_str = "->Buys: " + str(player.num_buys)
    else:
        num_buys_str = "  Buys: " + str(player.num_buys)
    num_coins_str = "  To Spend: $" + str(player.num_coins)
    
    name_image = font.render(name_str, True, text_color)
    name_rect = name_image.get_rect()
    name_rect.x = 450
    name_rect.y = player.y
    num_actions_image = font.render(num_actions_str, True, text_color)
    num_actions_rect = num_actions_image.get_rect()
    num_actions_rect.x = 450
    num_actions_rect.y = name_rect.bottom
    num_buys_image = font.render(num_buys_str, True, text_color)
    num_buys_rect = num_buys_image.get_rect()
    num_buys_rect.x = 450
    num_buys_rect.y = num_actions_rect.bottom
    num_coins_image = font.render(num_coins_str, True, text_color)
    num_coins_rect = num_coins_image.get_rect()
    num_coins_rect.x = 450
    num_coins_rect.y = num_buys_rect.bottom
    
    screen.blit(name_image, name_rect)
    screen.blit(num_actions_image, num_actions_rect)
    screen.blit(num_buys_image, num_buys_rect)
    screen.blit(num_coins_image, num_coins_rect)
    
    

def update_screen(screen, background_color, cards, supply_piles, 
        player, players, done_button, coins_button):
    """Update images on the screen and flip to the new screen."""
    # Draws background, supply piles, hands, and buttons on screen
    screen.fill(background_color)
    blit_supply_piles(screen, cards, supply_piles)
    blit_hands(screen, players)
    done_button.draw()
    coins_button.draw()
    blit_turn_info(screen, player)
    # Makes the most recently drawn screen visible
    pygame.display.flip()

def check_game_over(supply_piles):
    """Check for game over."""
    # Game ends when either the supply pile of province cards is empty or
    # any other 3 supply piles are empty
    
    num_empty_piles = len([i for i in supply_piles.values() if i == 0])

    if num_empty_piles >= 3 or supply_piles['Province'] == 0:
        game_over = True
    else:
        game_over = False
    
    return game_over

def determine_winner(players):
    """Determine winner at the end of the game and prints results."""
    for player in players:
        # Counts victory points in each player's deck
        player.deck.extend(player.discard_pile + player.hand)
        player.hand = []
        player.discard_pile = []
        for card in player.deck:
            if card.type == 'Victory' or card.type == 'Curse':
                player.victory_points += card.point_value
        
        # Sort players by most victory points and fewest turns
        def get_turns(player):
            return player.turn
        def get_victory_points(player):
            return player.victory_points
        players.sort(key=get_turns)
        players.sort(key=get_victory_points, reverse=True)
        
        # If multiple players share the highest score and
        # took the same number of turns
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
