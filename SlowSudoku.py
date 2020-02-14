# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 09:18:20 2020

@author: Max
"""

class Sudoku:
   
   
    def __init__(self, puzzle):
       
        self.queue = __import__("queue")
        self.copy = __import__('copy')
        self.math = __import__("math") 
        self.time = __import__("time")
       
        self.i = 0

	# initiales variables
        self.puzzle = puzzle
        self.size = int(self.math.sqrt(len(puzzle)))
        self.domain = self.convert([i for i in range(1, self.size+1)])
        
        print()
        self.pretty_print(puzzle, "Input:")
       
	# gets list of all variables as a dict
        self.variables = self.get_variables(puzzle)
        start = self.time.time()
	
	# solves sudoku
        self.solve()
        end = self.time.time()
        print(self.i, self.puzzle)
        print()
        self.pretty_print(self.puzzle, "Output:")
        print('Solved in: %fs' % (end - start))
        print('Solved in: %d steps' % self.i)
       
   
    # used for printing grid to terminal
    def pretty_print(self, puzzle, msg):        
       
        print(msg, end='\t')
        print(puzzle[0:3]   + '|' + puzzle[3:6]   + '|' +   puzzle[6:9], end='\n\t')
        print(puzzle[9:12]  + '|' + puzzle[12:15] + '|' + puzzle[15:18], end='\n\t')
        print(puzzle[18:21] + '|' + puzzle[21:24] + '|' + puzzle[24:27], end='\n\t')
        print('-----------', end='\n\t')
        print(puzzle[27:30] + '|' + puzzle[30:33] + '|' + puzzle[33:36], end='\n\t')
        print(puzzle[36:39] + '|' + puzzle[39:42] + '|' + puzzle[42:45], end='\n\t')
        print(puzzle[45:48] + '|' + puzzle[48:51] + '|' + puzzle[51:54], end='\n\t')
        print('-----------', end='\n\t')
        print(puzzle[54:57] + '|' + puzzle[57:60] + '|' + puzzle[60:63], end='\n\t')
        print(puzzle[63:66] + '|' + puzzle[66:69] + '|' + puzzle[69:72], end='\n\t')
        print(puzzle[72:75] + '|' + puzzle[75:78] + '|' + puzzle[78:81], end='\n\t')
        print()
       
    # used to solve sudoku using baacktracking, heuristics and constraint propagation   
    def solve(self):
        # base case, no more variables can be assigned thus puzzle must be solved       
        if self.variables == {}:
            return self.puzzle

	# gets next node based on hueristics
        node = min(self.calculate_hueristics(self.variables))[-1]

        print(self.i, self.puzzle, end='\r')
        for n in node[-1]:

            # appends string and recursivly tries next value
            self.append_to_puzzle(n , node)
            self.puzzle = self.solve()
            
            # if all variables are assigned then puzzle is complete break loop and return
            if '.' not in self.puzzle:
                break
            
            # if value entered fails then remove the value from the string
            self.remove_from_puzzle(n, node)
           
        return self.puzzle
    
    # appends to puzzle string and updates variables
    def append_to_puzzle(self, n, node):
        
        self.i += 1
        self.puzzle = self.replace(self.puzzle, n, node[0])
        self.variables = self.get_variables(self.puzzle)
        
    # removes from puzzle and updates variable list
    def remove_from_puzzle(self, n, node):
        
        self.puzzle =  self.replace(self.puzzle, '.', node[0])           
        self.variables = self.get_variables(self.puzzle)        
        
    # replaces chars in string       
    def replace(self, string, char, index):
       
        if index == 0:
            return char + string[index+1:]
        else:
            return string[:index] + char + string[index+1:]
       
    # used to calculate hueristics.   
	#Most constrained = least no of values
	#Most constraining = most number of empty spaces
	#Least constraining value = least number of occurences of value in conflicting cells
    def calculate_hueristics(self, variables):
        
        return [(self.most_constrained_vars(k, variables),
                (k , variables[k]))
                #self.most_constraining_vars(k, variables),
                #(k, self.least_constraining_val(k, variables)))
                for k, v in variables.items()]
   
    # gets a list of all the indexst assocated with a cell
    def get_all_indexes(self, i, variables):
       
        row = set(self.get_row(i, i=True))
        col = set(self.get_col(i, i=True))
        grid = set(self.get_grid(i, i=True))
       
        for i in col: row.add(i)
        for i in grid: row.add(i)
       
        return [i for i in row if i in variables.keys()]
   
    # calculates least constraining value hueristic
    def least_constraining_val(self, i, variables):
       
        s = variables[i]
        affected = self.get_all_indexes(i, variables)                
       
        nums = {n : sum([1 for m in affected if n in variables[m]]) for n in s}
                                           
        sort = self.queue.PriorityQueue()      
        [sort.put((v, k)) for k, v in nums.items()]
                       
        return ''.join([sort.get()[-1] for i in range(len(nums))])
       
    # calculates most constrained variable hueristic
    def most_constrained_vars(self, i, variables):
       
        return len(variables[i])
   
    # calculates most constraining variable hueristic
    def most_constraining_vars(self, i, variables):
       
        affected = self.get_all_indexes(i, variables)      
        indexes = variables.keys()  
       
        return len([i for i in affected if i in indexes])
       
    # returns a dictionary with available values for insertion at each index   
    def get_variables(self, puzzle):
       
        return {k: self.get_remaining(k) for k in range(len(puzzle))
                if puzzle[k] == '.'}
       
    # gets the remaining values that can be used in a variable
    def get_remaining(self, pos):
       
        row = self.convert(self.get_row(pos))
        col = self.convert(self.get_col(pos))
        grid = self.convert(self.get_grid(pos))
       
        return ''.join(sorted(set(self.domain) -
                              set(''.join([row, col, grid]).replace('.',''))))
       
    # converts a list to a string    
    def convert(self, x):
       
        return ''.join(map(str, x))
       
    # gets values at row accosisated to varaible   
    def get_row(self, pos, i=False):
       
        n = self.size
        t0, t1 = 0, 0 + n
        while t0 < n**2:
            if t0 <= pos and pos < t1:
                if i: return [i for i in range(t0, t1)]    
                else: return [self.puzzle[i] for i in range(t0, t1)]
            else:
                t0, t1 = t0 + n, t1 + n
                               
    # gets values at col accosisated to varaible              
    def get_col (self, pos, i=False):
       
        n = self.size
       
        if i: return [i for i in range(n**2) if i % n == pos % n]
        else: return [self.puzzle[i] for i in range(n**2) if i % n == pos % n]
   
    # get svalues at sub-grid accosisated to varaible                  
    def get_grid(self, pos, i=False):
       
        n = int(self.size)
        m = int(self.math.sqrt(n))
       
        t = self.math.floor(self.get_col(pos, i=True)[0] / m)
        s = self.math.floor(pos/n)
        s -= s % m
       
        pred = lambda i, j : j*n + m*t <= i < j*n + (1+t)*m
       
        if i: return [i for i in range(n**2)
                        if any([pred(i, j) for j in range(s,s+m)])]
       
        else: return [self.puzzle[i] for i in range(n**2)
                        if any([pred(i, j) for j in range(s,s+m)])]
       
       

if __name__ == '__main__':           
	init = ".34.4..21..3.21."
	init = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
	init = "1..489..673.....4......1295..712.6..5..7.3..8..6.957..9146......2.....378..512..4"
	init = ".2.6.8...58...97......4....37....5..6.......4..8....13....2......98...36...3.6.9."
	init = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..' # worlds hardest sudoku?

	print(init)
	i = 3
	sudoku = Sudoku(init)
	#print()
	#[print(t) for t in [sudoku.get_row(i) for i in range(0, 9*9, 9)]]
	#print()
	#[print(sudoku.convert(t)) for t in [sudoku.get_row(i) for i in range(0, 9*9, 9)]]
	#print()    


    
