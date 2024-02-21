import pygame as Pg
from window import Window
from data import Utils
from utils import handle_command_line_arguments


def main() :
    Pg.init()
    
    playerWhite, playerBlack = handle_command_line_arguments()
    
    window : Window = Window((Utils.DEFAULT_WINDOW_WIDTH, Utils.DEFAULT_WINDOW_HEIGHT), playerWhite, playerBlack)
    window.main_loop()

if __name__ == '__main__' :
    main()