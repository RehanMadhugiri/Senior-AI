
import random
from time import time
from othello_strategy import Strategy
import Othello_Core as core

tic = time()
SILENT = False
ROUNDS = 10

s = Strategy()

#Make s1 and s2 equal to s.human(), s.random(), or s.ab_strategy(depth)

s1 = s.ab_strategy(3) #play against CPU
s2 = s.human() #manually input moves

def play(strategy_X, strategy_O, first, silent):


    #STRATEGY_X is s1
    #STRATEGY_O is s2

    board = s.initial_board()
    player = first
    current_strategy = {first: strategy_X, s.opponent(first): strategy_O}
    print(s.print_board(board))

    while s.any_legal_move(player, board):
        move = current_strategy[player](board, player)
        board = s.make_move(move, player, board)
        player = s.next_player(board, player)
        if not silent: print(s.print_board(board))
    print(s.print_board(board))
    return s.winner(board) # returns the score


def main():
    total_nodes = 0
    """
    Plays ROUNDS tic-tac-toe games and keeps a count of
    wins/ties. Uses strategies defined as global constants above.
    Selects a random starting player
    """
    j = []
    nps = 0.0
    for i in range(ROUNDS):
            t = time()
            game_result = play(s1, s2, first=random.choice([core.WHITE, core.WHITE]), silent=SILENT)

            j.append(game_result)
            print("Winner: ", game_result, "\n")
            t2 = time()
            total_nodes = s.get_nodes()
            nps += (total_nodes*1.0/(t2-t))


    print("\nResults\n" + "%4s %4s %4s" % ("o", "@", "-"))
    print("-" * 15)
    print("%4i %4i %4i" % (j.count(core.WHITE), j.count(core.BLACK), j.count("TIE")))
    toc = time()
    print("Time:", toc-tic, " seconds")
    print(nps/10.0)


if __name__ == "__main__":
    main()
