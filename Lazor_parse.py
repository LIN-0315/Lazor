def parse_bff(parse_line):
    # Store the grid, blocks lasers and points
    grid = []
    blocks = {}
    lasers = []
    points = []

    # Split into lines
    lines = parse_line.strip().split('\n')
    grid_start = False

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip the comments
        if line.startswith("#"):
            continue

        # Detect the start and end of the grid
        if line == "GRID START":
            grid_start = True
            continue
        elif line == "GRID STOP":
            grid_start = False
            continue

        if grid_start:
            # Add grid lines
            grid.append(line.split())
        elif line.startswith("A") or line.startswith("B") or line.startswith("C"):
            # Parse the blocks
            type_b, num = line.split()
            blocks[type_b] = int(num)
        elif line.startswith("L"):
            # Parse laser
            x, y, vx, vy = map(int, line.split()[1:])
            lasers.append((x, y, vx, vy))
        elif line.startswith("P"):
            # Parse points
            x, y = map(int, line.split()[1:])
            points.append((x, y))

    # Return the parsed grid, blocks, lasers, points as a dictionary
    return {
        "grid": grid,
        "blocks": blocks,
        "lasers": lasers,
        "points": points
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
