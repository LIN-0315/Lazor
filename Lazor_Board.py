from Lazor_parse import load_files


class Laser:
    """Class representing a laser with position and direction."""
    def __init__(self, x, y, vx, vy):
        self.x = x  # x position
        self.y = y  # Y position
        self.vx = vx  # Velocity X
        self.vy = vy  # Velocity Y

    """Moves the laser"""
    def move(self):
        self.x += self.vx
        self.y += self.vy


class Block:
    """Base class for blocks."""
    def __init__(self, position):
        self.position = position

    def touch(self, laser):
        """Define the result when laser touches the blocks"""
        None


class ReflectBlock(Block):
    """Reflects the laser at a 90-degree angle."""
    def touch(self, laser):
        laser.vx, laser.vy = -laser.vx, -laser.vy


class OpaqueBlock(Block):
    """Blocks the laser"""
    def touch(self, laser):
        laser.vx, laser.vy = 0, 0


class RefractBlock(Block):
    """Splits the laser into two directions."""
    def touch(self, laser):
        # Creates a reflected laser
        reflected = Laser(laser.x, laser.y, -laser.vx, -laser.vy)
        return [laser, reflected]


class Point:
    """Class representing a target point"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.touch = False


def expand_grid(grid):
    """Expands the grid"""
    expanded_grid = [['' for _ in range(len(grid[0]) * 2)] for _ in range(len(grid) * 2)]

    for index, row in enumerate(grid):
        for index_i, i in enumerate(row):
            expanded_grid[index * 2][index_i * 2] = i  # Place original cells in even coordinates

    return expanded_grid


class Board:
    """Class representing the game board"""
    def __init__(self, grid, blocks, lasers, points):
        self.origin_grid = grid # The origin grid parsed from bff files
        self.grid = expand_grid(grid)  # Expanded grid
        self.blocks = {}  # Dictionary of block positions
        self.blocks_tem = []  # List to store unplaced block objects
        self.lasers = lasers
        self.points = points

        for types, num in blocks.items():
            for _ in range(num):
                if types == 'A':
                    self.blocks_tem.append(ReflectBlock((0, 0)))  # Initialize ReflectBlock
                elif types == 'B':
                    self.blocks_tem.append(OpaqueBlock((0, 0)))  # InitializeOpaqueBlock
                elif types == 'C':
                    self.blocks_tem.append(RefractBlock((0, 0)))  # Initialize RefractBlock

    def place_block(self, block, position):
        """Places a block on the expanded grid"""
        block.position = (position[0] * 2, position[1] * 2)
        self.blocks[(position[0] * 2, position[1] * 2)] = block
        self.grid[(position[0] * 2, position[1] * 2)[1]][(position[0] * 2, position[1] * 2)[0]] = block

    def simulate(self):
        """Simulates the laser movement"""
        for i in self.lasers:
            while self.in_bounds(i):
                # Move the laser
                i.move()
                # Detect touches odd or even
                if (i.x % 2 == 1) and (i.y % 2 == 1):
                    # Odd coordinate
                    block = self.blocks.get((i.x // 2, i.y // 2))
                    if block:
                        re = block.touch(i)
                        if isinstance(re, list):
                            # If the laser is refracted
                            self.lasers.extend(re[1:])

                # Check if the laser touches a point
                for n in self.points:
                    if (i.x, i.y) == (n.x, n.y):
                        n.touch = True

    def in_bounds(self, laser):
        """Checks if the laser is in bounds"""
        return 0 <= laser.x < len(self.grid[0]) and 0 <= laser.y < len(self.grid)

    def check(self):
        """Checks if all points are touched"""
        return all(i.touch for i in self.points)

    def display(self):
        """Displays the expanded grid with symbols for easier visualization."""
        for row in self.grid:
            row_display = []
            for cell in row:
                if cell is None:
                    row_display.append('.')
                elif isinstance(cell, ReflectBlock):
                    row_display.append('A')
                elif isinstance(cell, OpaqueBlock):
                    row_display.append('B')
                elif isinstance(cell, RefractBlock):
                    row_display.append('C')
                else:
                    row_display.append(str(cell))
            print(" ".join(row_display))

