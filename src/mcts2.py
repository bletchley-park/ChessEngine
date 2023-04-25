import chess
import math
import random
import time
from  encoder import boardToTensor
from ChessNet import ChessNet

random.seed(time.time())

chessNet = ChessNet()

board = chess.Board('r1bqkbnr/ppp2ppp/2np4/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 4')


print(board)

# board.push_san('e4')
# print(board)
# print()
# print(board.legal_moves)
# print()
# board.push_san('e5')
# print(board)
# print()
# board.push_san('Bc4')
# print(board)
# print(board.legal_moves)
# print()
# board.push_san('Nc6')
# print(board)
# print()
# board.push_san('Qf3')
# print(board)
# print()
# board.push_san('Nge7')
# print(board)
# print()

turn = board.turn

class Node:
    def __init__(self, state, parent = None, move = None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
    
    def __str__(self) -> str:
        return f'state = \n{self.state}\nwins = {self.wins}, visits = {self.visits}'

    def ucb_score(self, parent):
        if self.visits == 0:
            return float('inf')
        
        heuristic = chessNet(boardToTensor(self.state.__str__())) 
        return (self.wins / self.visits) + 1.4 * math.sqrt(2 * math.log(parent.visits) / self.visits) + 0.5 * heuristic.item()

    def expand(self):
        # print(f'expansion \n{self.state}')
        legal_moves = list(self.state.legal_moves)
        for move in legal_moves:
            new_state = self.state.copy()
            new_state.push(move)
            self.children.append(Node(new_state, self, move))

    # def select_child(self):
    #     #print(f'selection \n{self.state}')
    #     best_child = None
    #     best_score = float('-inf')
    #     for child in self.children:
    #         score = self.ucb_score(self)
    #         if score >= best_score:
    #             best_child = child
    #             best_score = score
    #     print(f'best_child = \n{best_child} : {best_child.ucb_score(self)}')
    #     return best_child
    
    def update(self, result):
        #print(f'updation \n{self.state} \nresult = {result}')
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.update(result)

class MCTS:
    def __init__(self, state, player):
        self.root = Node(state)
        self.player = player

    def select_child(self):
        #print(f'selection \n{self.state}')
        best_child = None
        best_score = float('-inf')
        for child in self.root.children:
            score = child.ucb_score(self.root)
            if score >= best_score:
                best_child = child
                best_score = score
        print(f'best_child = \n{best_child} : {best_child.ucb_score(self.root)}')
        return best_child

    def select_move(self, iterations = 500):
        node = self.root
        for i in range(iterations):
            if node.visits <= 100:
                if node.visits == 0 : node.expand()
                for child in node.children:
                    for i in range(10):
                        result = self.simulate(child.state.copy())
                        child.update(result)
                    # print(child)

                # for i in range(10):
                #     child = random.choice(node.children)
                #     for i in range(10):
                #         result = self.simulate(child.state.copy())
                #         child.update(result)

                # print(f'after expansion \n{node}')

            else:
                for child in node.children:
                    print(child)
                node = self.select_child()
            # if i % 10 == 0:
            #     print(f'selected state = \n{node.state}, i = {i/10}')
            
            # print(node.parent)
            # result = self.simulate(node.parent.state.copy())
            # node.update(result)

        best_move = self.select_child()
        print(f'best move = \n{best_move}')
        return best_move.move
    
    def simulate(self, state):
        #print(f'simulation \n{state}')
        if self.player == chess.WHITE:
            score = 1
        else:
            score = 0
            
        game_over = False
        i = 0
        while not game_over:
            if i % 20 == 0:
                # print(f'state = \n{state}, i = {i/20}')
                pass
            i += 1

            legal_moves = list(state.legal_moves)
            # print(legal_moves)
            if not legal_moves:
                if state.is_checkmate():
                    if state.turn:
                        return 1 - score
                    else:
                        return score
                else:
                    return 0.5
            move = random.choice(legal_moves)
            state.push(move)
            game_over = state.is_game_over()
        # print(f'final state = \n{state} and {state.result()}')
        if state.result() == "1-0":
            return score
        elif state.result() == "0-1":
            return 1-score
        else:
            return 0.5

player = MCTS(board, turn)
best_move = player.select_move()
print(f'main best move = \n{best_move}')
board.push(best_move)
print(board)
