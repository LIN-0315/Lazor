from Lazor_parse import load_files
from Lazor_Board import Board, Laser, ReflectBlock, OpaqueBlock, RefractBlock, Point
import copy


def setup(data):
    """Initializes the board with grid, blocks, lasers, and points from data."""
    grid = data["grid"]
    blocks = data["blocks"]
    lasers = [Laser(x, y, vx, vy) for x, y, vx, vy in data["lasers"]]
    points = [Point(x, y) for x, y in data["points"]]

    return Board(grid, blocks, lasers, points)


def dfs_solve(board, blocks, available_positions):
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
