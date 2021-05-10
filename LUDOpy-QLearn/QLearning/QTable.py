import numpy as np
import random as r
from QLearning.stateSpace import Action
from QLearning.stateSpace import State
import os.path

class Rewards:
    RewardsTable=np.zeros(len(Action))

    QTable=None
    tableName = "QTable.txt"
    def __init__(self, states,actions, epsilonGreedy=0.9, gamma=0.9, learningRate=0.1):
        super().__init__()
        if(os.path.isfile(self.tableName)):
            self.QTable = np.loadtxt(self.tableName, delimiter=',')
        else:
            self.QTable = np.zeros([states,actions])
        self._epsilonGreedy = epsilonGreedy
        self._gamma = gamma
        self._lr = learningRate

        self.RewardsTable[Action.MoveOut.value]=0.25
        self.RewardsTable[Action.Normal.value]=0.01
        self.RewardsTable[Action.Goal.value]=0.8
        self.RewardsTable[Action.Star.value]=0.5
        self.RewardsTable[Action.Globe.value]=0.4
        self.RewardsTable[Action.Protect.value]=0.3
        self.RewardsTable[Action.Kill.value]=0.4
        self.RewardsTable[Action.Die.value]=0
        self.RewardsTable[Action.GoalZone.value]=0.4
        # self.RewardsTable[Action.Nothing.value]=0

    def GetStateActionOfArray(self,value,array):
        if(np.isnan(value)):
            return (-1,-1)
        idx = np.where(array==value)
        rIdx = r.randint(0,len(idx[0])-1)
        state =idx[0][rIdx]
        action =idx[1][rIdx]
        return (state,action)


    def ChooseNextAction(self,player,actionTable):
        try:
            qTableOptions = np.multiply(self.QTable,actionTable)
        except Exception as e:
            print(e)
        if(r.uniform(0,1)>self._epsilonGreedy):
            nz = actionTable[np.logical_not(np.isnan(actionTable))]
            if(len(nz)<1):
                raise RuntimeError("array to small...")
            randomValue = nz[r.randint(0,len(nz)-1)]
            state,action= self.GetStateActionOfArray(randomValue,actionTable)
        else:
            maxVal = np.nanmax(qTableOptions)
            state,action = self.GetStateActionOfArray(maxVal,qTableOptions)
            # state = np.where(qTableOptions==maxVal)[0][0]
            # action = np.where(qTableOptions==maxVal)[1][0]
        return (state,action)

    def Reward(self,state, newState, action):
        state = int(state)
        action = int(action)
        newState = int(newState)
        try:
            oldQ = self.QTable[state, action]
            deltaQ = self._lr * (self.RewardsTable[action] + self._gamma * np.max(self.QTable[newState, :]) - self.QTable[state, action])
            # if(action == Action.Die.value or action == Action.Die.value):
                # print("oldState: {1}, newState: {2}, newQ: {0}".format(oldQ+deltaQ, state, newState))
                
            self.QTable[state,action] =  oldQ+deltaQ
            # print("update q table, state: {0}, action:{1}".format(state,action))
        except:
            raise RuntimeError("God damn it")
            print("God damn it")

        
    def __del__(self):
        np.savetxt(self.tableName, self.QTable, delimiter=',',fmt='%1.3f')