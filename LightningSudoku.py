# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 20:17:41 2020

@author: Max
"""

class Sudoku:
    
    def __init__(self, puzzle):
        
        time = __import__('time')
        self.i = 0
        
	# Used for keys to identify cells
        self.digits = '123456789'
        self.rows = 'ABCDEFGHI'
        self.cols = self.digits
        
	# Cross product used generate grid keys
        self.cross = lambda A, B: [a+b for a in A for b in B]
        
	# list of all squares in grid
        self.squares = self.cross(self.rows, self.cols)
	
	# contains lists of all the grouped cells by row, col and sub-grid
        self.unitlist = ([self.cross(self.rows, c) for c in self.cols] +
                         [self.cross(r, self.cols) for r in self.rows] +
                         [self.cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                          for cs in ('123', '456', '789')])
    	
	# dictionary with cell as key and the associated cells apply constraint
        self.units = {s : [u for u in self.unitlist if s in u] 
                        for s in self.squares}
        
	# dictionary containg only those cells that apply constraints
        self.peers = {s : set(sum(self.units[s], [])) - set([s]) 
                        for s in self.squares}
        
	# used for timing
        print('\nInput:' + self.display(self.grid_values(puzzle)))
        start = time.time()
        solution_dict = self.solve(puzzle)
        
	# used for ouptuting string solution
        self.solution = ''
        for i in solution_dict.values():
            self.solution += i   
            
                
        print(self.solution)
        print()
        print('Output:' + self.display(solution_dict), end='\n')
        print()


        
        print('Solved in: %fs' % (time.time() - start))
        print('Solved in: %d steps' % self.i)
    
    # attempts to solve the puzzle
    def solve(self, puzzle):
        return self.search(self.parse_grid(puzzle))
    
    
    # using backtracking and propogation tray all possible values
    def search(self, values):
        
        if values is False:
            return False
        elif all(len(values[s]) == 1 for s in self.squares):
            return values
        
        n, s = min((len(values[s]), s) for s in self.squares if len(values[s]) > 1)
        return self.some(self.search(self.assign(values.copy(), s, d)) for d in values[s])
    
    # check to see if puzzle is solved
    def some(self, seq):

        for e in seq:         
            if e: return e
            
        return False
    
    # returns dict of grid values with cell name as key the values stored are 
    def grid_values(self, puzzle):
        return dict(zip(self.squares, puzzle))
        
    # returns a dict such that the values stored by cell name are those that
    # can be still placed in that cell    
    def parse_grid(self, puzzle):
        
        values = { s: self.digits for s in self.squares }
        
        for s, d in self.grid_values(puzzle).items():
            if d in self.digits and not self.assign(values, s, d):
                return False
            
        return values
            
    # updates incoming values by eliminating the other values than d from s        
    def assign(self, values, s, d):
        
        other_values = values[s].replace(d, '')

        if all(self.eliminate(values, s, d2) for d2 in other_values):
            return values
        else:
            return False
        
    # removes the given value d from the values of s. Follows two rules:
    #	1) If a square s is reduced to one value d2, then eliminate 
    #	2) If a unit u is reduced to only one place for a value d, then put it there.
    def eliminate (self, values, s, d):

        self.i +=1
        if d not in values[s]:
            return values # Already eliminated
        
        values[s] = values[s].replace(d, '')
        
	# rule 1
        if len(values[s]) == 0:
            return False # Contradiction: removed last value
        elif len(values[s]) == 1:
            d2 = values[s]
            
            if not all(self.eliminate(values, s2, d2) for s2 in self.peers[s]):
                return False 
        
	# rule 2    
        for u in self.units[s]:
            dplaces = [s for s in u if d in values[s]]
            
            if len(dplaces) == 0:
                return False ## Contradiction: no place for value
            elif len(dplaces) == 1:
                if not self.assign(values, dplaces[0], d):
                    return False
        
        return values
        
    # displays grid to terminal    
    def display(self, values):
        
        width = max(len(values[s]) for s in self.squares)
        line = '+'.join(['-'*(width*3*2+1)]*3)
        string = ''
        for r in self.rows:
            string += '\t' + ''.join(' '+values[r+c].center(width)+(' |' if c in '36' else '') for c in self.cols) + '\n'
            if r in 'CF': 
                string += '\t' + line + '\n'
        return string


