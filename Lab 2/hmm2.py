A = input() #transition
B = input() #emission matrix
pi = input() #initial state prob
O = input() # Sequence of Emissions

A = A.split()
B = B.split()
pi = pi.split()
O = O.split()

O = [int(i) for i in O]

def MatrixBuilder(NumberRows, NumberCols, list):
    matrix = []
    for row in range(0, NumberRows):
        r = []
        startOfCol = row * NumberCols
        for col in range(0, NumberCols):
            r.append(float(list[startOfCol + col]))
        matrix.append(r)

    return matrix

ANumberOfRows = int(A.pop(0))
ANumberOfCols = int(A.pop(0))
A = MatrixBuilder(ANumberOfRows, ANumberOfCols, A)

BNumberOfRows = int(B.pop(0))
BNumberOfCols = int(B.pop(0))
B = MatrixBuilder(BNumberOfRows, BNumberOfCols, B)

piNumberOfRows = int(pi.pop(0))
piNumberOfCols = int(pi.pop(0))

pi = MatrixBuilder(piNumberOfRows, piNumberOfCols, pi)

NumberOfEmissions = int(O.pop(0))

# create DeltaMatrix, which is filled with zeros and is T high and N wide
DeltaMatrix = []
for i in range(NumberOfEmissions):
    tempList = [0] * ANumberOfRows
    DeltaMatrix.append(tempList)

DeltaMatrixArgs = []
for i in range(NumberOfEmissions):
    tempList = [-1] * ANumberOfRows
    DeltaMatrixArgs.append(tempList)

# Init delta
for i in range(ANumberOfRows):
    DeltaMatrix[0][i] = B[i][O[0]] * pi[0][i]

for t in range(1, NumberOfEmissions):  # T = NumberOfEmissions = number of timesteps
    for i in range(ANumberOfRows): # N = number of states
        maxNumber = 0.0
        index = 0
        for j in range(ANumberOfRows): # N = ANumberOfRows = number of different states
            currNum = DeltaMatrix[t-1][j] * A[j][i] * B[i][O[t]]
            if currNum >= maxNumber:
                index = j
                maxNumber = currNum
        DeltaMatrix[t][i] = maxNumber
        if(maxNumber > 0):
            DeltaMatrixArgs[t][i] = index

# print(DeltaMatrix)

result = [None] * NumberOfEmissions
tempIndex = None
tempMax = -1.0

# Calculating max of last row
tempIndex = DeltaMatrix[NumberOfEmissions-1].index(max(DeltaMatrix[NumberOfEmissions-1]))
#print(tempIndex)
#print(DeltaMatrix)
result[NumberOfEmissions-1] = tempIndex

# Backtracking
for i in range(NumberOfEmissions-1, 0, -1):
    tempIndex = DeltaMatrixArgs[i][tempIndex]
    result[i-1] = tempIndex

s = ""
for i in range(NumberOfEmissions):
    s+= str(result[i]) + " "
print(s)
