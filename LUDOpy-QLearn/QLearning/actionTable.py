import numpy as np

class ActionTableEntry:
        # __piece=[]
        # __value=[]
        def __init__(self,piece,value):
                super().__init__()
                # self.__piece.append(piece)
                # self.__value.append(value)
                self.pice=piece
                self.value=value
        
        def AddEntry(self,piece,value):
            self.__piece.append(piece)
            self.__value.append(value)


class ActionTable:
    _actionTable=None
    _state=0
    def __init__(self,states,actions):
        super().__init__()
        self.states=states
        self.actions=actions
        self.Reset()

    def SetState(self,state):
        self._state=state.value

    def GetActionTable(self):
        return self._actionTable
    
    def GetPieceToMove(self,state,action):
        if(state<0 or action<0):
            return -1
        return int(self._pieceToMove[state, action])

    def Reset(self):
        self._actionTable=np.full((self.states,self.actions),np.nan)#np.zeros((self.states, self.actions), dtype=np.object)
        self._pieceToMove=np.full((self.states,self.actions),np.nan)#np.zeros((self.states, self.actions), dtype=np.object)

    #todo: piece implementation missing...
    def UpdateQTable(self,action,piece,value):
        if(np.isnan(self._actionTable[self._state,action.value])):
            # self._qTable[self._state,action.value]=ActionTableEntry(piece,value)
            self._actionTable[self._state,action.value]=1
            self._pieceToMove[self._state,action.value]=piece
        # else:
        #     entry = self._qTable[self._state,action.value].AddEntry(piece,value)