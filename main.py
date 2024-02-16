import pygame as Pg
from window import Window
from data import Utils
from sys import argv
# import cProfile

def main() :
    Pg.init()
    game_type : bool = False
    if len(argv) > 1 and argv[1].lower() == "-ia":  # if we want to play with an ai
        game_type = True
        print(argv[1])
    window : Window = Window((Utils.DEFAULT_WINDOW_WIDTH, Utils.DEFAULT_WINDOW_HEIGHT), game_type)
    window.main_loop()

if __name__ == '__main__' :
    # cProfile.run('main()', sort='tottime')
    main()