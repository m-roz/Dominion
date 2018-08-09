# Dominion
Dominion prototype using pygame.
Currently plays a game with 2 players sharing the same screen with both hands always visible.
Each player shares the same '+$' and 'Done' buttons.
Click the 'Done' button to end the action phase and start the buy phase or end the buy phase and turn for the current player.

Uses the starting "first game" kingdom cards from dominion rulebook. All card images drawn on screen but currently only village, woodcutter, smithy, and market work.
All information regarding the active player and supply piles is printed to the console after every click. 

Should be able to finish a game with just the 4 working action cards.

Changelog:
Commit 1
-Basic two player game of dominion with village, woodcutter, smithy, and market action cards working.

Commit 2
-Fixed screen updating of player hand after a card is played.
-Only current player's hand visible on screen.

Commit 3
-Automatic phase and turn end without 'Done' button being pressed.

Commit 4
-Added '+$' button to play all coins in player's hand at once.
-Screen is updated continuously at the end of every loop instead of after the mouse is clicked.

Commit 5
-Refactored code
-Added game_functions.py module
-Both players' hands always visible on screen
