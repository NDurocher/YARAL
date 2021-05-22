# LUDO_QLearning
A Q learning AI player for the LUDO board game

To use my player import Qlearn.py and Qs.txt from the LUDOpy-QLearn/test
You may need to edit the path in self.tablename on line 51

Define player:
  player0 = Qplayer()

Make move:
  player0.nextmove(player_i, player_pieces, enemy_pieces, dice, move_pieces)
            piece_to_move = player0.piece
            _, _, new_P0, new_enemy, _, there_is_a_winner = g.answer_observation(piece_to_move)
