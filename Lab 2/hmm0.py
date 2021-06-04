#hello

A = input()
B = input()
pi = input()

A = A.split()
B = B.split()
pi = pi.split()
# first number is number of rows, second is number of columns


def MatrixBuilder(NumberRows, NumberCols, list):
    '''feed list without the two first elements (which only specify dimensions)
        returns: list of lists (matrix) '''

    matrix = []
    for row in range(0, NumberRows):
        r = []
        startOfCol = row * NumberCols
        for col in range(0, NumberCols):
            r.append(float(list[startOfCol + col]))
        matrix.append(r)
    
    return matrix
    

def MatrixMultiplier(X, Y):
    result = []
    for l in range(len(X)):
        result.append([0] * len(Y[0]))
    
    # iterate through rows of X
    for i in range(len(X)):
        # iterate through columns of Y
        for j in range(len(Y[0])):
            # iterate through rows of Y
            for k in range(len(Y)):
                result[i][j] += float(X[i][k]) * float(Y[k][j])

    return result


def MatrixToString(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    returnString = str(rows) + " " + str(cols)

    for r in range(rows):
        for c in range(cols):
            returnString += " " + str(matrix[r][c])
    
    return returnString


ANumberOfRows = int(A.pop(0))
ANumberOfCols = int(A.pop(0))
A = MatrixBuilder(ANumberOfRows, ANumberOfCols, A)

BNumberOfRows = int(B.pop(0))
BNumberOfCols = int(B.pop(0))
B = MatrixBuilder(BNumberOfRows, BNumberOfCols, B)

piNumberOfRows = int(pi.pop(0))
piNumberOfCols = int(pi.pop(0))
pi = MatrixBuilder(piNumberOfRows, piNumberOfCols, pi)


q2 = MatrixMultiplier(pi, A)

q3 = MatrixMultiplier(q2, B)


print(MatrixToString(q3))
