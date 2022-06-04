# Utility functions

def clamp(var, low, high):
    out = var
    if var > high:
        out = high
    elif var < low:
        out = low
    return out

def cluster():
    pass

def switch(var):
    return 1 - var


class CollisionZone:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        #self.origin = origin

    def isHovered(self, mousePos, origin):
        if (self.pos[0] <= mousePos[0]-origin[0] <= self.pos[0] + self.size[0]) and (self.pos[1] <= mousePos[1]-origin[1] <= self.pos[1] + self.size[1]):
            return True
        else:
            return False

    def getPos(self):
        return self.pos
    def getSize(self):
        return self.size


#cz = CollisionZone((12,15),(32,48))
#print(cz.isHovered((16,63)))
#print(cz.isHovered((16,64)))