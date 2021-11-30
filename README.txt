Course:	     CS-131-Artificial Intelligence
Assignment: CSP
Name: 	     Yige Sun

Following the instruction, I used two methods to build sudoku solver: backtracking and conflict-directed backjumping.
In .py file, I use the name "smartjump" to denote conflict-directed backjumping.

***********************************************************************************************************************
To use different method, please follow the instruction at line 170 to modify the value of ALGORITHM at line 171
***********************************************************************************************************************
On my computer(Windows11 Python3.9 Pycharm):
Conflicted-directed back jumping uses around 0.91 seconds to solve two puzzles.
Backtracking method uses around only 0.31 seconds to solve two puzzles.
Thus, on my computer, backtracking will be faster.
***********************************************************************************************************************

i. Backtracking method:
	In this method, follow the lecture, we will recursively back to previous assignment once conflict happens.
ii. Conflicted-directed back jumping
	In this method, follow the lecture, we will keep conflict sets to determine where we will back to and do 
	new assignments.