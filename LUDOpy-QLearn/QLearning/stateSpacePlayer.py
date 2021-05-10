from QLearning.stateSpace import StateSpace
import numpy as np
class StateSpacePlayer(StateSpace):
    _myPlayerIdx = 0
    _lastMove=None
    _piecesInGame = 0


    def __init__(self, myPlayerIdx):
        super().__init__()
        self._myPlayerIdx = myPlayerIdx

    def update(self, players, piecesToMove, dice):
        piecesInGame = np.count_nonzero(players[self._myPlayerIdx].pieces)
        if(piecesInGame<self._piecesInGame):
            gotKilled=True
        else:
            gotKilled = False
        self._piecesInGame=piecesInGame
        super().Update(players, self._myPlayerIdx, piecesToMove, dice)
        return (gotKilled,self.PlayerActionTable.GetActionTable())

    def getPiceToMove(self, state, action):
        piecesToMove = self.PlayerActionTable.GetPieceToMove(state, action)
        self._lastMove = (state, action)
        return piecesToMove

    
