# Sudoku
Sudoku Backtracking Algorithm written in Python

Backtracking is an efficient algorithm for solving games like Sudoku, the 8-queens problem etc. At it's core, this is an optimized brute force search.

This repo has a driver file, which may be run from BASH as

``````
$ python driver.py 003020600900305001001806400008102900700000008006708200002609500800203009005010300

````````````````````````````````````````
003020600900305001001806400008102900700000008006708200002609500800203009005010300 represents the sudoku input, with the first character representing the first row and forst column and the last the last row last column. The digits are 'stringified' rowwise. eg. the first 18 characters would make:

        . . 3 |. 2 . |6 . . 
        9 . 3 |. 5 . |. 1 . 
        . . . |. . . |. . . 
        ------+------+------
        . . . |. . . |. . . 
        . . . |. . . |. . . 
        . . . |. . . |. . . 
        ------+------+------
        . . . |. . . |. . . 
        . . . |. . . |. . . 
        . . . |. . . |. . .

etc.
0 represents a void in the sudoku grid.

The Shell.py is a python program that iterates over the sudoku_start.txt file, which has 200 input grids, and outputs into the sudoku_finish.txt file.

The runner.py is to chack against the output delivered by the program against the solved grids for each.
