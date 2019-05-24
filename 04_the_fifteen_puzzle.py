"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods
    def move_zero(self, target_row, target_col):
        """
        Generates a move string that moves zero tile
        to specified position, going up/down first then right/left
        """
        pos = self.current_position(0, 0)
        move = ""
        move_row = target_row - pos[0]
        move_col = target_col - pos[1]
        if move_row < 0: # moving up
            move += 'u' * abs(move_row)
        if move_col < 0: # moving left
            move += 'l' * abs(move_col)
        if move_row > 0: # moving down
            move += 'd' * move_row
        if move_col > 0: # moving right
            move += 'r' * move_col
        #self.update_puzzle(move)
        return move
    
    def move_to_zero(self, target_row, target_col):
        """
        Generates a move string that moves a tile that should be
        at target coordinates to the current position of zero tile
        then moves zero tile to the left
        """
        zero_pos = self.current_position(0, 0)
        tile_pos = self.current_position(target_row, target_col)
        #print "tile_pos:", tile_pos
        move_zero = self.move_zero(tile_pos[0], tile_pos[1])
        move = ""
        if zero_pos[1] == tile_pos[1]: # up
            move = 'lddru' * (zero_pos[0] - tile_pos[0] - 1) + 'ld' # moving down
        elif zero_pos[0] == tile_pos[0]: # same row
            if zero_pos[1] < tile_pos[1]: # right
                move = 'ulldr' * (tile_pos[1] - zero_pos[1] - 1) + 'ulld' # moving left
            elif zero_pos[1] > tile_pos[1]: # left
                move = 'urrdl' * (zero_pos[1] - tile_pos[1] - 1) # moving right
        else:
            vert_first, vert_back = 'u', 'd'
            if tile_pos[0] == 0:
                vert_first, vert_back = 'd', 'u'
            if zero_pos[1] < tile_pos[1]: # up right
                 move = (vert_first + 'll' + vert_back + 'r')\
                * (tile_pos[1] - zero_pos[1] - 1)\
                + ('dlu' if tile_pos[0] == 0 else 'ullddru') # moving left
            elif zero_pos[1] > tile_pos[1]: # up left
                move = 'drrul' * (zero_pos[1] - tile_pos[1] - 1) + 'dru' # moving right
            move += 'lddru' * (zero_pos[0] - tile_pos[0] - 1) + 'ld' # moving down
        return move_zero + move

    def _lower_row_invariant_nozero(self, target_row, target_col):
        """
        Helper invariant method, checks conditions in lower_row_invariant
        except zero position
        """
        for col in range(target_col + 1, self._width):
            if self._grid[target_row][col] != col + self._width * target_row:
                return False
        for row in range(target_row + 1, self._height):
            for col in range(0, self._width):
                if self._grid[row][col] != col + self._width * row:
                    return False
        return True
                
    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        #print self._grid[target_row][target_col] == 0
        #print self._lower_row_invariant_nozero(target_row, target_col)
        return self._grid[target_row][target_col] == 0 and \
               self._lower_row_invariant_nozero(target_row, target_col)

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        #print "Calling lower_row_invariant(" + str(target_row) + ", " + str(target_col) + ")"
        assert self.lower_row_invariant(target_row, target_col)
        move = self.move_to_zero(target_row, target_col)
        self.update_puzzle(move)
        return move

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        tile_pos = self.current_position(target_row, 0)
        solution, prefix = "", ""
        if tile_pos[1] == 0 and tile_pos[0] == target_row - 1: # tile is just one square up
            solution = 'u' + 'r' * (self._width - 1)
        else: # tile is somewhere else
            prefix = 'ur'
            self.update_puzzle(prefix)
            solution = self.move_to_zero(target_row, 0)
            solution += "ruldrdlurdluurddlu" + 'r' * (self._width - 1)
        self.update_puzzle(solution)
        return prefix + solution

    #############################################################
    # Phase two methods
    def _upper_row_invariant_nozero(self, target_col):
        """
        Helper invariant method, checks columns to the right
        for upper (row < 2) invariants
        """
        for row in range(0, 2):
            for col in range(target_col + 1, self._width):
                if self._grid[row][col] != col + self._width * row:
                    return False
        return True
        
    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        return self._grid[0][target_col] == 0 and \
               self._grid[1][target_col] == target_col + self._width and \
               self._upper_row_invariant_nozero(target_col) and \
               self._lower_row_invariant_nozero(1, self._width - 1)

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        return self._grid[1][target_col] == 0 and \
               self._upper_row_invariant_nozero(target_col) and \
               self._lower_row_invariant_nozero(1, self._width - 1)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        tile_pos = self.current_position(0, target_col)
        solution, prefix = "", ""
        if tile_pos[0] == 0 and tile_pos[1] == target_col - 1:
            solution = 'ld'
        else:
            prefix = 'ld'
            self.update_puzzle(prefix)
            solution = self.move_to_zero(0, target_col)
            # urdl urrd luld rruld
            solution += "urdlurrdluldrruld"
        self.update_puzzle(solution)
        return prefix + solution

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        move = self.move_to_zero(1, target_col) + 'ur'
        self.update_puzzle(move)
        return move

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        solution = ""
        if self._grid[1][0] == 1 + self._width: # left
            solution = 'lu'
        elif self._grid[0][1] == 1 + self._width: # up
            solution = 'ul'
        else:
            solution = 'lurdlu'
        self.update_puzzle(solution)
        return solution

    def _is_solved(self):
        """
        Checks if a part of the puzzle is already solved
        Returns first unsolved position in (row, col) format
        """
        for row in range(self._height - 1, -1, -1):
            for col in range(self._width - 1, -1, -1):
                if self._grid[row][col] != col + row * self._width:
                    return row, col
        return 0, 0
        
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        #zero_pos = self.current_position(0, 0)
        move_zero, solution = "", ""
        starting_row, starting_col = self._is_solved()
        #print starting_row, starting_col

        if starting_row == 0 and starting_col == 0:
            #print "already solved"
            return ""
        move_zero = self.move_zero(starting_row, starting_col)
        self.update_puzzle(move_zero)
        if starting_row > 1: # phase 1
            #print "phase 1"
            #print self
            if starting_col < self._width - 1:
                for col in range(starting_col, 0, -1):
                    solution += self.solve_interior_tile(starting_row, col)
                solution += self.solve_col0_tile(starting_row)
                starting_row -= 1
                starting_col = self._width - 1
            for row in range(starting_row, 1, -1):
                for col in range(starting_col, 0, -1):
                    #print self
                    #print "Calling solve_interior_tile(" + str(row), ", " + str(col) + ")"
                    solution += self.solve_interior_tile(row, col)
                #print "Calling solve_col0_tile(" + str(row) + ")"
                #print self
                solution += self.solve_col0_tile(row)
            starting_row, starting_col = 1, self._width - 1
        if starting_row < 2:
            if starting_col > 1: # phase 2
                #print "phase 2"
                #print "starting_row, starting_col: ", starting_row, starting_col
                #print self
                for col in range(starting_col, 1, -1): 
                    solution += self.solve_row1_tile(col)
                    solution += self.solve_row0_tile(col)
                starting_col = 1
            if starting_col < 2: # phase 3
                #print "phase 3"
                #print self
                solution += self.solve_2x2()
        return move_zero + solution

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(5, 6))

def create_grid(width, height):
    """
    Creates a 15-puzzle style grid
    """
    return [[col + width * row for col in range(width)]
                               for row in range(height)]

def test_puzzle():
    """
    Helper function for testing Puzzle objects
    """
    p2x4 = Puzzle(2, 4, [[0, 3, 2, 7], [4, 5, 6, 1]])
    print p2x4
    print p2x4.solve_puzzle()
    print p2x4
    grid = [[3, 2], [1, 0]]
    p2x2 = Puzzle(2, 2, grid)
    p2x2.update_puzzle('lurd')
    print " --- Testing 2x2 --- "
    print p2x2
    print p2x2.solve_puzzle()
    print p2x2
    print " --- Testing 3x3 --- "
    p3x3 = Puzzle(3, 3)
    p3x3.update_puzzle('rdrdlluurrddlulu')
    print p3x3
    print p3x3.solve_puzzle()
    print p3x3
    print " --- Testing 4x4 --- "
    p4x4 = Puzzle(4, 4)
    p4x4.update_puzzle('rdrdrdllluuurrrdddlululu')
    print p4x4
    print p4x4.solve_puzzle()
    print p4x4
    print " --- Testing 4x5 --- "
    p4x5 = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
    print p4x5
    print p4x5.solve_puzzle()
    print p4x5

#test_puzzle()
