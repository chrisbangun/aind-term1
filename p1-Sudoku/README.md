# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A:
by enforcing the constraint that for every twin squares, there is no boxes that can contains the twin values.
On my current approach, I started by getting all boxes that only has two values in it, then find the twins in their
related peers. Once the twins is found, go through all the boxes in the related units, remove digits from twins value
from other unit boxes. Therefore, no boxes in any unit has the twin values outside the two naked twins squares.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A:
by adding the two main diagonals sudoku to our units collections.
Then, the rest implementation are much likely the same. The eliminate and only choice strategy will put all values
in boxes in related diagonal units into consideration. That is how we include diagonals to constraint propagation.

#### my repo: https://github.com/chrisbangun/aind-term1/tree/master/p1-Sudoku

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
