'''
EN.640.635 Software Carpentry at JHU
Lazer Group Project
Group： Weiting Yu, Yilin Li

Lazor Game Solver - Solution Algorithm
This script contains the primary solution DFS algorithm for the Lazor game. It handles
finding valid configurations for placing blocks, tracing laser paths, and checking
if all target points are hit by the lasers.


'''

from Lazor_parse import load_files
from Lazor_Board import Board, Laser, ReflectBlock, OpaqueBlock, RefractBlock, Point
import copy
import os


def setup(data):
    '''
    Method setup.
    '''
    """Initializes the board with grid, blocks, lasers, and points from data."""
    
    # Assigns values or updates solution state
    grid = data["grid"]
    blocks = data["blocks"]
    lasers = [Laser(x, y, vx, vy) for x, y, vx, vy in data["lasers"]]
    points = [Point(x, y) for x, y in data["points"]]

# Returns result of method
    return Board(grid, blocks, lasers, points)


def dfs_solve(board, blocks, available_positions):
    
    '''
    Method dfs_solve.
    Finds a solution by placing blocks and tracing laser paths.

    Returns:
        bool: True if a solution is found where all target points are hit; False otherwise.
    '''
    
    """Recursive DFS to solve the Lazor game"""

    # If all blocks are placed, simulate and check if it's a solution
    if not blocks:
        board.simulate()
        if board.check():
            return board
        else:
            return None

    # Try placing each remaining block in each available position
    for i, pos in enumerate(available_positions):
        for j, block in enumerate(blocks):
            # Make a deep copy of the board to maintain independence
            new_board = copy.deepcopy(board)
            new_board.place_block(block, pos)

            # Update the list of blocks and positions for the recursive call
            new_blocks = blocks[:j] + blocks[j + 1:]
            new_positions = available_positions[:i] + available_positions[i + 1:]

            # Recursive call with updated board, blocks, and positions
            solution = dfs_solve(new_board, new_blocks, new_positions)
            if solution:
                return solution

    # Return None if no solution found
    return None


if __name__ == "__main__":
    file_name = input("Enter the name of the .bff file to solve (format 'mad_1.bff'): ")

    # Load and parse the specified .bff file
    parsed_files = load_files([file_name])
    data = parsed_files[file_name]

    # Initialize the board using the setup function
    board = setup(data)

    # Get available positions if it shows 'o' in the board
    available_positions = [
        (i, index) for index, row in enumerate(data["grid"]) for i, n in enumerate(row) if n == 'o'
    ]

    # Initialize blocks list
    blocks = [ReflectBlock((0, 0))] * data["blocks"].get("A", 0) + \
             [OpaqueBlock((0, 0))] * data["blocks"].get("B", 0) + \
             [RefractBlock((0, 0))] * data["blocks"].get("C", 0)

    # Solve the board using DFS
    solution_board = dfs_solve(board, blocks, available_positions)

    if solution_board:
        print("Solution found!")
        solution_board.display()
    else:
        print("No solution found.")

def save_solution_to_txt(board, bff_filename):
    '''
    Saves the board solution to a text file with the same name as the .bff file.
    
    Parameters:
        board (Board): The final board layout after solving the puzzle.
        bff_filename (str): The name of the .bff file used to load the board configuration.
    '''
    # Derive the solution filename from the .bff filename
    solution_filename = os.path.splitext(bff_filename)[0] + "_solution.txt"
    
    # Prepare the board layout as text
    lines = []
    for row in board.grid:
        line = " ".join(row)
        lines.append(line)
    
    # Write the solution to a text file
    with open(solution_filename, "w") as file:
        file.write("\n".join(lines))
    
    print(f"Solution saved to {solution_filename}")

# Assuming `board` is the final board with the solution and `bff_file` is the name of the .bff file
save_solution_to_txt(board, "solution")
