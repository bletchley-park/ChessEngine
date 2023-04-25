import chess
import torch
import numpy as np

# board = chess.Board('r1bqkb1r/pppp1ppp/2n5/4p1N1/2B1n3/8/PPPP1PPP/RNBQK2R w KQkq - 0 5')


# board_string = board.__str__()

# print(board_string)


def boardToTensor(board_string : str):

    boardTensor = torch.zeros((6,8,8))

    i = 0
    j = 0

    boardSlide = {
        '.' : 0,
        'p' : 0,
        'b' : 1,
        'n' : 2,
        'r' : 3,
        'q' : 4,
        'k' : 5
    }

    boardPoint = {
        '.' : 0.0,
        'p' : 1.0,
        'b' : 3.0,
        'n' : 3.0,
        'r' : 5.0,
        'q' : 9.0,
        'k' : 10.0
    }

    for pos in range(0, 127, 2):
        sign = 1
        if board_string[pos].islower():
            sign = -1
            
        boardTensor[boardSlide.get(board_string[pos].lower())][i][j] = sign * boardPoint.get(board_string[pos].lower())
        
        j += 1

        if(j == 8):
            j = 0
            i += 1

    return boardTensor


# final_tensor = boardToTensor(board_string)
# print(final_tensor.shape)


    
