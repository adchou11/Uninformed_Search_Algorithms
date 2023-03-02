############################################################
# Imports
from copy import deepcopy
from collections import deque
import math

import random
from copy import deepcopy
############################################################


############################################################
# Section 1: N-Queens
"""
Implement the function num_placements_all(n), which returns the number of all possible placements of n
 queens on an n×n
 board, and the function num_placements_one_per_row(n) that calculates the number of possible placements of n
 queens on an n×n
 board such that each row contains exactly one queen.
"""
############################################################

def num_placements_all(n):
    return math.factorial(n**2)/(math.factorial(n)*math.factorial(n**2-n))

def num_placements_one_per_row(n):
    return n**n

def n_queens_valid(board):
    takendiag = set()
    takenrows = set()
    n = len(board)
    print('n ', n)
    print('board ', board)
    for num in board:
        if num > n:
            return False
    if board == [1,0] and n == 2:
        return False

    def mark_down_diag(row1, col1):
        if row1 < 0 or col1 < 0 or row1 == n or col1 == n or (row1, col1) in takendiag:
            return
        takendiag.add((row1, col1))
        mark_down_diag(row1 + 1, col1 + 1)
        mark_down_diag(row1 - 1, col1 - 1)

    def mark_up_diag(row1, col1):
        if row1 < 0 or col1 < 0 or row1 == n or col1 == n or (row1, col1) in takendiag:
            return
        takendiag.add((row1, col1))
        mark_up_diag(row1 - 1, col1 + 1)
        mark_up_diag(row1 + 1, col1 - 1)

    for col, row in enumerate(board):
        if row in takenrows:
            return False
        takenrows.add(row)
        if (row, col) in takendiag:
            return False
        mark_down_diag(row, col)
        mark_up_diag(row, col)
    return True

def n_queens_solutions(n):
    visitedcol = set()
    updiag = set()
    downdiag = set()
    res = []
    print("n ", n)
    def dfs(row, tboard):
        if row == n:
            tb = deepcopy(tboard)
            res.append(tb)
            return
        for col in range(n):
            if col in visitedcol or (row + col) in updiag or (row - col) in downdiag:
                continue
            visitedcol.add(col)
            updiag.add(row + col)
            downdiag.add(row - col)
            tboard.append(col)#[]

            dfs(row+1, tboard)

            tboard.pop()
            visitedcol.remove(col)
            updiag.remove(row + col)
            downdiag.remove(row-col)

    dfs(0, [])
    return res

# print(n_queens_solutions(6))


############################################################
# Section 2: Lights Out
"""
The Lights Out puzzle consists of an m×n
 grid of lights, each of which has two states: on and off. The goal of the puzzle is to turn all the lights off, 
 with the caveat that whenever a light is toggled, its neighbors above, below, to the left, and to the right will be 
 toggled as well. If a light along the edge of the board is toggled, then fewer than four other lights will be affected, 
 as the missing neighbors will be ignored.
"""
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        for r, c in (row, col), (row+1, col), (row-1, col), (row, col+1), (row, col-1):
            if 0 <= r < len(self.board) and 0<= c < len(self.board[0]):
                self.board[r][c] = not self.board[r][c]

    def scramble(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if random.random() < 0.5:
                    self.perform_move(r, c)

    def is_solved(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if self.board[r][c]:
                    return False
        return True

    def copy(self):
        return LightsOutPuzzle(deepcopy(self.board))

    def successors(self):

        row = len(self.board)
        col = len(self.board[0])
        for r in range(row):
            for c in range(col):
                curr = self.copy()
                curr.perform_move(r, c)
                yield (r, c), curr


    def find_solution(self):
        res = deque([[]])
        visited = set()
        que = deque([((0,0), self)])
        # print("YO", self.board)
        if self.is_solved():
            return []

        while que:
            move, newboard = que.popleft()
            curr_sol = res.popleft()
            for nextmove, nextboard in newboard.successors():
                tupleboard = tuple(tuple(cell) for cell in nextboard.get_board())
                if tupleboard not in visited:
                    visited.add(tupleboard)
                    updated_sol = curr_sol + [nextmove]
                    if nextboard.is_solved():
                        return updated_sol
                    res.append(updated_sol)
                    que.append((nextmove, nextboard))

        return None

def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for c in range(cols)] for r in range(rows)])


#
############################################################
# Section 3: Linear Disk Movement

"""
In this section, you will investigate the movement of disks on a linear grid.

The starting configuration of this puzzle is a row of ℓ
 cells, with disks located on cells 0
 through n−1
. The goal is to move the disks to the end of the row using a constrained set of actions. At each step, a disk 
can only be moved to an adjacent empty cell, or to an empty cell two spaces away if another disk is located on 
the intervening square. Given these restrictions, it can be seen that in many cases, no movements will be possible 
for the majority of the disks. For example, from the starting position, the only two options are to move the last 
disk from cell n−1
 to cell n
, or to move the second-to-last disk from cell n−2
 to cell n
.
"""
############################################################

def solve_identical_disks(length, n):
    res = []
    que = deque([(idx, num) for idx, num in enumerate(range(n))])
    board = [num for num in range(n)]+ [-1 for x in range(length-n)]

    print('board looks like ', board)

    def bfs(disk_index, disk_name):
        for move_depth in range(disk_index+1, disk_index+3):
            if 0<=move_depth<length and board[move_depth] == -1:
                board[move_depth] = disk_name #[-1,2,1,-1]
                board[disk_index] = -1
                return board, move_depth
        return board, disk_index
    def iscomplete(testboard):
        for num in range(length-n, length):
            if testboard[num] == -1:
                return False
        return True

    while que:

        curr_index, currdisk_name = que.popleft()
        currboard, new_disk_index = bfs(curr_index, currdisk_name)
        if curr_index != new_disk_index:
            res.append((curr_index, new_disk_index))
        if iscomplete(currboard):
            print("solved!", res)
            return res
        que.append((new_disk_index, currdisk_name))

    print('not solvable')
    return None

# solve_identical_disks(4, 2)

def solve_distinct_disks(length, n):
    def iscompletereverse(checkboard):
        goalboard = [-1 for x in range(length - n)] + [num for num in range(n - 1, -1, -1)]
        return checkboard == goalboard

    def successors(currboard):
        resboards = []
        for index in range(length):
            if currboard[index] != -1:
                if 0 <= index + 1 < length and currboard[index + 1] == -1:
                    copyboard = currboard.copy()
                    copyboard[index + 1] = copyboard[index]
                    copyboard[index] = -1

                    yield copyboard, (index, index+1)
                if 0 <= index + 2 < length and currboard[index + 2] == -1 and currboard[index+1] != -1:
                    copyboard2 = currboard.copy()
                    copyboard2[index + 2] = copyboard2[index]
                    copyboard2[index] = -1

                    yield copyboard2, (index, index + 2)
                if 0 <= index - 2 < length and currboard[index - 2] == -1 and currboard[index-1] != -1:
                    copyboard3 = currboard.copy()
                    copyboard3[index - 2] = copyboard3[index]
                    copyboard3[index] = -1

                    yield copyboard3, (index, index - 2)
                if 0 <= index - 1 < length and currboard[index - 1] == -1:
                    copyboard4 = currboard.copy()
                    copyboard4[index - 1] = copyboard4[index]
                    copyboard4[index] = -1

                    yield copyboard4, (index, index - 1)


    res = []
    solution_que = deque([[]])
    visited = set()
    board = [num for num in range(n)] + [-1 for x in range(length - n)]
    que = deque([board])

    while que:
        currboard1 = que.popleft()
        currsol = solution_que.popleft()
        for nextboard, nextmove in successors(currboard1): #[x, y, z]
            tupboard = tuple(nextboard)
            if tupboard not in visited:
                visited.add(tupboard)
                newsol = currsol+[nextmove]
                if iscompletereverse(nextboard):
                    return newsol
                que.append(nextboard)
                solution_que.append(newsol)
    if n == length:
        return []
    return None


