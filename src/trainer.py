import os
import torch
import numpy as np
from torch import nn
import chess
from encoder import boardToTensor
from sf import sf
import random
from ChessNet import ChessNet, ValueLoss

state = chess.Board()

model = ChessNet()

loss_function = ValueLoss()

optimizer = torch.optim.Adam(model.parameters(), lr = 0.003)
scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[100,200,300,400], gamma=0.2)

print(model(boardToTensor(state.__str__()))) 

epochs = 8

simulations = 1000

for epoch in range(epochs):
    print(f'Epoch number {epoch}')
    for position in range(simulations):
        if position % 100 == 0:
            print(f'Simulation number {position}')
        state.reset()
        game_over = False
        i = 0
        while not game_over:
            if i % 20 == 0:
                print(f'state = \n{state}, \ni = {i//20}')
                pass
            i += 1

            pred = model(boardToTensor(state.__str__()))

            sf.set_fen_position(state.fen())
            loss = loss_function(pred, sf.get_evaluation()['value'])

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()
            legal_moves = list(state.legal_moves)
            # print(legal_moves)
            move = random.choice(legal_moves)
            state.push(move)
            game_over = state.is_game_over()
        # print(f'final state = \n{state} and {state.result()}')


def save_model(model_dictionary):
    checkpoint_directory = 'chessnet_directory'
    file_path = os.path.join(checkpoint_directory, 'model.pt')
    torch.save(model_dictionary, file_path)

model_dictionary = {
    'model_state' : model.state_dict(),
    'model_optimizer' : optimizer.state_dict()
}

save_model(model_dictionary)