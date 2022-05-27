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