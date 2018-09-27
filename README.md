# Dominion
Dominion prototype using pygame.
Currently plays a game with 2-4 players sharing the same screen with each player's hand always visible.
Uses the starting "first game" kingdom cards from dominion rulebook.
All card images taken from isotropic dominion.

To play, run Dominion.py
Click the 'Done' button to end the current phase.
Action, buy, and victory information printed to the console. 


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

Commit 6
-Updated function to determine the winner at the end of a game

Commit 7
-Moved code to update screen into game_functions.py

Commit 9/26/18
-Supply pile information displayed on screen
-All 10 action cards work
-Number of players can be changed

check_events() function in game_functions.py module currently very messy and needs to be refactored
