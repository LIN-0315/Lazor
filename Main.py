import time
import os
from Blocks import Laser, ReflectBlock, OpaqueBlock, RefractBlock
from copy import deepcopy
from collections import deque

class Board:
    '''
    Represents the game board, loading the game settings and creating the grid.
    Determines possible positions for placing blocks and non-block areas.
    
    Attributes:
        grid (list): The matrix representing the board layout.
        blocks (dict): Counts of each block type (reflect, opaque, refract).
        lasers (list): Laser beams on the board with their positions and directions.
        targets (list): Target points that lasers should intersect.
        grid_content (list): Raw grid layout from the .bff file.
    '''
    
    def __init__(self):
        '''Initialize the Board with default settings.'''
        self.grid = []
        self.blocks = {'reflect': 0, 'opaque': 0, 'refract': 0}  
        self.lasers = []
        self.targets = []
        self.grid_content = []

    def load_bff(self, filename):
        '''
        Loads the game settings from a .bff file and creates the grid.
        
        Parameters:
            filename (str): Path to the .bff configuration file.
        '''
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        reading_grid = False
        for line in lines:
            line = line.strip()
            if line.startswith('#') or not line:
                continue

            if line == 'GRID START':
                reading_grid = True
            elif line == 'GRID STOP':
                reading_grid = False
            elif reading_grid:
                self.grid_content.append(line.split())
            else:
                parts = line.split()
                if parts[0] in 'ABC':  
                    block_type = 'reflect' if parts[0] == 'A' else 'opaque' if parts[0] == 'B' else 'refract'
                    self.blocks[block_type] = int(parts[1])
                elif parts[0] == 'L':
                    self.lasers.append({
                        'position': (int(parts[1]), int(parts[2])),
                        'direction': (int(parts[3]), int(parts[4]))
                    })
                elif parts[0] == 'P':
                    self.targets.append((int(parts[1]), int(parts[2])))
        
        self.create_matrix(self.grid_content)

    def create_matrix(self, grid_content):
        '''
        Creates a 2D matrix representation of the board based on provided grid content.
        
        Parameters:
            grid_content (list): Grid layout from the .bff file.
        '''
        rows = len(grid_content)
        cols = len(grid_content[0]) if rows > 0 else 0
        self.grid = [[' ' for _ in range(2 * cols + 1)] for _ in range(2 * rows + 1)]
        
        for r in range(rows):
            for c in range(cols):
                self.grid[2 * r + 1][2 * c + 1] = grid_content[r][c]

    def __call__(self):
        '''
        Returns positions for placing blocks and non-block areas on the grid.
        
        Returns:
            legal_positions (list): Coordinates where blocks can be placed.
            illegal_positions (list): Coordinates where blocks cannot be placed.
            grid (list): The expanded grid layout.
        '''
        legal_positions = [
            (j, i) for i in range(len(self.grid))
            for j in range(len(self.grid[0]))
            if self.grid[i][j] == 'o'
        ]
        
        illegal_positions = [
            ((j, i), self.grid[i][j]) for i in range(len(self.grid))
            for j in range(len(self.grid[0]))
            if self.grid[i][j] in ['x', 'opaque']
        ]

        return legal_positions, illegal_positions, self.grid
    
    


class Solve:
    '''
    Represents the solving algorithm using a BFS approach to place blocks and guide lasers to target points.

    Parameters:
        grids (callable): Returns the legal and illegal positions and the grid.
        lasers (list): List of Laser objects on the board.
        blocks (dict): Dictionary with counts of each block type (reflect, opaque, refract).
        targets (list): List of target points that lasers must intersect.
    '''

    def __init__(self, grids, lasers, targets, blocks):
        '''
        Initializes the Solve object with the provided board layout, lasers, targets, and blocks.
        '''
        self.legal_positions, self.illegal_positions, self.grid = grids()
        self.lasers = lasers
        self.blocks = blocks
        self.targets = targets

    def bfs_solve(self):
        '''
        Uses BFS to find a configuration of blocks that directs lasers to all target points.

        Returns:
            tuple: (solved (bool), result_positions (list), result_blocks (list))
        '''
        initial_state = {
            'grid': deepcopy(self.grid),
            'lasers': deepcopy(self.lasers),
            'targets': deepcopy(self.targets),
            'blocks': self.blocks,
            'positions': []
        }
        queue = deque([initial_state])

        while queue:
            state = queue.popleft()
            current_grid = state['grid']
            remaining_targets = state['targets']
            current_positions = state['positions']

            # Check if all targets are hit
            if not remaining_targets:
                # Extract block types and their positions for the solution
                result_positions = [pos for _, pos in current_positions]
                result_blocks = [block for block, _ in current_positions]
                return True, result_positions, result_blocks

            # If there are remaining positions to explore, place a block
            if state['blocks']:
                for pos in self.legal_positions:
                    if pos in [p for _, p in current_positions]:  # Skip if position already occupied
                        continue
                    
                    # Try placing each type of block
                    for block_type in ['reflect', 'opaque', 'refract']:
                        if state['blocks'][block_type] > 0:
                            # Copy the state and modify it for this block placement
                            new_state = deepcopy(state)
                            new_state['positions'].append((block_type, pos))
                            new_state['blocks'][block_type] -= 1
                            new_state['grid'][pos[1]][pos[0]] = block_type

                            # Run laser paths and check for target hits
                            new_state['lasers'], new_state['targets'] = self.run_lasers(new_state['lasers'], new_state['grid'], new_state['targets'])

                            # Add modified state to queue for further exploration
                            queue.append(new_state)

        return False, [], []  # No solution found

    def run_lasers(self, lasers, grid, targets):
        '''
        Runs the lasers on the grid and updates target points as they're hit.

        Parameters:
            lasers (list): List of Laser objects.
            grid (list): 2D grid with blocks and empty spaces.
            targets (list): List of target points.

        Returns:
            tuple: (updated lasers list, updated targets list)
        '''
        updated_targets = set(targets)
        for laser in lasers:
            while not laser.is_blocked and (laser.x, laser.y) in updated_targets:
                if (laser.x, laser.y) in updated_targets:
                    updated_targets.remove((laser.x, laser.y))

                next_position = (laser.x + laser.vx, laser.y + laser.vy)
                if grid[next_position[1]][next_position[0]] == 'reflect':
                    ReflectBlock((laser.x, laser.y)).reflect(laser)
                elif grid[next_position[1]][next_position[0]] == 'opaque':
                    OpaqueBlock((laser.x, laser.y)).block(laser)
                elif grid[next_position[1]][next_position[0]] == 'refract':
                    new_laser, laser = RefractBlock((laser.x, laser.y)).refract(laser)
                    lasers.append(new_laser)
                else:
                    laser.move()  # Move if no block interaction

        return lasers, list(updated_targets)

def run(file):
    '''
    Loads the board configuration from the specified file,
    runs the solve, and plots the solution to a text file.

    Parameters:
        file (str): The filename of the game configuration.
    '''
    # Initialize the board
    board = Board()

    try:
        board.load_bff('./Board/' + file + '.bff')
    except FileNotFoundError:
        print(f"Error: File {file}.bff not found in Board directory.")
        return  # Exit the function if the file is not found

    print('RUNNING')
    time_start = time.time()
    
    # Initialize the lasers using the Laser class
    lasers = [Laser(laser['position'], laser['direction']) for laser in board.lasers]
    
    # Initialize the solver with BFS approach
    solver = Solve(board, lasers, board.targets, board.blocks)
    
    # Run the solver using BFS
    solved, result_positions, result_blocks = solver.bfs_solve()
    
    # Display the result
    if solved:
        # Solution found, plot the result
        plot_result_to_txt(board, result_blocks, result_positions, filename=file + "_solution.txt")
        print("Solution saved in", file + "_solution.txt")
    else:
        # No solution found
        print('No solution.')

    time_end = time.time()
    print('Successfully Resolved!' if solved else 'Resolution Failed.')
    print('Time cost:', time_end - time_start, 'seconds')


if __name__ == '__main__':
    game_name = input('Enter game name to solve: ')
    run(game_name)
