'''
This file defines components related to the Lazor Project, including classes for handling lasers and different block types.

Classes:
- Laser: Represents the laser beam.
- ReflectBlock: Represents a block that reflects the laser.
- OpaqueBlock: Represents a block that blocks the laser.
- RefractBlock: Represents a block that refracts the laser.
'''

class Laser:
    '''
    Represents a laser beam with a position and direction.
    
    Parameters:
        position: tuple
            The initial (x, y) position of the laser.
        direction: tuple
            The (vx, vy) direction vector of the laser.
    '''
    
    def __init__(self, position, direction):
        '''Initialize laser position and direction.'''
        self.x, self.y = position
        self.vx, self.vy = direction
        self.is_blocked = False  # Indicates if laser is blocked

    def move(self):
        '''Update the laser's position based on its direction.'''
        self.x += self.vx
        self.y += self.vy


class ReflectBlock:
    '''
    Represents a block that reflects a laser beam.
    
    Parameters:
        position: tuple
            The (x, y) position of the block on the grid.
    '''
    
    def __init__(self, position):
        '''Initialize reflect block position.'''
        self.position = position

    def reflect(self, laser: 'Laser') -> 'Laser':
        '''
        Reflects the laser when it hits the block.
        
        Parameters:
            laser: Laser
                The laser beam hitting the block.
        
        Returns:
            Laser: The laser with updated direction after reflection.
        '''
        rel_pos = (laser.x - self.position[0], laser.y - self.position[1])

        if rel_pos in [(0, 1), (0, -1)]:  # Vertical hit
            laser.vy = -laser.vy
        elif rel_pos in [(1, 0), (-1, 0)]:  # Horizontal hit
            laser.vx = -laser.vx

        laser.move()  # Update position after reflection
        return laser

    def __call__(self, laser):
        '''Allow the block to be called to reflect a laser.'''
        return self.reflect(laser)


class OpaqueBlock:
    '''
    Represents a block that blocks a laser beam.
    
    Parameters:
        position: tuple
            The (x, y) position of the block on the grid.
    '''
    
    def __init__(self, position):
        '''Initialize opaque block position.'''
        self.position = position

    def block(self, laser: 'Laser') -> 'Laser':
        '''
        Blocks the laser, stopping its movement.
        
        Parameters:
            laser: Laser
                The laser beam hitting the block.
        
        Returns:
            Laser: The laser marked as blocked.
        '''
        laser.is_blocked = True
        return laser

    def __call__(self, laser):
        '''Allow the block to be called to block a laser.'''
        return self.block(laser)


class RefractBlock:
    '''
    Represents a block that can refract a laser beam, creating a new laser.
    
    Parameters:
        position: tuple
            The (x, y) position of the block on the grid.
    '''
    
    def __init__(self, position):
        '''Initialize refract block position.'''
        self.x, self.y = position

    def refract(self, laser: 'Laser') -> ('Laser', 'Laser'):
        '''
        Refracts the laser, creating a new laser beam with opposite direction.
        
        Parameters:
            laser: Laser
                The laser beam hitting the block.
        
        Returns:
            laser: Laser
                The original laser beam.
            new_laser: Laser
                The refracted laser beam in a new direction.
        '''
        new_vx, new_vy = laser.vx, laser.vy

        if (self.x - 1, self.y) == (laser.x, laser.y) or (self.x + 1, self.y) == (laser.x, laser.y):
            new_vx = -laser.vx
        if (self.x, self.y - 1) == (laser.x, laser.y) or (self.x, self.y + 1) == (laser.x, laser.y):
            new_vy = -laser.vy

        new_laser = Laser((laser.x, laser.y), (new_vx, new_vy))
        laser.move()  # Move original laser
        return new_laser, laser

    def __call__(self, laser):
        '''Allow the block to be called to refract a laser.'''
        return self.refract(laser)
