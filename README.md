# YARAL: Yet Another Reinforcement learning  Approach to Ludo
A Q learning AI player for the LUDO board game.

## Motivation
The object of the project was to create a player policy that learns to play the board game LUDO using a common reinforcement learning technique. The player policy was compared against a random action selecting opponent and another policy created by a classmate. This project was developed as part of the *Tools of Artificial Intellignece* class at the *University of Southern Denmark* in the Spring of 2021.

## Features
The player utilizes a state space of:
1. Home
2. Goal Zone
3. Safe
4. Danger

The home state refers to when the piece is not in play and can only be moved
when a six is rolled. A piece is in the goal zone when it occupies one of the final
six spaces before the goal. The safe state is when the piece is either on a globe
tile or when it is not within six tiles of an opponents piece such that it could be
sent home by the next roll. Finally, the danger state is defined when the pieces
is within striking distance of an enemy piece or on the coloured globe tile at the
opponents home. 

The player's action space consisting of 10 actions for various scenarios:
1. Open
2. Normal
3. Goal
4. Star
5. Globe
6. Protect
7. Kill
8. Overshoot Goal
9. Goal Zone
10. Null

The open, normal, goal, star, globe, protect and kill moves are all standard
playing moves defined by the rules of the game. However, the overshoot goal and
goal zone moves are added classification moves to effect the priority of moves
near the goal. In particular the overshoot goal move is used as an unwanted
action that occurs when a piece is in the goal area but the dice roll is higher
than the number of tiles needed to reach the goal. Finally the null action is a placeholder for when the player
has no active pieces to move.

The Q values are updated based on the standard temporal differnce equation:

![Q_learn_update](./Images/Q_learning_update.png)

## Results
The player policy was able to dominate a random selection player winning 83%, 70%, and 60% of games against one two and three opponents respectively.
![random_resuts](./Images/WR_all3Opp.png)

The player policy was also able to win a significant amount of games against a classmates policy player, where is won 68%, 52%, and 41% of games against one two and three opponents respectively.
![random_resuts](./Images/WR_all3Jan.png)

## How to use?
To use my player import Qlearn.py and Qs.txt from /src and ludopy from /LUDOpy/

Define player:
  player0 = Qplayer(tableName="/PATH to Qs.txt)

Make move:
  player0.nextmove(player_i, player_pieces, enemy_pieces, dice, move_pieces)
            piece_to_move = player0.piece
            _, _, new_P0, new_enemy, _, there_is_a_winner = g.answer_observation(piece_to_move)

## Credits
LUDOpy developed by https://github.com/SimonLBSoerensen/LUDOpy.
Classmate player policy created by Jan Ruben Schmid. LudoPy. https://github.com/janschmid/LudoPy.
