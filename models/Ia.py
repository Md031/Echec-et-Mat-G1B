import random as rd
import Data as Dt
import models.Game as Gm
import controllers.GameController as GCtrl
import models.Move as Mv

# class Type_Pieces :
# 	PAWN = 0
# 	KNIGHT = 1
# 	BISHOP = 2
# 	ROOK = 3
# 	QUEEN = 4
# 	KING = 5
# 	KING_END_GAME = 6

class Ia:
	def __init__(self, game : Gm.Game, game_ctrl : GCtrl):
		self.__game_controller : GCtrl = game_ctrl
		self.__game = game
		self.__piece_type : dict["str" : int] = {"pawn" : 0, "knight" : 1, "bishop" : 2, "rook" : 3, "queen" : 4, "king" : 5}

	@property
	def game(self) -> Gm.Game :
		return self.__game

	@property
	def game_controller(self) -> GCtrl :
		return self.__game_controller

	def random_ia(self) -> Mv.Move :
		choice_move = rd.choice(self.game._valid_actions())
		return self.game_controller.action_conversion(choice_move)

	def minimax(self, max_depth : int = 3) -> Mv.Move :
		return self.maximize(max_depth)[1]

	def maximize(self, depth : int, move : Mv.Move = None) -> float :
		if depth == 0 or self.game.is_over :
			return self.evaluation(), move

		best_move : Mv.Move = None
		score : float = float("-INF")

		for player_action in self.game.active_player_actions :
			action = self.game_controller.action_conversion(player_action)
			self.game.push_move(action)
			self.game.update_state()
			action_score : float = self.minimize(depth - 1, action)[0]
			if action_score > score :
				score = action_score
				best_move = action
			self.game.pop_move()
			self.game.update_state()
		return score, best_move

	def minimize(self, depth : int, move : Mv.Move = None) -> float:
		if depth == 0 or self.game.is_over :
			return self.evaluation(), move

		best_move : Mv.Move = None
		score : float = float("INF")

		for player_action in self.__game.active_player_actions :
			action = self.game_controller.action_conversion(player_action)
			self.game.push_move(action)
			self.game.update_state()
			action_score : float = self.maximize(depth - 1, action)[0]
			if action_score < score :
				score = action_score
				best_move = action
			self.game.pop_move()
			self.game.update_state()
		return score, best_move

	def evaluation(self) -> float:
		score_total : int = 0
		pieces : list = self.game.board.get_player_pieces(self.game.active_player)
		for piece in pieces :
			pieces_type = self.__piece_type[piece.name]
			idx = int(piece.position.x) * self.game.board.size[0] + int(piece.position.y)
			if self.game.active_player == 0: # white pieces
				score_total += Dt.PIECE_TABLES_WHITE[pieces_type][idx]
			else: # black pieces
				score_total -= Dt.PIECE_TABLES_BLACK[pieces_type][idx]
		return score_total
		# TODO : add the change of score when we are in the end game
