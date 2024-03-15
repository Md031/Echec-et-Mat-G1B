from sys import argv
import models.Ia as ai
import chess as ch

def create_ai(ai_name : str, color : bool) -> None :
    tokens : list[str] = ai_name.split("-")
    player : ai = None 
    if tokens[0].lower() == "random" :
        player = ai.Random(color)
    elif tokens[0].lower() == "minimax" :
        player = ai.Minimax(color, int(tokens[1]))
    elif tokens[0].lower() == "neural" :
        player = ai.NeuronalNetwork(color)
    return player

def handle_command_line_arguments():
    playerWhite = None
    playerBlack = None
    print(len(argv))
    if len(argv) == 3 : # 2 AI's against each other
        playerWhite = create_ai(argv[1], ch.WHITE)
        playerBlack = create_ai(argv[2], ch.BLACK)
    elif len(argv) == 2 : # Human VS Ai
        playerBlack = create_ai(argv[1], ch.BLACK)

    # if len(argv) > 2: # 2 AI's against each other
    #     if(argv[1].lower() == "random"):
    #         playerWhite = ai.Random(ch.WHITE)
    #     elif(argv[1].lower() == "minimax"):
    #         playerWhite = ai.Minimax(ch.WHITE)
    #     elif(argv[1].lower() == "neural"):
    #         playerWhite = ai.NeuronalNetwork(ch.WHITE)
    #     if(argv[2].lower() == "random"):
    #         playerBlack = ai.Random(ch.BLACK)
    #     elif(argv[2].lower() == "minimax"):
    #         playerBlack = ai.Minimax(ch.BLACK)
    #     elif(argv[2].lower() == "neural"):
    #         playerBlack = ai.NeuronalNetwork(ch.BLACK)
    # elif len(argv) > 1: # Human VS Ai
    #     if(argv[1].lower() == "random"):
    #         playerBlack = ai.Random(ch.BLACK)
    #     elif(argv[1].lower() == "minimax"):
    #         playerBlack = ai.Minimax(ch.BLACK)
    #     elif(argv[1].lower() == "neural"):
    #         playerBlack = ai.NeuronalNetwork(ch.BLACK)
    return playerWhite, playerBlack