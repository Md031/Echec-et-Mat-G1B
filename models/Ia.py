import random as rd
import models.game as gm
import chess as ch
import data as Dt
# import controllers.GameController as GCtrl

class Ia:
	def __init__(self, game : gm.Game):
		self.__game = game
		self.__alpha : float = float('-inf')
		self.__beta : float = float('inf')

	def random_ia(self) -> ch.Move :
		actions = list(self.__game.active_player_actions)
		return rd.choice(actions)

	def evaluation(self) -> float:
		score_total : int = 0
		for square in ch.SQUARES:
			piece = self.__game.board.piece_at(square)
			if piece is None:  # the empty squares of the board
				continue
			if piece.color == ch.WHITE and self.__game.active_player:
				score_total -= Dt.PIECE_VALUES[piece.piece_type -1] - Dt.PIECE_TABLES_WHITE[piece.piece_type - 1][square]
			elif piece.color == ch.BLACK and not self.__game.active_player:
				score_total += Dt.PIECE_VALUES[piece.piece_type -1] + Dt.PIECE_TABLES_BLACK[piece.piece_type - 1][square]
		return score_total

	def alpha_beta(self, max_depth : int = 4) -> ch.Move :
		if self.__game.active_player:
			print("Only the second player can be an ai")
			raise ValueError
		return self.maximize(max_depth)[1]

	def maximize(self, depth : int, move : ch.Move = None) -> list[float, ch.Move]:
		if depth == 0 or self.__game.is_over:
			return self.evaluation() + depth, move
		final_score = float('-inf')
		final_action = None
		for action in self.__game.active_player_actions:
			self.__game.push_move(action)  # try the move
			testScore : float = self.minimize(depth-1, action)[0]
			if testScore >= final_score:
				final_score = testScore
				final_action = action
			self.__game.pop_move()  # cancel the move
			if final_score >= self.__beta:
				return final_score, final_action
			self.__alpha = max(self.__alpha, final_score)
		return final_score, final_action

	def minimize(self, depth : int, move : ch.Move = None) -> list[float, ch.Move]:
		if depth == 0 or self.__game.is_over:
			return self.evaluation() - depth, move
		final_score = float('inf')
		final_action = None
		for action in self.__game.active_player_actions:
			self.__game.push_move(action)  # try the move
			testScore : float = self.maximize(depth-1, action)[0]
			if testScore >= final_score:
				final_score = testScore
				final_action = action
			self.__game.pop_move()  # cancel the move

			if final_score <= self.__alpha:
				return final_score, final_action
			self.__beta = min(self.__beta, final_score)
		return final_score, final_action
