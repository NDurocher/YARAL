from ludopy.player import Player
from enum import Enum
import numpy as np
from QLearning.actionTable import ActionTable

class State(Enum):
    Home=0 #state in which the token is home, which also is the starting position.
    Safe=1 #state in which the token has reached goal.
    Unsafe=2 # state where the token is safe but not at home or goal.
    Danger=3 #state in which the token is in danger of being knocked home before the next turn.

class Action(Enum):
    MoveOut=0 # Moving token out of start
    Normal=1 # Moving eyes of dice
    Goal=2 # Move into goal position
    Star=3 #Move on star (jump forward)
    Globe=4 # Move to a save point
    Protect=5 #Move to same token as yourself -> save
    Kill=6 # Kill another player
    Die=7 #Move to a field where opponent has 2 or more pieces
    GoalZone=8 #Move into goal zone
    Nothing=9 #nothing possible


class StateSpace():
    _quarterGameSize=13
    _starPositions=[5,12,18,25,31,38,44,51]
    _globePositionsGlobal=[9,22,35,48,53]
    _globePositionsLocal=[1]
    _dangerPositionsGlobal=[1,14,27,40]
    LocalPlayerPosition=[Player(), Player(), Player(), Player()]
    GlobalPlayerPosition = [Player(), Player(), Player(), Player()]
    PlayerActionTable=ActionTable(len(State), len(Action))


    def __init__(self, Debug=0):
        super().__init__()
        self._debug=Debug

    def _GlobPos(self,player,piece):
        return self.GlobalPlayerPosition[player].pieces[piece]
    
    def _LocPos(self,player,piece):
        return self.LocalPlayerPosition[player].pieces[piece]

    def _UpdateQTable(self,player,action,piece,value):
        self.PlayerActionTable.UpdateQTable(action,piece,value)
        if(self._debug):
            print("UpdateQTable, player: {0}, state: {2}, piece:{3}, action: {1}".format(player,action,self.PlayerActionTable._state, piece))

    def _UpdatePlayerPositions(self, players):
        self.LocalPlayerPosition=players
        indexPlayer = 0
        for player in players:
            indexPiece=0
            for piece in player.pieces:
                if(piece==0):
                    self.GlobalPlayerPosition[indexPlayer].pieces[indexPiece]=0
                elif(piece==59):
                    self.GlobalPlayerPosition[indexPlayer].pieces[indexPiece]=0
                else:
                    self.GlobalPlayerPosition[indexPlayer].pieces[indexPiece]=(piece+(self._quarterGameSize*indexPlayer))%52
                indexPiece = indexPiece+1
            indexPlayer = indexPlayer+1

    def _CheckIfPieceIsSafe(self,player,piece):
        localPos = self._LocPos(player,piece)
        globalPos = self._GlobPos(player,piece)

        if(globalPos in self._globePositionsGlobal or localPos in self._globePositionsLocal):
            return True
        if(localPos!=0 and localPos!=59 and len(np.where(self.LocalPlayerPosition[player].pieces==localPos)[0])>1):
            return True
        return False

    def _CheckIfPieceIsInDanger(self,player,piece, enemyList):
        localPos = self._LocPos(player,piece)
        globalPos = self._GlobPos(player,piece)
        
        if(localPos>53 or localPos ==1):
            return False

        # if(pos in self._globePositions):
        #     return False
        
        if(globalPos in self._dangerPositionsGlobal):
            return True
        dangerPositions = np.empty
        
        for i in range(1,6):
            dangerPositions = np.append(dangerPositions,np.add(enemyList,i))

        if(globalPos in dangerPositions):
            return True
        return False
        # for i in range(1,6):
        #     if pos-i>=1:
        #         positionsOfInterest.append(pos-i)
        #     else:
        #         positionsOfInterest.append((self._quarterGameSize*4)-(pos-i))

        # for i in range(len(self.GlobalPlayerPosition)):
        #     if i==player:
        #         continue
        #     for posIdx in range(len(self.GlobalPlayerPosition[i].pieces)):
        #         pPos = self._GlobPos(i,posIdx)
        #         if(pPos in positionsOfInterest):
        #             return True
        # return False

    #Return: (killList,dieList)
    def _GetEnemyList(self,player):
        killList = []
        dieList = []
        for enemyPlayerIndex in range(len(self.GlobalPlayerPosition)):
            for enemyPieceIndex in range(len(self.GlobalPlayerPosition[enemyPlayerIndex].pieces)):
                enemyPos = self._GlobPos(enemyPlayerIndex,enemyPieceIndex)
                if(enemyPos>53 or enemyPos==0):
                    continue
                if(enemyPos in killList):
                    dieList.append(enemyPos)
                    killList.remove(enemyPos)
                else:
                    killList.append(enemyPos)
        enemyList =[]
        enemyList.extend(killList)
        enemyList.extend(dieList)
        return (killList,dieList,enemyList)

    def _SetPlayerState(self, player, piece, enemyList):
        if(self._LocPos(player,piece)==0):
            self.PlayerActionTable.SetState(State.Home)
        elif(self._CheckIfPieceIsInDanger(player,piece, enemyList)):
            self.PlayerActionTable.SetState(State.Danger)
        elif(self._CheckIfPieceIsSafe(player,piece)):
            self.PlayerActionTable.SetState(State.Safe)
        else:
            self.PlayerActionTable.SetState(State.Unsafe)

    def _UpdateMoveOutAction(self,player,piece,dice):
        if(self._LocPos(player,piece)==0 and dice==6) :
            self._UpdateQTable(player, Action.MoveOut, piece,1)
            return True
        return False
        
    def _UpdateNormalAction(self,player,piece,dice):
        if(self._LocPos(player,piece)==0):
            return False
        if(self._LocPos(player,piece)+dice<=59):
            self._UpdateQTable(player, Action.Normal,piece,1)
            return True
    
    def _UpdateGoalAction(self,player,piece,dice):
        localTargetPos = self._LocPos(player,piece)+dice
        if(localTargetPos==59):
            self._UpdateQTable(player, Action.Goal, piece,1)
            return True
        return False

    def _UpdateStarAction(self,player,piece,dice):
        if(self._LocPos(player,piece)+dice) in self._starPositions:
            self._UpdateQTable(player, Action.Star,piece,1)
            return True
        return False
    
    def _UpdateGlobeAction(self,player,piece,dice):
        if(self._GlobPos(player,piece)+dice) in self._globePositionsGlobal:
            self._UpdateQTable(player, Action.Globe,piece,1)
            return True
        return False

    def _UpdateProtectAction(self,player, piece,dice):
        targetPos = self._LocPos(player,piece)+dice
        if(targetPos>53):
            return False
        for i in range(len(self.LocalPlayerPosition)):
            if(i==piece):
                continue
            if(targetPos == self._LocPos(player,i)):
                self._UpdateQTable(player, Action.Protect,piece,1)
                return True
        return False

    def _UpdateKillAction(self,player,piece,dice,killList):
        localTargetPos = self._LocPos(player,piece)+dice
        if(localTargetPos>53):
            return False
        
        targetPos = self._GlobPos(player,piece)+dice
        if(targetPos in killList and targetPos not in self._globePositionsGlobal and localTargetPos not in self._globePositionsLocal):
            self._UpdateQTable(player,Action.Kill,piece,1)
            return True
        return False

    def _UpdateDieAction(self,player,piece,dice,dieList):
        localTargetPos = self._LocPos(player,piece)+dice
        if(localTargetPos>53):
            return False

        targetPos = self._GlobPos(player,piece)+dice
        if(targetPos in dieList):
            self._UpdateQTable(player, Action.Die,piece,1)
            return True
        return False

    def _UpdateGoalZone(self,player,piece,dice):
        localTargetPos = self._LocPos(player,piece)+dice
        if(localTargetPos>53 and localTargetPos<59):
            self._UpdateQTable(player,Action.GoalZone,piece,1)
            return True
        return False

    def _UpdateNotingAction(self,player,piece):
        pieceActionTable = self.PlayerActionTable._actionTable[piece]
        if(len(pieceActionTable[np.logical_not(np.isnan(pieceActionTable))])==0):
            self._UpdateQTable(player,Action.Nothing, piece,1)
            return True
        return False

    def Update(self, players,currentPlayer, piecesToMove, dice):
        self._UpdatePlayerPositions(players)
        self.PlayerActionTable.Reset()
        player = players[currentPlayer]
        (killList,dieList,enemyList) = self._GetEnemyList(player)
        for piece in piecesToMove:
            self._SetPlayerState(currentPlayer, piece,enemyList)
            if(self._UpdateMoveOutAction(currentPlayer,piece,dice)):
                continue
            if(self._UpdateGoalAction(currentPlayer,piece,dice)):
                continue
            if(self._UpdateStarAction(currentPlayer,piece,dice)):
                continue
            if(self._UpdateGlobeAction(currentPlayer,piece,dice)):
                continue
            if(self._UpdateProtectAction(currentPlayer,piece,dice)):
                continue
            if(self._UpdateKillAction(currentPlayer,piece,dice,killList)):
                continue
            if(self._UpdateDieAction(currentPlayer,piece,dice,dieList)):
                continue
            if(self._UpdateGoalZone(currentPlayer,piece,dice)):
                continue
            if(self._UpdateNormalAction(currentPlayer,piece,dice)):
                continue
            if(self._UpdateNotingAction(currentPlayer,piece)):
                continue
