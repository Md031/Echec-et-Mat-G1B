import pygame as Pg
from Window import Window
from Data import Utils
from sys import argv

def main() :
    game_type : bool = False
    if len(argv) > 1 and argv[1] == "-ia":
        game_type = True
        print(argv[1])
    window : Window = Window((Utils.DEFAULT_BOARD_DIMENSIONS, Utils.DEFAULT_BOARD_DIMENSIONS), game_type)
    window.main_loop()

if __name__ == '__main__' :
    main()