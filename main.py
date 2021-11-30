# Yige Sun
# CS131-Artificial Intelligence
# Assignment4 CSP
# Two method are allowed, to use different method, changed the value of ALGORITHM at line 171
# to use backtrack, ALGORITHM = BACKTRACK; to use conflict-directed back jump, ALGORITHM = SMARTJUMP
import numpy as np
import time

class CSP(object):
    def solver(self, sudoku):
        coords = []
        for x in range(0, 9):
            for y in range(0, 9):
                if sudoku.puzzle[x][y] == 0:
                    coords.append((x, y))
        if ALGORITHM == "BACKTRACK":
            return self.backTrack(sudoku, sudoku.puzzle, coords)
        elif ALGORITHM == "SMARTJUMP":
            return self.smartJump(sudoku, sudoku.puzzle, coords)

    # Backtrack
    def backTrack(self, sudoku, puzzle, coords):
        if len(coords) == 0:
            return True, puzzle
        # Assign subsequent coords
        row_after, column_after = coords[0]
        coords_after = coords[1:]
        # recursive approach, updating puzzle board
        for x in range(1, 10):
            if sudoku.checkCoords(puzzle, row_after, column_after, x):
                puzzle[row_after, column_after] = x
                result, update_puzzle = self.backTrack(sudoku, puzzle.copy(), coords_after)
                if result:
                    return True, update_puzzle
                puzzle[row_after, column_after] = 0
        return False, puzzle

    # conflict-directed back jumping
    def smartJump(self, sudoku, puzzle, coords):
        if len(coords) == 0:
            return True, puzzle, set()
        # conflict set tracking new conflicting assignments + subsequent coords
        conflict_set = set()
        row_after, column_after = coords[0]
        coords_after = coords[1:]
        # observing board
        for x in range(1, 10):
            result = False
            update_puzzle = []
            # require set conflicts in conflict-driven backjump approach
            new_conflicts = set()
            if sudoku.checkCoords(puzzle, row_after, column_after, x):
                puzzle[row_after, column_after] = x
                result, update_puzzle, new_conflicts = self.smartJump(sudoku, puzzle.copy(), coords_after)
            else:
                new_conflicts = sudoku.checkConflicts(puzzle, row_after, column_after, x)
            # attempts to return immediately after conflict, may not have been
            # adjusted properly from general backjump pseudocode reference point
            if result:
                return True, update_puzzle, set()
            elif (row_after + (8 * column_after)) not in new_conflicts:
                return False, puzzle, new_conflicts
            else:
                new_conflicts.remove(row_after + (8 * column_after))
                conflict_set = conflict_set.union(new_conflicts)

            # return updated puzzle
            puzzle[row_after, column_after] = 0

        return False, puzzle, conflict_set

class Sudoku(object):

    # Initial vals
    def __init__(self, puzzle, approach):
        self.puzzle = puzzle
        self.approach = approach

    # Essentially calls the general solver in ConstraintSatisfaction Class
    def solver(self):
        coords = []
        for x in range(0, 9):
            for y in range(0, 9):
                if self.puzzle[x][y] == 0:
                    coords.append((x, y))
        return self.approach.solver(self)

    # ensures general line valid
    def checkLine(self, axis, index, puzzle):
        line = []
        if axis == 0:
            line = puzzle[index, :]
        elif axis == 1:
            line = puzzle[:, index]
        return is_valid

    # when called, ensures the 3x3 region is valid (used in all 9 of puzzle)
    def checkSubSquare(self, row, column, puzzle):
        line = []
        for x in range(0, 3):
            for y in range(0, 3):
                line.append(puzzle[(row + x), (column + y)])
        is_valid = self.checkLine(line)
        return is_valid

    # check if X or Y axis valid
    def checkAxis(self, puzzle, axis, axis_index, num):
        for x in range(0, 9):
            if axis == 0:
                if (puzzle[axis_index][x] == num):
                    return True
            elif axis == 1:
                if (puzzle[x][axis_index] == num):
                    return True
        return False

    # check if number already used
    def checkIfUsed(self, puzzle, row, column, num):
        for x in range(3):
            for y in range(3):
                if (puzzle[x + row][y + column] == num):
                    return True
        return False

    # confirm Puzzle has been solved or not
    def confirmFinish(self, puzzle):
        for x in range(0, 9):
            if not self.checkLine(0, x, puzzle):
                return False
            if not self.checkLine(1, x, puzzle):
                return False

            row = (int(x/3)) * 3
            column = (x%3) * 3
            if not self.checkSubSquare(row, column, puzzle):
                return False

        if (0 not in puzzle):
            return False

        return True

    #  X or Y Coords of Board validity
    def checkCoords(self, arr, row, column, num):
        return not self.checkIfUsed(arr, row - row % 3, column - column % 3, num) and \
               not self.checkAxis(arr, 0, row, num) and \
               not self.checkAxis(arr, 1, column, num)

    # check rows, then columns, for conflict set pairings
    def checkConflicts(self, puzzle, row, column, num):
        conflict_set = set()
        for x in range(9):
            if puzzle[row][x] == num:
                conflict_set.add((row + (x * 8)))
        for x in range(9):
            if puzzle[x][column] == num:
                conflict_set.add((x + (column * 8)))

        box_row = row - row % 3
        box_column = column - column % 3

        # Update lastest to conflict set after determination & return to
        # backjump in ConstraintSatisfaction Class
        for x in range(3):
            for y in range(3):
                if (puzzle[x + box_row][y + box_column] == num):
                    conflict_set.add(x + box_row + (8 * (y + box_column)))
        conflict_set.add(row + (8 * column))
        return conflict_set

# to use backtrack, ALGORITHM = BACKTRACK; to use conflict-directed back jump, ALGORITHM = SMARTJUMP
ALGORITHM = "BACKTRACK"

if __name__ == '__main__':
    puzzle1 = [
        [6, 0, 8, 7, 0, 2, 1, 0, 0],
        [4, 0, 0, 0, 1, 0, 0, 0, 2],
        [0, 2, 5, 4, 0, 0, 0, 0, 0],
        [7, 0, 1, 0, 8, 0, 4, 0, 5],
        [0, 8, 0, 0, 0, 0, 0, 7, 0],
        [5, 0, 9, 0, 6, 0, 3, 0, 1],
        [0, 0, 0, 0, 0, 6, 7, 5, 0],
        [2, 0, 0, 0, 9, 0, 0, 0, 8],
        [0, 0, 6, 8, 0, 5, 2, 0, 3]
    ]
    puzzle2 = [
        [0, 7, 0, 0, 4, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 6, 1, 0],
        [3, 9, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 4, 0, 0, 9],
        [0, 0, 3, 0, 0, 0, 7, 0, 0],
        [5, 0, 0, 1, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 7, 6],
        [0, 5, 4, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 1, 0, 0, 5, 0]
    ]
    print("*You are using " + ALGORITHM +" method now.*")
    startTime = time.time()
    print("Puzzle1:(0 denotes the open position need to be solved) ")
    print("Original Puzzle:\t\t\t\t Solution:")
    sudoku2 = Sudoku(np.array(puzzle1), CSP())
    solution2 = ((sudoku2.solver()[1:])[0]).tolist()
    for i in range(9):
        print(puzzle1[i],"\t", solution2[i])
    print("-------------------------------------------------------------")
    print("Puzzle2:(0 denotes the open position need to be solved) ")
    print("Original Puzzle:\t\t\t\t Solution:")
    sudoku2 = Sudoku(np.array(puzzle2), CSP())
    solution2 = ((sudoku2.solver()[1:])[0]).tolist()
    for i in range(9):
        print(puzzle1[i], "\t", solution2[i])
    endTime = time.time()
    timeSpent = endTime - startTime
    print(ALGORITHM + " needs " + str(timeSpent) + " seconds to solve these two puzzles.")