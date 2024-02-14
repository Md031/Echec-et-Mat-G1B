import chess

class Human:
    
    def __init__(self) -> None:
        self.color = None
    
    def get_move(self, prompt):
        uci = input(prompt)
        if uci and uci[0] == "q":
            raise KeyboardInterrupt()
        try:
            chess.Move.from_uci(uci)
        except:
            uci = None
        return uci

    def set_color(self, color):
        self.color = color

    def move(self, board):
        legal_uci_moves = [move.uci() for move in board.legal_moves]

        uci = self.get_move("Coups légaux: " + (",".join(sorted(legal_uci_moves))) + "\n\nJouez un coup [q pour quitter]>")
        while uci not in legal_uci_moves:
            uci = self.get_move("Coups légaux: " + (",".join(sorted(legal_uci_moves))) + "\n\nJouez un coup [q pour quitter]>")
        return uci