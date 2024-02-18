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
		# for square in ch.SQUARES:
		# 	piece = self.__game.board.piece_at(square)
		# 	if piece is None:
		# 		continue
		# 	if piece.color == ch.WHITE:
		# 		score_total += Dt.PIECE_VALUES[piece.piece_type-1]
		# 	else:
		# 		score_total -= Dt.PIECE_VALUES[piece.piece_type-1]
		# return score_total
		for square in ch.SQUARES:
			piece = self.__game.board.piece_at(square)
			if piece is None:
				continue
			if piece.color == ch.WHITE:
				score_total += Dt.PIECE_VALUES[piece.piece_type - 1]  # Subtract for white pieces
			else:
				score_total -= Dt.PIECE_VALUES[piece.piece_type - 1]  # Add for black pieces
		return score_total

	def alpha_beta(self, max_depth : int = 4) -> ch.Move :
		if self.__game.active_player:
			print("Only the second player can be an ai")
			raise ValueError
		return self.maximize(max_depth)[1]

	def maximize(self, depth : int, move : ch.Move = None) -> list[float, ch.Move]:
		if depth == 0 or self.__game.is_over:
			score = self.evaluation()
			# print(score, " player : ", int(self.__game.active_player), " action chosen : ", move)
			# print(self.__game.board)
			return score + depth, move
		final_score = float('-inf')
		final_action = None
		print("nb move : ", len(list(self.__game.active_player_actions)))
		# raise ValueError
		for action in self.__game.active_player_actions:
			self.__game.push_move(action)  # try the move
			# self.set_move(move)
			# self.play_move()
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
			score = self.evaluation()
			# print(self.__game.board)
			return score + depth, move
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

