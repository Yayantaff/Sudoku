# cd /Volumes/General/AI/Project4/driver.py
# python problem3.py input3.csv
# python driver.py 003020600900305001001806400008102900700000008006708200002609500800203009005010300

import sys
import matplotlib.pyplot as plt
import numpy as np
import collections
from sets import Set

from copy import deepcopy


class Solver:
    
    def __init__(self):
        return
        
    def combine(self, rows, columns):
        "Combining files and columns"
        return [r + c for r in rows for c in columns]

    def solve(self):    
        
        '''
        grid : [a1 a2 a3 a4 a5 a6 a7 a8 a9 b1 b2 b3 ....]
        
        4 . . |. . . |8 . 5 
        . 3 . |. . . |. . . 
        . . . |7 . . |. . . 
        ------+------+------
        . 2 . |. . . |. 6 . 
        . . . |. 8 . |4 . . 
        . . . |. 1 . |. . . 
        ------+------+------
        . . . |6 . 3 |. 7 . 
        5 . . |2 . . |. . . 
        1 . 4 |. . . |. . .
        '''
        
        
        
        
        
        rows     = 'ABCDEFGHI'
        columns     = '123456789'
        
        #grid(list) : list of all squares 
        grid  = self.combine(rows, columns)
        
        #unitlist(list) : list of all files, columns and boxes
        unitlist = ([self.combine(rows, col) for col in columns] +
                    [self.combine(row, columns) for row in rows] +
                    [self.combine(rws, clmns) for rws in ('ABC','DEF','GHI') for clmns in ('123','456','789')])
        
        #units(dict) , sq : [sq belongs to [row][column][box]]          
        units = dict((s, [u for u in unitlist if s in u]) for s in grid)
        
        #peers(dict) , sq : set([list of all squares affected by the current square sq] ) 
        peers = dict((s, set(sum(units[s],[]))-set([s])) for s in grid)
        
        #values(dict) , sq : value
        values = self.grid_values(grid)
        
        #assignment = {}
        
        domain = self.domain_values(values, peers)
        
        #consistency = self.ac_3(values, domain, peers) # returns a 3-tuple if consistent, else False
        
        #if consistency:
            #consistency , inference , domain = consistency
            
        assignment = self.backtracking_search(values, domain, peers)
        values_string = ''
        #print assignment
        if assignment:
            for item in grid:
                values_string += assignment[item]
                #values_string +=.append(assignment[item])
        #print values_string
        
        f= open("output.txt","a")
        f.write(values_string+'\n')
        f.close()
        #print 'domain main'
        #print inference
        #print domain
        #print consistency
        #print inference
        return values
       
        
        
    def grid_values(self, grid):
        
        "Convert grid into a dict of {square: value}"
        chars = [c for c in sys.argv[1]]
        #assert len(chars) == 81
        return dict(zip(grid, chars))
    
    def domain_values(self, values, peers):
        
        "Convert grid into a dict of {square: domain_values}"
        domain = {}
        digits = '123456789'
        for s,d in values.items():
            if not str(d) in digits:
                temp_domain = digits
                for item in peers[s]:
                    if str(values[item]) in digits:
                       temp_domain = temp_domain.replace(values[item], '') 
                       
                domain[s] = temp_domain
                #print s,domain[s]
        return domain
                
    def ac_3(self, values,  domain, peers):
        
        queue_blank_squares = Set()
        domain_cc = dict(domain)#.deepcopy()
        digits = '123456789'
        for s,d in values.items():
            if not str(d) in digits:
                for p in peers[s]:
                    if not str(values[p]) in digits:
                        queue_blank_squares.add((s,p))
                        #print s, p
                #queue_blank_squares.add(s) 
        #print domain_cc 
        #print values['C3']
        #print '----'      
        
        while queue_blank_squares:
            
            current_pair = queue_blank_squares.pop()
            
            a = current_pair[0]
            b = current_pair[1]
            
            a_d = domain_cc[a]
            b_d = domain_cc[b]
            
            #print '@@@'
            #print domain_cc[a]
            revised = self.revise(current_pair, domain_cc)
            #print 'current pair'
            #print current_pair
            if revised:
                #print 'len(domain_cc[a])'
                #print 'domain of B3 is'
                #print domain_cc['B3']
                #print domain_cc['C2']
                
                
                #print b,values[b]
                #print a, len(domain_cc[a]), domain_cc[a]
                #print b, len(domain_cc[b]), domain_cc[b]
                #domain_cc[a] = new_domain_a
                if len(domain_cc[a]) == 0:
                    #print 'The domain is 0 here'
                    return False
                #print domain_cc[a]
                #print '---'
                    
                for p in peers[a]:
                    if not str(values[p]) in digits and not p == b:
                        queue_blank_squares.add((a,p))
                        #print '-----'
                        #print a, p 
                        #print '#####'
                        #print a,p
        #print domain_cc
        
        inference = {}
        for s, d in domain_cc.items():
            
            #print s, domain_cc[s]
            
            if len(d) == 1:
                inference[s] = domain_cc[s]
        
        #print 'inference'
        #print inference
        #print '-cc-'
        #print domain_cc   
        
        #print '--' 
        #domain = {}
        #domain = domain_cc
        #for s,d in domain.items():
            #print 'del'
            #print s, d
            #del domain[s]
        #print 'domain ac3---'
        
        #print '--'   
        return True, inference , domain_cc
                    
                
            
                
    def revise(self, pair, domain_cc):
        
        
        revised = False
        #print '--'
        #print pair[0]
        
        a = pair[0]
        b = pair[1]
        
        a_d = domain_cc[a]
        b_d = domain_cc[b]
        
        #print 'Revised'
        #print 'a_d'
        #print a
        #print a_d
        #print 'b_d'
        #print b
        #print b_d
        
        if len(b_d) == 1:
            for x in a_d:
                if b_d == x:
                    domain_cc[a] = domain_cc[a].replace(x,'') # a_d holds a copy of domain_cc[a] string only, not a reference
                    revised = True
                    
        elif len(a_d) == 1:
            for x in b_d:
                if a_d == x:
                    domain_cc[b] = domain_cc[b].replace(x,'') # a_d holds a copy of domain_cc[a] string only, not a reference
                    revised = True
                    
        return revised 
        
        
    
    
    def backtracking_search(self,values, domain, peers) :
        
        '''Entry point to backtracking, returns assignment'''
        
        assignment = {}
        digits = '123456789'
        assignment = self.backtrack(assignment, values, domain, peers)
        #print assignment
        #print 'the assignment is '
        #print assignment
        if assignment:
            for s,d in values.items():
                if not str(d) in digits:
               
                   values[s] = assignment[s] 
        
        #print values
        return values
        #return assignment
        
    def backtrack(self, assignment, values, domain, peers):
        
        '''self recursive, finds the assignment'''
        
        if not domain:
            #for s,d in values.items():
            #   print s,d
            
            #print len(values)
            return assignment
        
        
        _mrv = []
        min = 9
        for s , d in domain.items():
            #print len(d)
            if len(d) < min:
                min = len(d)
                mrv = s
                #_mrv.append(s)
                #print 's,d'
                #print s,d
        #mrv = _mrv.pop()
        #print 'mrv'
        #print _mrv
                
            
                  
        #mrv = min
        
        #print 'mrv %s' %mrv
        
        #print domain[mrv]
        
        #while _mrv:
            #mrv = _mrv.pop()
        #values_cc = dict(values)
        for value in domain[mrv]: #mrv : minimum remaining value variable
            values_cc = dict(values)
            values_cc[mrv] =  value  # assigning a value to the mrv
            domain_cc_BT = self.domain_values(values_cc, peers)  # rewriting domain for each vacant square
            #print 'domain[mrv]'
            #print domain[mrv]
            assignment[mrv] = value
            consistency = self.ac_3(values_cc, domain_cc_BT, peers) # checking if consistent, forwards check
            #print 'the consistency is ' 
            #print consistency 
            if consistency:
                consistency , inference , domain = consistency  # if consistent, then new inference, new domain returned
                #print 'assignment us '
                #print assignment
                #if assignment:
                assignment = self.merge_two_dicts(assignment, inference) # merging inference and assignment
                #del domain[mrv]    # value found from domain. removing element from domain
                result = self.backtrack(assignment, values_cc, domain_cc_BT, peers)
                #if assignment:
                    #assignment = self.merge_two_dicts(assignment, inference) # merging inference and assignment
                #print 'Return assignment'
                #print domain['C3']
                #print domain['B3']
                #print 'mrv here '
                #print mrv
                #print assignment[mrv]
                #print result
                #print domain_cc_BT[mrv]
                if result:
                    return result
                #del domain[mrv]
            #values[mrv] = 0
            del assignment[mrv] 
            #assignment = {s: v for s, v in assignment.items() if s not in inference}  
        #print 'Reaching here'
        #print '_mrv'
        #print _mrv
        return False
            #domain[mrv] 
        
        #consistency = self.ac_3(values, domain, peers) # returns a 3-tuple if consistent, else False
        
        #if consistency:
            #consistency , inference , domain = consistency
            
    
    def merge_two_dicts(self,x, y):
        """Given two dicts, merge them into a new dict as a shallow copy."""
        z = x.copy()
        z.update(y)
        return z                     
            
        
                 
            
        
        
             
        
            
   
















#-------------------------------------------- Main -------------------------------------------------------  
  
  
# Define a main() function 
def main():
    solver = Solver()
  
    solver.solve()


#-----------------------------------------------------------------------------------------------------  


# This is the standard boilerplate that calls the main() function.   
if __name__ == '__main__':
    main()
