import othello_core as core
import random

weights = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 300, -300, 20, 5, 5, 20, -300, 300, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 300, -300, 20, 5, 5, 20, -3000, 300, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

dict = {}
global nodes

class Strategy(core.OthelloCore):

    def __init__(self):
        pass

    def is_valid(self, move):
        if move is None:
            return False
        return (move >= 11 and move < 89)

    def opponent(self, player):
        if player == core.BLACK:
            return core.WHITE
        elif player == core.WHITE:
            return core.BLACK

    def find_bracket(self, move, player, board, direction):
        current = move
        while self.is_valid(move) and self.is_valid(move + direction):
            current += direction
            if board[current] == core.OUTER:
                return None
            if board[current] == player:
                if board[current - direction] == player:
                    return None
                elif board[current - direction] == self.opponent(player):
                    return move

            if board[current] == core.EMPTY:
                return None

        return None

    def is_legal(self, move, player, board):
        if not self.is_valid(move) or board[move] is not core.EMPTY:
            return False
        for i in range(8):
            direction = core.DIRECTIONS[i]
            if self.find_bracket(move, player, board, direction) is not None:
                return True
        return False


    def winner(self, board):
        blacks = 0
        whites = 0
        for space in board:
            if space == core.BLACK:
                blacks += 1
            elif space == core.WHITE:
                whites += 1

        if blacks > whites:
            return core.BLACK
        elif whites > blacks:
            return core.WHITE
        else:
            return "TIE"

    ######################### Making moves ##########################


    # When the player makes a move, we need to update the board and flip all the
    # bracketed pieces.


    def make_move(self, move, player, board):
        for i in range(8):
            direction = core.DIRECTIONS[i]
            if self.find_bracket(move, player, board, direction):
                board[move] = player
                self.make_flips(move, player, board, direction)

        return board

    def make_flips(self, move, player, board, direction):
        """Flip pieces in the given direction as a result of the move by player."""
        current = move + direction
        while board[current] == self.opponent(player):
            board[current] = player
            current = current + direction

    def legal_moves(self, player, board):
        moves = []
        indices = [i for i, x in enumerate(board) if x == player]

        for square in range(11,89):
            if self.is_legal(square, player, board):
                moves.append(square)

        random.shuffle(moves)
        return moves

    def any_legal_move(self, player, board):
        return len(self.legal_moves(player, board)) != 0

    def next_player(self,board, prev_player):
        next = self.opponent(prev_player)
        if self.any_legal_move(next, board):
            return next
        return None

    def score(self,player, board):
        pl = 0
        o = 0
        for i in range(11, 89):
            if board[i] == player:
                pl += weights[i]
            elif board[i] == self.opponent(player):
                o += weights[i]
        return pl - o



    ######################### Strategies #############################


    def human(self):
        def human_strat(board, player):
            moves_list = self.legal_moves(player, board)
            move = input("Where would you like to put a piece? Here are your options: %s " % moves_list)
            return int(move)
        return human_strat

    def random(self):
        def rand_strat(board, player):
            moves_list = self.legal_moves(player, board)
            move = random.choice(moves_list)
            return move
        return rand_strat

    def minimax(self, player, board, maxdepth):
        if player == core.WHITE: move = self.max_dfs(board, player, maxdepth, 0)[1]
        if player == core.BLACK: move = self.min_dfs(board, player, maxdepth, 0)[1]

        return move

    def max_dfs(self, board, player, maxdepth, current_d):
        global nodes
        if current_d == maxdepth:
            return self.score(core.WHITE, board), None
        v = -999999999
        move = -1
        for m in self.legal_moves(player, board):
            new_board = [i for i in board]
            self.make_move(m, player, new_board)
            board_str = "".join(board)
            if (board_str, player) in dict:
                new_value = dict[(board_str, player)]
            else:
                new_value = self.min_dfs(new_board, self.next_player(new_board, player), maxdepth, current_d + 1)[0]
                dict[(board_str, player)] = new_value

            if new_value > v:
                v = new_value
                move = m
        return v, move

    def min_dfs(self, board, player, maxdepth, current_d):
        if current_d == maxdepth:
            return self.score(core.BLACK, board), None
        v = 999999999
        move = -1
        for m in self.legal_moves(player, board):
            new_board = [i for i in board]
            self.make_move(m, player, new_board)
            board_str = "".join(board)
            if (board_str, player) in dict:
                new_value = dict[(board_str, player)]
            else:
                new_value = self.max_dfs(new_board, self.next_player(new_board, player), maxdepth, current_d + 1)[0]
                dict[(board_str, player)] = new_value

            if new_value < v:
                v = new_value
                move = m
        return v, move

    def minimax_strategy(self, max_depth):
        def strategy(board, player):
            return self.minimax(player, board, max_depth)

        return strategy

    ##################### ALPHA BETA STUFF #########################


    def best_strategy(self, board, player, best_move, still_running):
        depth = 1
        while still_running:
            best_move.value = self.ab_pruning(board, player, -9999999999, 9999999999, depth)
            depth += 1
            if depth == 6:
                break


    def ab_strategy(self, max_depth):
        def abstrategy(board, player):
            return self.ab_pruning(board, player, -9999999999, 9999999999, max_depth)
        return abstrategy

    def ab_pruning(self, board, player, a, b, depth):
        global nodes
        nodes = 0
        move = 0
        if player == core.WHITE: move = self.ab_max(board, player, a, b, depth)[1]
        if player == core.BLACK: move = self.ab_min(board, player, a, b, depth)[1]

        return move

    def get_nodes(self):
        return nodes

    def ab_max(self, board, player, alpha, beta, depth):
        global nodes
        nodes+=1
        if depth == 0:
            return self.score(core.WHITE, board), None
        if not self.any_legal_move(player, board) and not self.any_legal_move(self.opponent(player), board):
            return 9999999999, None
        v = -9999999999
        move = -1
        for m in self.legal_moves(player, board):
            new_board = [i for i in board]
            self.make_move(m, player, new_board)
            board_str = "".join(new_board)
            if (board_str, player) in dict:
                new_value = dict[(board_str, player)]
            else:
                new_value = self.ab_min(board, player, alpha, beta, depth-1)[0]
                dict[(board_str, player)] = new_value

            if new_value > v:
                v = new_value
                move = m
            if v >= beta:
                return v, move
            beta = min(beta, v)

        return v, move

    def ab_min(self, board, player, alpha, beta, depth):
        global nodes
        nodes+=1
        if depth == 0:
            return self.score(core.BLACK, board), None
        if not self.any_legal_move(player, board) and not self.any_legal_move(self.opponent(player), board):
            return -9999999999, None
        v = 9999999999
        move = -1
        for m in self.legal_moves(player, board):
            new_board = [i for i in board]
            self.make_move(m, player, new_board)
            board_str = "".join(new_board)
            if (board_str, player) in dict:
                new_value = dict[(board_str, player)]
            else:
                new_value = self.ab_max(board, player, alpha, beta, depth-1)[0]
                dict[(board_str, player)] = new_value
            if new_value < v:
                v = new_value
                move = m
            if v <= alpha:
                return v, move
            beta = min(beta, v)

        return v, move


class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)
