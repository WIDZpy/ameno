import numpy as np


def readRLE(filename, c_shape=(50, 50)):
    if filename == 1:
        return np.zeros(c_shape).astype(int)
    filename = "rle/" + filename + ".rle"
    f = open(filename, "r")
    s = ''
    while True:
        ligne = f.readline()

        if ligne == '':  # Empty indicates end of file. An empty line would be '\n'
            break

        if ligne[0] == '#':
            continue

        if ligne[0] == 'x':
            continue

        s = s + ligne[:-1]  # To remove EOL
    s = s + '$' if s[-1] != '$' else ''
    f.close()

    # curX, curY = 0, 0

    colone = np.array([[]]).astype(int)
    line = np.zeros(colone.shape[-1]).astype(int)
    coef = ""
    q = 1
    print(q)

    for loop in s:

        if loop == '':  # End of file
            break

        if loop == '$':

            q = 1 if coef == '' else int(coef)

            while int(colone.shape[-1]) < int(line.shape[-1]):
                colone = np.hstack((colone, np.zeros((colone.shape[0] if colone.shape[0] != 0 else 1, 1)).astype(int)))

            while int(colone.shape[-1]) > int(line.shape[-1]):
                line = np.hstack((line, [0]))

            for nn in range(q):
                colone = np.vstack((colone, line))
                line = np.zeros(colone.shape[-1]).astype(int)

            # reset line
            line = np.array([]).astype(int)
            coef = ""

        if 47 < ord(str(loop)) < 58:
            coef = coef + str(loop)

        if loop == 'b' or loop == 'o':
            q = 1 if coef == '' else int(coef)

            for i in range(q):
                line = np.hstack((line, [0 if loop == 'b' else 1]))

            coef = ''

    return colone[1:]
