"""Utility functions used in GoL. Anyone is free to use this module as they wish."""

def clamp(var, low=None, high=None):
    """
    :param var: value to clamp
    :type var: numeric
    :param low: minimum value for var
    :param high: maximum value for var
    :return: clamped var
    :rtype: numeric

    Acts as a min, max, or both depending on which arguments are given.
    Defines a domain for var, e.g: var ∈ [low,high].
    """
    out = var
    if low is not None and var < low:
        out = low
    if high is not None and var > high: # high != None or not high == None
        out = high
    return out


def cluster():
    pass

def switch(var):
    """
    :param var: value to switch
    :type var: bool
    :return: switched var

    This function takes a boolean and returns it's 'opposite'.
    """
    return bool(1 - var)


class CollisionZone:
    """
    Creates a "box" at coordinates `pos[x,y]` of dimensions `size[w,h]` that is able to detect collisions,
    with the mouse pointer for instance.
    """
    def __init__(self, pos, size):
        """
        :param pos: `[x,y]`. Coordinates of the object, on a 2D grid.
        :type pos: list
        :param size: `[w,h]`. Width and height of the object, without any unit.
        :type size: list

        Please give np.arrays or lists as args rather than tuples, as they are immutable and thus cannot be modified.
        """
        self.pos = pos
        self.size = size
        #self.origin = origin

    def isHovered(self, targetPos, origin):
        """
        :param targetPos: `[x,y]`. Position to check the overlap of with the defined CollisionZone.
        :type targetPos: list
        :param origin: `[x,y]`. Offset to apply to `pos[x,y]`.
        :type origin: list
        :return: isHovered
        :rtype: bool
        """
        if (self.pos[0] <= targetPos[0]-origin[0] <= self.pos[0] + self.size[0]) and (self.pos[1] <= targetPos[1]-origin[1] <= self.pos[1] + self.size[1]):
            return True
        else:
            return False

    def getPos(self):
        return self.pos
    def getSize(self):
        return self.size
