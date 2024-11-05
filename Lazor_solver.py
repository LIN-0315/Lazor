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
    bff_files = [
        'dark_1.bff', 'mad_1.bff', 'mad_4.bff', 'mad_7.bff',
        'numbered_6.bff', 'showstopper_4.bff', 'tiny_5.bff', 'yarn_5.bff'
    ]

    # Load and parse .bff files
    parsed_bff_files = load_files(bff_files)

    for filename, data in parsed_bff_files.items():
        print(f"\nSolving for file: {filename}")

        board = setup(data)

        # Get available positions and initialize blocks
        available_positions = [
            (i, index) for index, row in enumerate(data["grid"]) for i, cell in enumerate(row) if cell == 'o'
        ]

        # Initialize blocks list
        blocks = [ReflectBlock((0, 0))] * data["blocks"].get("A", 0) + \
                 [OpaqueBlock((0, 0))] * data["blocks"].get("B", 0) + \
                 [RefractBlock((0, 0))] * data["blocks"].get("C", 0)

        # Solve the board
        solution_board = dfs_solve(board, blocks, available_positions)

        # Output results
        if solution_board:
            print(f"Solution found for {filename}!")
            solution_board.display()
        else:
            print(f"No solution found for {filename}.")