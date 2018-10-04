import pygame

import game_functions as gf

# Very messy

def cellar(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button):
    player.plus_actions(1)
    print("Discard cards:")
    done = False
    num = 0
    while not done:
        if len(player.hand) == 0:
            done = True
        else:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if done_button.rect.collidepoint(mouse_pos):
                        done = True
                    else:
                       for card, card_rect in zip(player.hand, player.hand_rects):
                            if card_rect.collidepoint(mouse_pos):
                                player.discard_card(card)
                                num += 1
                                gf.update_screen(screen, background_color, cards, supply_piles, player, players, done_button, coins_button)
    player.draw(num)

def moat(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button):
    player.draw(2)
    
def village(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button):
    player.draw(1)
    player.plus_actions(1)
    
def workshop(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button):
    print("Gain a card costing up to $4:")
    done = False
    while not done:
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for card in cards:
                    if card.supply_rect.collidepoint(mouse_pos):
                        if card.cost <= 4 and supply_piles[card.name] != 0:
                            player.gain_card(card, supply_piles)
                            done = True
        gf.update_screen(screen, background_color, cards, supply_piles, player, players, done_button, coins_button)

def woodcutter(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button):
    player.plus_buys(1)
    player.plus_coins(2)

def smithy(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button):
    player.draw(3)

def remodel(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button):
    print("Trash a card:")
    done = False
    if len(player.hand) == 0:
        print("No cards to trash.")
        done = True
    while not done:
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for hand_card, hand_card_rect in zip(player.hand, player.hand_rects):
                    if hand_card_rect.collidepoint(mouse_pos):
                        player.trash_card(hand_card, trash_pile)
                        print("Gain a card:")
                        while not done:
                            # Get mouse position
                            mouse_pos = pygame.mouse.get_pos()
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    for card in cards:
                                        if card.supply_rect.collidepoint(mouse_pos):
                                            if card.cost <= hand_card.cost + 2 and supply_piles[card.name] != 0:
                                                player.gain_card(card, supply_piles)
                                                done = True
                                gf.update_screen(screen, background_color, cards, supply_piles, player, players, done_button, coins_button)
                                        
def militia(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button):
    player.plus_coins(2)
    
    # Resolve in turn order
    target_players = players[players.index(player)+1:] + players[0:players.index(player)]
    for player in target_players:
        gf.update_screen(screen, background_color, cards, supply_piles, player, players, done_button, coins_button)
        if 'Moat' in [card.name for card in player.hand]:
            print(player.name, "reveals a moat.")
        else:
            print(player.name, "discard down to 3 cards:")
            while len(player.hand) > 3:
                # Get mouse position
                mouse_pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for hand_card, hand_card_rect in zip(player.hand, player.hand_rects):
                            if hand_card_rect.collidepoint(mouse_pos):
                                player.discard_card(hand_card)
                                gf.update_screen(screen, background_color, cards, supply_piles, player, players, done_button, coins_button)
                                
                                  
def market(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button):
    player.draw(1)
    player.plus_actions(1)
    player.plus_buys(1)
    player.plus_coins(1) 
                                        
def mine(screen, background_color, cards, supply_piles, trash_pile, player, players, done_button, coins_button):
    if 'Treasure' not in [card.type for card in player.hand]:
        print("No treasure cards in hand.")
    else:
        print("Trash a card:")
        done = False
        while not done:
            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for hand_card, hand_card_rect in zip(player.hand, player.hand_rects):
                        if hand_card_rect.collidepoint(mouse_pos):
                            if hand_card.type == 'Treasure':
                                player.trash_card(hand_card, trash_pile)
                                print("Gain a card:")
                                gf.update_screen(screen, background_color, cards, supply_piles, player, players, done_button, coins_button)
                                while not done:
                                    # Get mouse position
                                    mouse_pos = pygame.mouse.get_pos()
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            for card in cards:
                                                if card.supply_rect.collidepoint(mouse_pos):
                                                    if card.type == 'Treasure' and card.cost <= hand_card.cost + 3 and supply_piles[card.name] != 0:
                                                        player.gain_card(card, supply_piles, True)
                                                        done = True
                gf.update_screen(screen, background_color, cards, supply_piles, player, players, done_button, coins_button)                                      
