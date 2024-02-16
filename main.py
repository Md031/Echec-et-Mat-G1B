import pygame as Pg
from window import Window
from data import Utils
from sys import argv
# import cProfile

def main() :
    Pg.init()
    # game_type : bool = True
    # if len(argv) > 1 and argv[1].lower() == "-ia":
    #     game_type = True
    #     # print(argv[1])
    window : Window = Window((Utils.DEFAULT_WINDOW_WIDTH, Utils.DEFAULT_WINDOW_HEIGHT))
    window.main_loop()

if __name__ == '__main__' :
    # cProfile.run('main()', sort='tottime')
    main()