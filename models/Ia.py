import random as rd
import models.game as gm
import chess as ch
import data as Dt
import torch
from NeuralNetwork.chessNet import ChessNet 
from NeuralNetwork.NeuralNetworkPickMoves import choose_move
import random
import time
# import controllers.GameController as GCtrl


class Ai:   #Interface class
	def __init__(self, color, game = None):
		self.game = game
		self.color = color

	def move():
		raise Exception("NotImplementedException")
	
	def set_game(self, game):
		self.game = game


class Random(Ai):
	def __init__(self, color, game = None):
		super().__init__(color, game)

	def move(self) -> ch.Move :
		move = random.choice(list(self.game.board.legal_moves))
		return move
	
class Minimax(Ai):
	def __init__(self, color, game = None):
		super().__init__(color, game)

	def move(self, max_depth: int = 4) -> ch.Move:
		if self.game.active_player == ch.WHITE:
			return self.maximize(max_depth)[1]
		else :
			return self.minimize(max_depth)[1]

	def evaluation(self) -> float:
		score_total : int = 0
		for square in ch.SQUARES:
			piece = self.game.board.piece_at(square)
			if piece is None:
				continue
			if piece.color == ch.WHITE:
				score_total += Dt.PIECE_VALUES[piece.piece_type - 1] + Dt.PIECE_TABLES_WHITE[piece.piece_type - 1][square]
			else:
				score_total -= Dt.PIECE_VALUES[piece.piece_type - 1] + Dt.PIECE_TABLES_BLACK[piece.piece_type - 1][square]
		return score_total	
	
	def maximize(self, depth : int, alpha : float = float('-inf'), 
	beta : float = float('inf'), move : ch.Move = None) -> list[float, ch.Move]:
		if depth == 0 or self.game.is_over:
			if self.game.board.is_checkmate():
				if  self.game.active_player != self.color:    #If the current player has checkmate
					evaluation = float("INF") if self.color == ch.WHITE else float("-INF")
				else:
					evaluation = float("-INF") if self.color == ch.WHITE else float("INF")
			else:
				evaluation = self.evaluation()
			return evaluation, move

		final_score = float('-inf')
		final_action = None
		for action in self.game.active_player_actions:
			self.game.push_move(action)  # try the move
			action_score = self.minimize(depth - 1, alpha, beta, action)[0]
			if action_score > final_score:
				final_score = action_score
				final_action = action
			self.game.pop_move()  # cancel the move
			if final_score >= beta:  # pruning part
				return final_score, final_action
			alpha = max(alpha, final_score)
		return final_score, final_action

	def minimize(self, depth : int, alpha : float = float('-inf'), 
	beta : float = float('inf'), move : ch.Move = None) -> list[float, ch.Move]:
		if depth == 0 or self.game.is_over:
			if self.game.board.is_checkmate():
				if  self.game.active_player != self.color:    #If the current player has checkmate
					evaluation = float("INF") if self.color == ch.WHITE else float("-INF")
				else:
					evaluation = float("-INF") if self.color == ch.WHITE else float("INF")
			else:
				evaluation = self.evaluation()
			return evaluation, move
		final_score = float('inf')
		final_action = None
		for action in self.game.active_player_actions:
			self.game.push_move(action)  # try the move
			action_score = self.maximize(depth - 1, alpha, beta, action)[0]
			if action_score < final_score:
				final_score = action_score
				final_action = action
			self.game.pop_move()  # cancel the move
			if final_score <= alpha:  # pruning part
				return final_score, final_action
			beta = min(beta, final_score)
		return final_score, final_action
	
class NeuronalNetwork(Ai):
    def __init__(self, color, ModelPath="NeuralNetwork/ChessModel.pt", game = None):
        super().__init__(color, game)
        self.model = ChessNet()

        # Checks if the a GPU is available
        if torch.cuda.is_available():
            print("Cuda is available")
            device = "cuda"
            self.model.load_state_dict(torch.load(ModelPath))
        else: # for CPU-only machines
            print("Cuda is unavailable")
            device = "cpu"
            self.model.load_state_dict(torch.load(ModelPath, map_location=torch.device('cpu')))
        
        self.model.eval()
        self.model.to(device)

    
    def move(self):
        move = choose_move(self.game.board, self.color, self.model)
        return move
