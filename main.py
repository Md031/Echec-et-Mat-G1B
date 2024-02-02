import pygame as Pg
from Window import Window
from Data import Utils

def main() :
    window : Window = Window((Utils.DEFAULT_BOARD_DIMENSIONS, Utils.DEFAULT_BOARD_DIMENSIONS))
    window.main_loop()

if __name__ == '__main__' :
    main()