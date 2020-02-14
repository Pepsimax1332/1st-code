# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 09:18:20 2020

@author: Max
"""


class Sudoku:
   
   
    def __init__(self, puzzle):
        
        self.math = __import__('math')
        self.time = __import__('time')
        
	# initialises variables     
        self.i = 0

        self.puzzle = self.make_board(puzzle)
        self.size = int(self.math.sqrt(len(self.puzzle)))
        print()
        print("Input: ", end='')
        self.pretty_print(self.puzzle)
	
	# solves the puzzle and tracks time taken
        start = self.time.time()
        self.solve(self.puzzle)
        end = self.time.time() - start
        
	# prints the puzzle to screen
        print("\nOutput:", end='')
        self.pretty_print(self.puzzle)
        
        print()
        print("Solved in: %fs" % end)
        print("Solved in: %d steps" % self.i)

    #solves the puzzle using backtracking
    def solve(self, board):
             
        find = self.find_empty(board)
        
        if not find:
            return True
        else:
            row, col = find 
    
        for i in range(1,10):
            if self.valid(board, i, (row, col)):
                self.i += 1
    
                board[row][col] = i
                
                if self.solve(board):
                    return True

                board[row][col] = 0
    
        return False
    
    # makes the board into a 2d array given a string
    def make_board(self, s):
        w = int(self.math.sqrt(len(s)))
        return [[self.convert(s[i]) for i in range(j*w, (j+1)*w)] for j in range(w)]
        
    # converts the chars in input string into digits
    def convert(self, s):
        return 0 if s == '.' else int(s)
    
    # checks if number inserted is a valid number to be placed
    def valid(self, board, num, pos):
        
        n = self.size
        # Check row
        for i in range(len(board[0])):
            if (board[pos[0]][i] == num and pos[1] != i) or (
                    board[i][pos[1]] == num and pos[0] != i):
                return False
    
        # Check boardx
        boardx_x = int(pos[1] / self.size)
        boardx_y = int(pos[0] / self.size)
    
        for i in range(boardx_y*n, boardx_y*n + n):
            for j in range(boardx_x * n, boardx_x*n + n):
                if board[i][j] == num and (i,j) != pos:
                    return False
                
        return True
    
    
    # used for printing grid tp terminal
    def pretty_print(self, board):
        
        n = int(self.size)
        
        for i in range(len(board)):
            print('\t', end='')
            if i % self.size == 0 and i != 0: 
                print(''.join(['-'*n + ('' if j == n-1 else '+') for j in range(n)]), end='\n\t')
    
            for j in range(len(board[0])):
                
                if j % self.size == 0 and j != 0: 
                    print("|", end="")
                    
                if j == (len(board)-1): 
                    print(board[i][j])
                    
                else: 
                    print(board[i][j], end="")
    
    # change this to find best empty move and impliment heuristics    
    def find_empty(self, board):
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0: return (i, j)  # row, col
        return False      
       
if __name__ == '__main__':          
	init = ".34.4..21..3.21."
	init = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
	init = '.'*9**2 # empty sudoku


	init = "...26.7.168..7..9.19...45..82.1...4...46.29...5...3.28..93...74.4..5..367.3.18..." # easy
	init = "1..489..673.....4......1295..712.6..5..7.3..8..6.957..9146......2.....378..512..4" # easy
	init = '2..3.....8.4.62..3.138..2......2.39.5.7...621.32..6....2...914.6.125.8.0.....1..2' # intermediate
	init = ".2.6.8...58...97......4....37....5..6.......4..8....13....2......98...36...3.6.9." # hard
	init = '...6..4..7....36......91.8...........5.18...3...3.6.45.4.2...6.9.3.......2....1..' # hard++
	init = '.2..........6....3.74.8.........3..2.8..4..1.6..5.........1.78.5....9..........4.' # nightmare
	init = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..' # worlds 



	sudoku = Sudoku(init)

