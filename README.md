# Dominion
Dominion prototype using pygame.
Currently plays a game with 2 players sharing the same screen with both hands always visible. (As of second commit, only active player's hand is visible after mouse click. )
Each player shares the same 'Done' button.
Click the button to end the action phase and start the buy phase or end the buy phase and turn for the current player.
Uses the starting "first game" kingdom cards from dominion rulebook. All card images drawn on screen but currently only village, woodcutter, smithy, and market work.
All information regarding the active player and supply piles printed to console after every click. 

Should be able to finish a game with just the 4 working action cards.



-Main bug is that cards are not properly removed from hand when played.
A new card is drawn to the screen each time but does not appear in the player's actual card list.
FIXED in second commit by creating dedicated function to re-fill and re-draw screen after every click.
