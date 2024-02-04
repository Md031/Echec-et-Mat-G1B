import random as rd
import Data as Dt
from models.Game import Game

class Ia:
	def __init__(self, game: Game):
		self.__game = game

	def random_ia(self):
		choice_move = rd.choice(self.__game._valid_actions())
		begin = Dt.convert_coordinates(choice_move[0:2])
		ending = Dt.convert_coordinates(choice_move[2:])
		return begin, ending