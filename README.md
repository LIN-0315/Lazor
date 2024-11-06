# Lazor project

## Team Member:

Weiting Yu

Yilin Li

## Introduction
This document provides the description of the Lazor Game, describing how to use the files and their roles and functionality.

---

## Modules Overview

### 1. `lazor_parse`

The `lazor_parse` module is responsible for parsing the bff files, transforming the data within the file into structured information that the game can use.

#### Functionality
- **Read Bff File**: Opens and reads the bff files that contains the game’s grid, lasers, blocks, points.
- **Parse Block and Laser Data**: Identifies and interprets data for grid, block types and quantities, initial laser positions and directions, points positions.
- **Return Parsed Data**: Converts the parsed file information into structured data that other game modules can directly work with to solve.

#### Purpose
The purpose of `lazor_parse` is to transform the bff files into data structures that are easy for other modules to process. For example, it can convert file contents into a dictionary format, setting up the initial state of the game board.

---

### 2. `lazor_board`

The `lazor_board` module is responsible for creating and managing the game’s board, which forms the core environment for the game.

#### Functionality
- **Generate Game Grid**: Uses data from `lazor_parse` to build a two-dimensional grid that represents block placements and laser paths.
- **Manage Block Positions**: Tracks the position of reflection, opaque, and refraction blocks within the grid.
- **Set Up Lasers and Targets**: Places lasers (including their initial position and direction) and points on the grid to facilitate laser path calculations.
- **Simulate the laser movement**: Simulate the laser movement for us to track the position.
- **Check in_bounds and results**: Check the laser is in bound and return the result the solution is existed or not.

#### Purpose
`lazor_board` is used to create and manage the game’s main environment. After setting up lasers and points in this module, the grid becomes the basis for subsequent path-solving processes.

---

### 3. `lazor_solver`

The `lazor_solver` module is responsible for calculating laser paths and block arrangements to ensure that all points are hit by a laser.

#### Functionality
- **Laser Path Calculation**: Simulates the laser path based on interactions with different block types (reflection, Opaque, refraction) and updates the path accordingly.
- **Generate Block Position Combinations**: Produces and tests potential block position combinations to find an arrangement that meets the game’s objectives.
- **Check Target Coverage**: Verifies whether all points are covered by a laser path during the simulation.
- **Provide Solution and save**: Returns a valid arrangement of blocks that allows lasers to hit all points and save to the files, or notifies the user if no solution exists.

#### Purpose
`lazor_solver` is the core algorithm module for the game, responsible for determining the block arrangement that meets the game’s goal. After game initialization, it continuously simulates and tests laser paths until it finds a solution that meets all points requirements.

---

## Module Relationships

1. **`lazor_parse`**: This is the initial step, reading and interpreting the bff files to provide essential data for building the game board and solving laser paths.
2. **`lazor_board`**: This module takes the parsed data to construct the game’s grid, placing blocks and lasers based on the initial configuration.
3. **`lazor_solver`**: Using the board setup and configuration, this module calculates laser paths, adjusts block arrangements, and seeks a solution to meet the game’s objectives.

Together, these modules work in tandem to parse the file, set up the game board, and find a solution for the laser game.

## Classes

### `Laser`

Represents a laser in the game, with properties for position and velocity.

- **`__init__(self, x, y, vx, vy)`**: Initializes the laser with an initial position `(x, y)` and `(vx, vy)`.
- **`move(self)`**: Updates the laser’s position based on its current velocity.

### `Block`

A base class for blocks on the board, defining basic interactions between the laser and the blocks.

- **`__init__(self, position)`**: Initializes a block with a specified position on the board.
- **`touch(self, laser)`**: Defines the default interaction when a laser touches the block. This method is overridden by subclasses.

### `ReflectBlock(Block)`

A subclass of `Block` that reflects lasers, reversing their direction upon contact.

- **`touch(self, laser)`**: Overrides the `touch` method to reverse the laser's direction.

### `OpaqueBlock(Block)`

A subclass of `Block` that completely blocks lasers, stopping their movement.

- **`touch(self, laser)`**: Overrides the `touch` method to set the laser’s velocity to zero, effectively stopping it.

### `RefractBlock(Block)`

A subclass of `Block` that splits a laser into two directions when hit.

- **`touch(self, laser)`**: Overrides the `touch` method to return two laser objects: one that continues in the original direction and another that reflects.

### `Point`

Represents a target point that the lasers must reach.

- **`__init__(self, x, y)`**: Initializes a point with an `(x, y)` position and a flag to check if it's reached.
  
## Functions

### `expand_grid(grid)`

Expands the grid by doubling its size to provide more space for block interactionathat generate a double length gird to solve.

- **Parameters**: `grid` (list) – The initial grid.
- **Returns**: `expanded_grid` (list) – The expanded grid.

### `Board`

Represents the entire game board, handling block placement, laser management, and points.

- **`__init__(self, grid, blocks, lasers, points)`**: Initializes the board with a grid, available blocks, laser positions, and target points.
- **place_block(block, position)**: Places a block on the expanded grid.
- **simulate()**: Simulates the laser movement
- **in_bounds(laser)**: Checks if the laser is in bounds
- **check()**: Checks if all points are touched
- **display()**: Displays the expanded grid with symbols for easier visualization.

### `parse_bff(parse_line)`

Parses the content of a `.bff` file to extract grid data, blocks, lasers, and points.

- **Parameters**: 
  - `parse_line` (str): The raw content of the `.bff` file as a string.
- **Returns**: A dictionary with the following keys:
  - `grid` (list): A 2D list representing the game board’s layout.
  - `blocks` (dict): A dictionary mapping block types (`A`, `B`, `C`) to their available quantities.
  - `lasers` (list): A list of tuples, each containing the initial `(x, y)` position and `(vx, vy)` direction of a laser.
  - `points` (list): A list of `(x, y)` tuples representing points that lasers must reach.

### `load_files(file_paths)`

Loads multiple `.bff` files, parsing each one to extract game configurations.

- **Parameters**: 
  - `file_paths` (list): A list of file paths to the `.bff` configuration files.
- **Returns**: A dictionary where each key is the filename and each value is the parsed output of `parse_bff`.

The `Lazor_solver` module provides functionality for solving the Lazor game by setting up the board and testing permutations of block placements. It uses depth-first search and permutation strategies to place blocks in a way that allows lasers to reach all target points.

## Functions

### `setup(data)`

Sets up the game board using parsed configuration data.

- **Parameters**: 
  - `data` (dict): A dictionary containing parsed data from a `.bff` file, including the grid, blocks, lasers, and points.
- **Returns**: 
  - `Board` instance initialized with the grid layout, block information, laser positions, and points.

### `dfs_solve(board, blocks, available_positions)`

Attempts to find a solution by testing different block placement using dfs.

- **Parameters**:
  - `board` (`Board`): The initialized game board.
  - `blocks` (list): A list of block instances that can be placed on the board.
  - `available_positions` (list): A list of coordinates where blocks can legally be placed on the board.
- **Returns**: 
  - `Board` instance with a solution if a valid arrangement is found, or `None` if no solution exists.

---

## Main Execution

Run the `Lazor_solver`:

1. Prompt the user to enter the name of a `.bff` file to solve.
2. Load and parse the file, initializing the board with the `setup` function.
3. Determine available positions on the board where blocks can be placed.
4. Initialize the blocks based on parsed data.
5. Attempt to find a solution.
6. Display and save the solution to output files if one is found.

## Example Usage:  
The Input .bff docs like (dark_1.bff)  

GRID START

x o o

o o o

o o x

GRID STOP

B 3

L 3 0 -1 1

L 1 6 1 -1

L 3 6 -1 -1

L 4 3 1 -1


P 0 3

P 6 1

The result will display like (solution_dark_1.txt)  

x  B  B 
     
B  o  o 
     
o  o  x 
