import sys

sys.path.insert(0,"../")
import matplotlib.pyplot as plt


# return playerIsAWinner
    # if(i>0):
    #     player1WinningAvg.append((player1Won/i)*100)
    #     if(playerIsAWinner and player_i == 0):
    #         player1Won = player1Won+1
    #     if(there_is_a_winner and i%10==0):
    #         movingAvg = np.convolve(player1WinningAvg, np.ones(10)/10)
    #         plt.plot(movingAvg)
    #         plt.pause(0.001)
    # print("Success... Saving history to numpy file")
    # g.save_hist("game_history.npy")
    # print("Saving game video")
    # g.save_hist_video("game_video.mp4")
# plt.savefig("SuccessRate.png")
# print("Success: {0}%".format((player1Won/trainingGames)*100))
# return True



    

def randwalk():
    import ludopy
    from PIL import Image as pilImg
    from QLearning.QTable import Rewards
    from QLearning.stateSpace import Action
    from QLearning.stateSpacePlayer import StateSpacePlayer
    from test.Qlearn import Qplayer, plottesting
    import numpy as np


    debug = False
    aiPlayer = 0
    playerNathan = 2
    ghosts = [1, 3]
    num_of_opp = 3-len(ghosts)
    g = ludopy.Game(ghost_players=ghosts)
    qLearning = Rewards(4, 10)
    player1Won=0
    player2Won=0
    player1WinningAvg = []
    player2WinningAvg = []
    trainingGames = 1000
    plt.axis([0, trainingGames, 0, 100])
    for i in range(trainingGames):
        there_is_a_winner = False
        g.reset()
        player1 = StateSpacePlayer(aiPlayer)
        player2 = Qplayer()
        while not there_is_a_winner:
            (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner,
            there_is_a_winner), player_i = g.get_observation()

            if len(move_pieces):
                if(player_i == playerNathan):
                    player2.nextmove(player_i, player_pieces, enemy_pieces, dice, move_pieces)
                    piece_to_move = player2.piece


                elif(player1._myPlayerIdx == player_i):
                    if(debug):
                        print("Dice: {0}".format(dice))
                    gotKilled, actionTable = player1.update(g.players,move_pieces, dice)
                    state,action = qLearning.ChooseNextAction(player_i, actionTable)
                    if(player1._lastMove!=None):
                        (lastState, lastAction) = player1._lastMove
                        if(gotKilled):
                            #shit, i got killed in the mean time... 
                            qLearning.Reward(lastState, state, Action.Die.value)
                        else:
                            qLearning.Reward(lastState, state, lastAction)
                    piece_to_move = player1.getPiceToMove(state, action)
                    if(not piece_to_move in move_pieces):
                        boardImg = g.render_environment()
                        # img = pilImg.fromarray(boardImg)
                        # img.save("test.jpeg")
                        # raise RuntimeError("I fucked it up again, cannot move this piece...")

                else:
                    piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
                
                # print("Dice: {0}".format(dice))
                
                
                
            else:
                piece_to_move = -1
            try:
                _, _, _, _, playerIsAWinner, there_is_a_winner = g.answer_observation(piece_to_move)
                if(debug):
                    boardImg = g.render_environment()
                    img = pilImg.fromarray(boardImg)
                    img.save("test.jpeg")

                #let's plot the data

            except Exception as e:
                boardImg = g.render_environment()
                img = pilImg.fromarray(boardImg)
                img.save("test.jpeg")
                print("Damn it, not again!!!!!!!!!!!1")
                print(e)
                # g.save_hist("game_history.npy")
                # print("Saving game video")
                # g.save_hist_video("game_video.mp4")
                return
        if(i>0):
            player1WinningAvg.append((player1Won/i)*100)
            player2WinningAvg.append((player2Won / i) * 100)
            if(g.first_winner_was==player1._myPlayerIdx):
                player1Won = player1Won+1
            if(g.first_winner_was ==playerNathan):
                player2Won = player2Won+1
            if(there_is_a_winner and i%20==0):
                movingAvg = np.convolve(player1WinningAvg, np.ones(10)/10)
                # plt.plot(movingAvg)
                # plt.pause(0.001)
        # print("Success... Saving history to numpy file")
        # g.save_hist("game_history.npy")
        # print("Saving game video")

    # plt.savefig("SuccessRate.png")
    # g.save_hist_video("game_video.mp4")
    df = plottesting(np.arange(i), player2WinningAvg, num_of_opp)
    print("Success Jan: {0}%".format((player1Won/trainingGames)*100))
    print("Success Nathan: {0}%".format((player2Won/trainingGames)*100))

    return True



randwalk()
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, randwalk())


# if __name__ == '__main__':
#     unittest.main()