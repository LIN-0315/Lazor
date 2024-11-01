class Laser:
    def __init__(self, start_position, direction):
        """Initialize a laser with starting coordinates and direction."""
        self.x, self.y = start_position
        self.vx, self.vy = direction
        self.is_active = True  # Indicates if the laser is still moving

    def step_forward(self):
        """Move the laser one step in the current direction."""
        if self.is_active:
            self.x += self.vx
            self.y += self.vy


class Block:
    def __init__(self, position):
        """Initialize a generic block at a specific position on the grid."""
        self.position = position

    def interact(self, laser):
        """Defines how the block interacts with a laser. To be overridden by subclasses."""
        raise NotImplementedError("This method should be overridden in subclasses")


class BlockA(Block):  # Reflective Block
    def interact(self, laser):
        """Reflects the laser based on its direction of impact."""
        if (laser.x, laser.y) == self.position:
            # Reflect laser based on the axis of impact
            if laser.vx != 0:  # Horizontal impact
                laser.vx = -laser.vx
            if laser.vy != 0:  # Vertical impact
                laser.vy = -laser.vy


class BlockB(Block):  # Opaque Block
    def interact(self, laser):
        """Stops the laser when it encounters this block."""
        if (laser.x, laser.y) == self.position:
            laser.is_active = False  # Block the laser completely


class BlockC(Block):  # Refractive Block
    def interact(self, laser):
        """Splits the laser into two, one reflecting and one passing through."""
        if (laser.x, laser.y) == self.position:
            # Generate a new laser that continues in the same direction
            through_laser = Laser((laser.x, laser.y), (laser.vx, laser.vy))
            # Reflect the original laser
            if laser.vx != 0:
                laser.vx = -laser.vx
            if laser.vy != 0:
                laser.vy = -laser.vy
            return laser, through_laser  # Return both the reflected and through laser
        return laser, None
