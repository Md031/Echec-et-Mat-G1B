import random as rd
import models.game as gm
import chess as ch
import data as Dt
# import controllers.GameController as GCtrl

class Ia:
	def __init__(self, game : gm.Game):
		self.__game = game
		
	def random_ia(self) -> ch.Move :
		actions = list(self.__game.active_player_actions)
		return rd.choice(actions)

	def evaluation(self) -> float:
	    score_total : int = 0
	    for square in ch.SQUARES:
	        piece = self.__game.board.piece_at(square)
	        if piece is None:
	            continue
	        if piece.color == ch.WHITE:
	            score_total -= Dt.PIECE_VALUES[piece.piece_type - 1]
	        else:
	            score_total += Dt.PIECE_VALUES[piece.piece_type - 1]
	    return score_total

	def alpha_beta(self, max_depth: int = 4) -> ch.Move:
		if self.__game.active_player:
			print("Only the second player can be an ai")
			raise ValueError
		return self.maximize(max_depth, float('-inf'), float('inf'))[1]

	def maximize(self, depth: int, alpha: float, beta: float, move: ch.Move = None) -> list[float, ch.Move]:
		if depth == 0 or self.__game.is_over:
			return self.evaluation(), move
		final_score = float('-inf')
		final_action = None
		for action in self.__game.active_player_actions:
			self.__game.push_move(action)  # try the move
			testScore : float = self.minimize(depth-1, alpha, beta, action)[0]
			if testScore > final_score:
				final_score = testScore
				final_action = action
			self.__game.pop_move()  # cancel the move
			if final_score >= beta:
				return final_score, final_action
			alpha = max(alpha, final_score)
		return final_score, final_action

	def minimize(self, depth: int, alpha: float, beta: float, move: ch.Move = None) -> list[float, ch.Move]:
		if depth == 0 or self.__game.is_over:
			score = self.evaluation()
			return score, move
		final_score = float('inf')
		final_action = None
		for action in self.__game.active_player_actions:
			self.__game.push_move(action)  # try the move
			test_score, _ = self.maximize(depth - 1, alpha, beta, action)
			if test_score < final_score:
				final_score = test_score
				final_action = action
			self.__game.pop_move()  # cancel the move
			if final_score <= alpha:
				return final_score, final_action
			beta = min(beta, final_score)
		return final_score, final_action
