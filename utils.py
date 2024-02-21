from sys import argv
import models.Ia as ai
import chess as ch

def handle_command_line_arguments():
    playerWhite = None
    playerBlack = None
    if len(argv) > 2: # 2 AI's against each other
        if(argv[1].lower() == "random"):
            playerWhite = ai.Random(ch.WHITE)
        elif(argv[1].lower() == "minimax"):
            playerWhite = ai.Minimax(ch.WHITE)
        elif(argv[1].lower() == "neural"):
            playerWhite = ai.NeuronalNetwork(ch.WHITE)
        if(argv[2].lower() == "random"):
            playerBlack = ai.Random(ch.BLACK)
        elif(argv[2].lower() == "minimax"):
            playerBlack = ai.Minimax(ch.BLACK)
        elif(argv[2].lower() == "neural"):
            playerBlack = ai.NeuronalNetwork(ch.BLACK)
    elif len(argv) > 1: # Human VS Ai
        if(argv[1].lower() == "random"):
            playerBlack = ai.Random(ch.BLACK)
        elif(argv[1].lower() == "minimax"):
            playerBlack = ai.Minimax(ch.BLACK)
        elif(argv[1].lower() == "neural"):
            playerBlack = ai.NeuronalNetwork(ch.BLACK)
    return playerWhite, playerBlack