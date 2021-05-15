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
    from test.Qlearn import Qplayer, plottestcomb
    import numpy as np


    debug = False
    aiPlayer1 = 1
    aiPlayer2 = 2
    aiPlayer3 = 3
    playerNathan = 0
    ghosts = [[1, 3], [2], []]
    for ghost in ghosts:
        num_of_opp = 3-len(ghost)
        g = ludopy.Game(ghost_players=ghost)
        qLearning = Rewards(4, 10)
        # player1Won=0
        # player2Won = 0
        # player1WinningAvg = []
        # player2WinningAvg = []
        trainingGames = 1000
        wins = np.zeros([4], dtype=int)
        winrate = []
        for i in range(trainingGames):
            there_is_a_winner = False
            g.reset()
            player1 = StateSpacePlayer(aiPlayer1)
            player2 = StateSpacePlayer(aiPlayer2)
            player0 = Qplayer()
            player3 = StateSpacePlayer(aiPlayer3)
            while not there_is_a_winner:
                (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner,
                there_is_a_winner), player_i = g.get_observation()

                if len(move_pieces):
                    if player_i == playerNathan:
                        player0.nextmove(player_i, player_pieces, enemy_pieces, dice, move_pieces)
                        piece_to_move = player0.piece

                    elif(player1._myPlayerIdx == player_i):
                        # if(debug):
                        #     print("Dice: {0}".format(dice))
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
                        # if player_pieces[piece_to_move] + dice > 59:
                        #     Jovershoots += 1
                        # if(not piece_to_move in move_pieces):
                        #     boardImg = g.render_environment()
                            # img = pilImg.fromarray(boardImg)
                            # img.save("test.jpeg")
                            # raise RuntimeError("I fucked it up again, cannot move this piece...")
                    elif(player2._myPlayerIdx == player_i):
                        # if(debug):
                        #     print("Dice: {0}".format(dice))
                        gotKilled, actionTable = player2.update(g.players, move_pieces, dice)
                        state, action = qLearning.ChooseNextAction(player_i, actionTable)
                        if (player2._lastMove != None):
                            (lastState, lastAction) = player2._lastMove
                            if (gotKilled):
                                # shit, i got killed in the mean time...
                                qLearning.Reward(lastState, state, Action.Die.value)
                            else:
                                qLearning.Reward(lastState, state, lastAction)
                        piece_to_move = player2.getPiceToMove(state, action)
                        # if player_pieces[piece_to_move] + dice > 59:
                        #     Jovershoots += 1
                        # if(not piece_to_move in move_pieces):
                        #     boardImg = g.render_environment()
                        # img = pilImg.fromarray(boardImg)
                        # img.save("test.jpeg")
                        # raise RuntimeError("I fucked it up again, cannot move this piece...")
                    elif(player3._myPlayerIdx == player_i):
                        # if(debug):
                        #     print("Dice: {0}".format(dice))
                        gotKilled, actionTable = player3.update(g.players, move_pieces, dice)
                        state, action = qLearning.ChooseNextAction(player_i, actionTable)
                        if (player3._lastMove != None):
                            (lastState, lastAction) = player3._lastMove
                            if (gotKilled):
                                # shit, i got killed in the mean time...
                                qLearning.Reward(lastState, state, Action.Die.value)
                            else:
                                qLearning.Reward(lastState, state, lastAction)
                        piece_to_move = player3.getPiceToMove(state, action)
                        # if player_pieces[piece_to_move] + dice > 59:
                        #     Jovershoots += 1
                        # if(not piece_to_move in move_pieces):
                        #     boardImg = g.render_environment()
                        # img = pilImg.fromarray(boardImg)
                        # img.save("test.jpeg")
                        # raise RuntimeError("I fucked it up again, cannot move this piece...")

                    else:
                        piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
                else:
                    piece_to_move = -1
                try:
                    _, _, _, _, playerIsAWinner, there_is_a_winner = g.answer_observation(piece_to_move)
                    # if(debug):
                    #     boardImg = g.render_environment()
                    #     img = pilImg.fromarray(boardImg)
                    #     img.save("test.jpeg")
                    #
                    # #let's plot the data
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

            wins[g.get_winner_of_game()] += 1
            winrate.append(wins[0] / (i + 1) * 100)
            if i != 0:
                if (i % int(trainingGames / 10)) == 0:
                    print(i)
        print("Win percentage: ", int(wins[0] / trainingGames * 100), "%")
        print(wins)
        if num_of_opp == 1:
            op1 = winrate
        elif num_of_opp == 2:
            op2 = winrate
        else:
            op3 = winrate
            # Jovers.append(Jovershoots)
            # Novers.append(Novershoots)
            # if(i>0):
            #     player1WinningAvg.append((player1Won/i)*100)
            #     player2WinningAvg.append((player2Won / i) * 100)
            #     if g.first_winner_was == player1._myPlayerIdx:
            #         player1Won = player1Won+1
            #     if g.first_winner_was == playerNathan:
            #         player2Won = player2Won+1
                # if(there_is_a_winner and i%20==0):
                    # movingAvg = np.convolve(player1WinningAvg, np.ones(10)/10)
                    # plt.plot(movingAvg)
                    # plt.pause(0.001)
            # print("Success... Saving history to numpy file")
            # g.save_hist("game_history.npy")
            # print("Saving game video")
        # plt.savefig("SuccessRate.png")
        # g.save_hist_video("game_video.mp4")
    df = plottestcomb(np.arange(i + 1), op1, op2, op3)
    df.to_csv('TestingData_Jan.csv')

    return True



randwalk()
