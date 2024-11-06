'''
EN.640.635 Software Carpentry at JHU
Lazer Group Project
Group： Weiting Yu, Yilin Li


Lazor Game Solver Parser
This file is responsible for parsing the .bff board configuration file for the Lazor game.
It reads grid settings, block configurations, laser positions, and target points from the file,
and organizes them into structured data for further processing.


'''


def parse_bff(parse_line):
    '''
    Parses the .bff file for Lazor game settings, including the grid layout, blocks,
    lasers, and target points.
    Parameters:
        parse_line (str): Contents of the .bff file as a single string.
    Returns:
        dict: Contains grid, blocks, lasers, and points as parsed data.
    '''
    # Initialize storage for grid layout, block counts, laser positions, and target points
    grid = []  # Stores the grid layout of allowed and blocked cells
    blocks = {}  # Stores block types with their counts (A, B, C)
    lasers = []  # Stores laser start positions and direction vectors
    points = []  # Stores coordinates of target points

    # Split the input into individual lines
    lines = parse_line.strip().split('\n')
    grid_start = False  # Flag to indicate if the grid definition has started

    # Iterate over each line in the file to process grid, blocks, lasers, and points
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue

        # Identify grid start and stop markers for parsing the grid layout
        if line == "GRID START":
            grid_start = True
            continue
        elif line == "GRID STOP":
            grid_start = False
            continue

        # Process lines within grid section
        if grid_start:
            # Each line corresponds to a row in the grid layout
            grid.append(line.split())
        # Process block definitions
        elif line.startswith("A") or line.startswith("B") or line.startswith("C"):
            # Parse block type and quantity
            type_b, num = line.split()
            blocks[type_b] = int(num)  # Add block type with count
        # Process laser configurations
        elif line.startswith("L"):
            # Expected laser format: L x y vx vy
            laser_data = line.split()
            lasers.append(tuple(map(int, laser_data[1:])))  # Convert positions and vectors to integers
        # Process target points for laser intersections
        elif line.startswith("P"):
            # Expected point format: P x y
            point_data = line.split()
            points.append((int(point_data[1]), int(point_data[2])))  # Convert coordinates to integers

    # Return all parsed data in a structured dictionary for game setup
    return {
        "grid": grid,       # Grid layout of the game board
        "blocks": blocks,   # Block types and their counts
        "lasers": lasers,   # Laser starting points and directions
        "points": points    # Target points for laser paths
    }



# List of .bff files to parse
bff_files = [
    'dark_1.bff',
    'mad_1.bff',
    'mad_4.bff',
    'mad_7.bff',
    'numbered_6.bff',
    'showstopper_4.bff',
    'tiny_5.bff',
    'yarn_5.bff'
]


def load_files(file_paths):
    """Loads multiple files"""
    file_lst = {}
    for file in file_paths:
        with open(file, 'r') as f:
            parse = f.read()
        file_lst[file] = parse_bff(parse)
    return file_lst


if __name__ == "__main__":
    mad_1_result = {
        "grid": [
            ["o", "o", "o", "o"],
            ["o", "o", "o", "o"],
            ["o", "o", "o", "o"],
            ["o", "o", "o", "o"]
        ],
        "blocks": {
            "A": 2,
            "C": 1
        },
        "lasers": [
            (2, 7, 1, -1)
        ],
        "points": [
            (3, 0),
            (4, 3),
            (2, 5),
            (4, 7)
        ]
    }

    parsed_files = load_files(["mad_1.bff"])

    parsed_mad_1_result = parsed_files["mad_1.bff"]

    assert parsed_mad_1_result["grid"] == mad_1_result["grid"], f"Grid mismatch: {parsed_mad_1_result['grid']}"
    assert parsed_mad_1_result["blocks"] == mad_1_result["blocks"], f"Blocks mismatch: {parsed_mad_1_result['blocks']}"
    assert parsed_mad_1_result["lasers"] == mad_1_result["lasers"], f"Lasers mismatch: {parsed_mad_1_result['lasers']}"
    assert parsed_mad_1_result["points"] == mad_1_result["points"], f"Points mismatch: {parsed_mad_1_result['points']}"

    print("mad_1.bff parsing test passed!")
