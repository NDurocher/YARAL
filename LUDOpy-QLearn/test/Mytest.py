import unittest
import sys
import torch
from torch import autograd, nn, optim
import torch.nn.functional as F

sys.path.append("../")

batch_size = 5
input_size = 3
hidden_size = 4
num_classes = 4
learning_rate = 0.001

torch.manual_seed(123)
input = autograd.Variable(torch.rand(batch_size, input_size)) - 0.5
target = autograd.Variable((torch.rand(batch_size) * num_classes).long())
print('Target: ', target)
# print('\nInput: ', input)

class Model(nn.Module):
    def __init__(self,input_size, hidden_size, num_classes):
        super().__init__()
        self.h1 = nn.Linear(input_size, hidden_size)
        self.h2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        x = self.h1(x)
        x = torch.tanh(x)
        x = self.h2(x)
        x = F.softmax(x, dim=1)
        return x

model = Model(input_size = input_size, hidden_size = hidden_size, num_classes = num_classes)
opt = optim.Adam(params=model.parameters(), lr=learning_rate)

for epoch in range(1000):
    out = model(input)
    # print('\nOut: ', out)
    _, pred = out.max(1)
    # print('\nPrediction: ', pred)

    loss = F.nll_loss(out, target)
    print('\n Loss: ', loss)

    model.zero_grad()
    loss.backward()
    opt.step()

print('\nTarget: ', target)
print('\nPrediction: ', pred)
    # model.parameters()





# def randwalk():
#     import ludopy
#     import numpy as np
#
#     g = ludopy.Game()
#     there_is_a_winner = False
#
#     while not there_is_a_winner:
#         (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner,
#          there_is_a_winner), player_i = g.get_observation()
#
#         if len(move_pieces):
#             piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
#         else:
#             piece_to_move = -1
#
#         _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)
#
#     print("Saving history to numpy file")
#     g.save_hist("game_history.npy")
#     print("Saving game video")
#     g.save_hist_video("game_video.mp4")
#
#     return True
#
#
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, randwalk())
#
#
# if __name__ == '__main__':
#     unittest.main()
