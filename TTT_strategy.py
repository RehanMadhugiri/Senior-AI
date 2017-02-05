import random as rand
from core import *

player = "X"
current_d = 0
DICTIONARY = {}


def terminal_test(board):
    if terminal_X(board): return "X"
    if terminal_O(board): return "O"
    elif not "." in board: return "TIE"


def terminal_X(b):
    board = list(b)
    if board[0] == board[1] == board[2] == "X": return True
    elif board[0] == board[3] == board[6] == "X": return True
    elif board[0] == board[4] == board[8] == "X": return True
    elif board[2] == board[4] == board[6] == "X": return True
    elif board[1] == board[4] == board[7] == "X": return True
    elif board[2] == board[5] == board[8] == "X": return True
    elif board[3] == board[4] == board[5] == "X": return True
    elif board[6] == board[7] == board[8] == "X": return True

    return False


def terminal_O(b):
    board = list(b)
    if board[0] == board[1] == board[2] == "O": return True
    elif board[0] == board[3] == board[6] == "O": return True
    elif board[0] == board[4] == board[8] == "O": return True
    elif board[2] == board[4] == board[6] == "O": return True
    elif board[1] == board[4] == board[7] == "O": return True
    elif board[2] == board[5] == board[8] == "O": return True
    elif board[3] == board[4] == board[5] == "O": return True
    elif board[6] == board[7] == board[8] == "O": return True

    return False

def terminal_value(board):
    if terminal_X(board): return 1
    if terminal_O(board): return -1
    elif "." not in board: return 0


def human(board, player):
    index = input("What index for " + player + ": ")
    return int(index)


def random(board, player):
    index = rand.choice(open_values(board))
    return index


def minimax_strategy(max_depth):
    def strategy(board, player):
        return minimax(board, player, max_depth)

    return strategy


def minimax(board, player, maxdepth):
    if player == "X": move = max_dfs(board, player, maxdepth, current_d)[1]
    if player == "O": move = min_dfs(board, player, maxdepth, current_d)[1]

    return move


def max_dfs(board, player, maxdepth, current_d):
    if terminal_test(board):
        return terminal_value(board), None
    v = -999999999
    move = -1
    for m in open_values(board):
        new_board = assign(board, m, player)
        if (new_board, player) in DICTIONARY:
            new_value = DICTIONARY[(new_board, player)]
        else:
            new_value = min_dfs(assign(board, m, player), next_player(board, player),
                                maxdepth, current_d + 1)[0]
            DICTIONARY[(new_board, player)] = new_value

        if new_value > v:
            v = new_value
            move = m
    return v, move


def min_dfs(board, player, maxdepth, current_d):
    if terminal_test(board):
        return terminal_value(board), None
    v = 999999999
    move = -1
    for m in open_values(board):
        new_board = assign(board, m, player)
        if (new_board, player) in DICTIONARY:
            new_value = DICTIONARY[(new_board, player)]
        else:
            new_value = max_dfs(assign(board, m, player), next_player(board, player),
                            maxdepth, current_d + 1)[0]
            DICTIONARY[(new_board, player)] = new_value
        if new_value < v:
            v = new_value
            move = m
    return v, move


def open_values(board):
    if all(p == '.' for p in board):
        return([0, 1, 4])

    open = []
    b = list(board)
    for i in range(9):
        if b[i] == ".":
            open.append(i)

    return open


def assign(board, m, player):
    if m in open_values(board):
        l = list(board)
        l[m] = player
        board = "".join(l)
    return board


def eval(board):
    return 0
    # 3x1 + x2 - 3o2 - o
