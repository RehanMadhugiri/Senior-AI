# Name: Rehan Madhugiri
# Block: 5
# Email: 2017rmadhugi@tjhsst.edu


from time import time
import math
import heapq
from collections import deque
import random
from random import randrange
import copy

goalcount = 0
nodes = 0

class nQueens:
    def __init__(self, state=None, choices=None, n=8, parent=None, cursor = 0):
        #if the board is a child, give it the parent's state and choices. Otherwise, give it empty state and choices.
        global nodes
        nodes += 1
        if state is None:
            self.state = [[-1 for a in range(n)] for b in range(n)]
        else:
            self.state = state
        if choices is None:
            self.choices = [[set(range(1, n+1)) for x in range(n)] for j in range(n)]
        else:
            self.choices = choices
        self.n = n
        self.parent = None
        self.cursor = cursor

    def assign(self, col, row, value):
        if value not in self.choices[col][row]:
            self.choices[col][row] == -1
            return False

        if row // 3 == 0 and col // 3 == 0:
            for i in range(3):
                for x in range(3):
                    self.choices[i][x].discard(value)
        elif row // 3 == 0 and col // 3 == 1:
            for i in range(3):
                for x in range(3):
                    if (i + col < self.n):
                        self.choices[i + col][x].discard(value)
        elif row // 3 == 0 and col // 3 == 2:
            for i in range(3):
                for x in range(3):
                    if i + col < self.n:
                        self.choices[i + col][x].discard(value)
        elif row // 3 == 1 and col // 3 == 0:
            for i in range(3):
                for x in range(3):
                    if x + row < self.n:
                        self.choices[i][x + row].discard(value)
        elif row // 3 == 2 and col // 3 == 0:
            for i in range(3):
                for x in range(3):
                    if x + row < self.n:
                        self.choices[i][x + row].discard(value)
        elif row // 3 == 1 and col // 3 == 1:
            for i in range(3):
                for x in range(3):
                    if i + col < self.n and x + row < self.n:
                        self.choices[i + col][x + row].discard(value)
        elif row // 3 == 1 and col // 3 == 2:
            for i in range(3):
                for x in range(3):
                    if i + col < self.n and x + row < self.n:
                        self.choices[i + col][x + row].discard(value)
        elif row // 3 == 2 and col // 3 == 1:
            for i in range(3):
                for x in range(3):
                    if i + col < self.n and x + row < self.n:
                        self.choices[i + col][x + row].discard(value)
        elif row // 3 == 2 and col // 3 == 2:
            for i in range(3):
                for x in range(3):
                    if i + col < self.n and x + row < self.n:
                        self.choices[i + col][x + row].discard(value)

        for i in range(self.n):
            for x in range(self.n):
                if col == i or row == x:
                    self.choices[i][x].discard(value)


        self.cursor+=1
        self.state[col][row] = value
        self.choices[col][row].discard(value)
        self.choices[col][row] = set()
        print(self.choices)
        print(self)
        return True

    def goal_test(self):
        global goalcount
        goalcount = goalcount + 1
        numassigned = 0
        for i in range(self.n):
            for x in range(self.n):
                if self.state[i][x] != -1:
                    numassigned+=1
        return numassigned == (self.n * self.n)

    def get_next_unassigned_var(self):
        #return self.__getnext_LR()
        #return self.__getnext_most_constrained()
        for i in range(self.n):
            for x in range(self.n):
                if self.state[i][x] == -1:
                    return i, x

    def __getnext_LR(self):
        return self.cursor()

    def __getnext_most_constrained(self):
        cols = list(range(self.n))
        random.shuffle(cols)
        i_min = cols[0]
        for i in cols:
            if 0 < len(self.choices[i]) < len(self.choices[i_min]) or len(self.choices[i_min]) == 0:
                i_min = i
        return i_min

    def get_choices_for_var(self, col, row):
        return self.__sort_choices_by_constraints(col, row)

    def __sort_choices_by_constraints(self, col, row):
        l = list(self.choices[col][row])
        l.sort(key=lambda x: abs(x - self.n // 2))
        return l

    def __get_choices_LR(self, var):
        return list(self.choices[var])

    def consistency_test(self):
        for i in range(self.n):
            if self.state[i] == -1 and len(self.choices[i]) == 0:
                return False
        return True

    def __str__(self):
        s = ""
        for col in range(self.n):
            for row in range(self.n):
                if self.state[col][row] == -1:
                    s += "...|"
                else:
                    s = s + "%3s" % str(self.state[col][row]) + "|"
            s += "\n"

        return s

def dfs_recursive(state: nQueens, start_state, count = 0):
    if count > state.n * 3: state, count = start_state, 1
    if state.goal_test():
        return state, count+1
    if not state.consistency_test(): return None, count+1
    c, r = state.get_next_unassigned_var()
    for val in state.get_choices_for_var(c, r):
        child = nQueens(state=list(state.state),
                        choices=copy.deepcopy(state.choices),
                        parent = state,
                        cursor = state.cursor,
                        n = state.n)

        if child.assign(c, r, val):
            result, subcount = dfs_recursive(child, start_state, count)
            count = subcount
            if result is not None: return result, count+1
    return None, count+1


###--------------------------------------------------------------------------------------------------------

def generate_tests(start, end, skip):
    global goalcount
    global nodes


    out = open("results.txt", "a")
    print("*"*80, file=out)
    header = "DFS with restart"
    title_string = "%4s %10s %10s %8s %8s" % ("n", "goals", "nodes", "time", "goals/sec")
    print(header, file=out)
    print(title_string, file = out)

    #for size in range(start, end, skip):
    goalcount = 0
    nodes = 0
    n = nQueens(n=9)
    n.assign(0, 0, 6)
    n.assign(0, 2, 2)
    n.assign(0, 4, 5)
    n.assign(1, 5, 4)
    n.assign(1, 7, 3)
    n.assign(3, 0, 4)
    n.assign(3, 1, 3)
    n.assign(3, 5, 8)
    n.assign(4, 1, 1)
    n.assign(4, 6, 2)
    n.assign(5, 6, 7)
    n.assign(6, 0, 5)
    n.assign(6, 3, 2)
    n.assign(6, 4, 7)
    n.assign(7, 7, 8)
    n.assign(7, 8, 1)
    n.assign(8, 3, 6)
    fringe = []
    fringe.append(n)
    while True:
        if len(fringe) == 0:
            print("FAIL")
            return None
        node = fringe.pop()
        if node.goal_test():
            print(node)
            return True
        col, row = node.get_next_unassigned_var()
        for val in node.get_choices_for_var(col, row):
            child = nQueens(state=list(node.state), choices=copy.deepcopy(node.choices), parent=node, cursor=node.cursor, n=9)
            child.assign(col, row, val)
            fringe.append(child)

    '''start_time = time()
    sol, count = dfs_recursive(n, n)
    print(sol)
    t = time() - start_time
    data_line = "%4d %10d %10d %8.3f %8.0f" % (size, goalcount, nodes, t, goalcount / t)
    print(data_line, file=out)'''

    #out.close()

generate_tests(9, 10, 1)
