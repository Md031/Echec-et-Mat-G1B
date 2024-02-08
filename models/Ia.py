import random as rd
import Data as Dt
from models.Game import Game
from enum import Enum
import controllers.GameController as GCtrl
import models.Move as Mv

class Type_Pieces(Enum):
	PAWN = 0
	KNIGHT = 1
	BISHOP = 2
	ROOK = 3
	QUEEN = 4
	KING = 5
	KING_END_GAME = 6

class Ia:
	def __init__(self, game: Game, game_ctrl: GCtrl):
		self.__Gctrl : GCtrl = game_ctrl
		self.__game = game
		self.__Type_Pieces : Enum = Type_Pieces
		self.__num_column : int = game.board.get_grid_size
		self.__dic_score : dict = dict()
		self.__last_action : Mv = None

	@property
	def get_game(self) -> Game:
		return self.__game

	def random_ia(self) -> (Dt.Point, Dt.Point):
		choice_move = rd.choice(self.__game._valid_actions())
		begin = Dt.convert_coordinates(choice_move[:2])
		ending = Dt.convert_coordinates(choice_move[2:])
		return begin, ending

	def minimax(self, max_depth: int = 3) -> Mv.Move :
		if self.__game.active_player != 1:
			print("The Ia can only be the second player.")
		finalScore = float('-inf')
		finalAction = None
		# TODO : save the previous score of a state 
		for action in self.__game._valid_actions():
			# print("in minimax action : ", action)
			choice = self.__Gctrl.action_conversion(action)
			# self.__game.set_move_type(choice)
			self.__game.push_move(choice)
			self.__game.update_state()
			self.__last_action = action
			testScore = self.maximize(max_depth - 1)

			self.__dic_score[(self.__game.board.fen, action)] = testScore
			if finalScore < testScore:
				finalScore = testScore
				finalAction = choice
				# print("action : ", finalAction, " score : ", finalScore)
			self.__game.pop_move() # we cancel the action we did
			self.__game.update_state()
		for elem in self.__dic_score:
			print(elem)
		self.__dic_score = {}  # reset the dictionnary
		return choice

	def maximize(self, depth : int) -> float:
		if depth == 0 or self.__game.is_over():
			return self.__dic_score[(self.__game.board.fen, self.__last_action)] + depth
		else:
			best_score = float('-inf')
			for action in self.__game._valid_actions():
				choice = self.__Gctrl.action_conversion(action)
				# self.__game.set_move_type(choice)
				self.__game.push_move(choice)
				self.__game.update_state()
				self.__last_action = action
				state_score = self.evaluation(self.__game)

				self.__dic_score[(self.__game.board.fen, action)] = state_score
				best_score = max(state_score, self.minimize(depth-1))
				self.__game.pop_move()
				self.__game.update_state()
			return best_score

	def minimize(self, depth: int) -> float:
		if depth == 0 or self.__game.is_over():
			return self.__dic_score[(self.__game.board.fen, self.__last_action)] - depth
		else:
			best_score = float('inf')
			for action in self.__game._valid_actions():
				choice = self.__Gctrl.action_conversion(action)
				# self.__game.set_move_type(choice)
				self.__game.push_move(choice)
				self.__game.update_state()
				self.__last_action = action
				state_score = self.evaluation(self.__game)

				self.__dic_score[(self.__game.board.fen, action)] = state_score
				best_score = min(state_score, self.maximize(depth-1))
				self.__game.pop_move()
				self.__game.update_state()
			return best_score

	def evaluation(self, state: Game) -> float:
		score_total = 0
		pieces = state.board.get_player_pieces(state.active_player)
		for elem in pieces:
			pos_x, pos_y = Dt.convert_coordinates(elem.chess_positon).x, Dt.convert_coordinates(elem.chess_positon).y # get the position of the piece we're looking at
			name = elem.name.upper()
			pieces_type = Type_Pieces[name].value
			idx = int(pos_x) * self.__num_column + int(pos_y)
			if state.active_player == 0: # white pieces
				score_total += Dt.PIECE_TABLES_WHITE[pieces_type][idx]
			else: # black pieces
				score_total -= Dt.PIECE_TABLES_BLACK[pieces_type][idx]
		return score_total
		# TODO : add the change of score when we are in the end game
