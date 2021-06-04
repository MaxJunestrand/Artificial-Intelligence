
A = input() #transition
B = input() #emission matrix
pi = input() #initial state prob
O = input() # Sequence of Emissions

A = A.split()
B = B.split()
pi = pi.split()
O = O.split()
# first number is number of rows, second is number of columns

newO = []
for i in O:  # make O a list of integers
    newO.append(int(i))

O = newO


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


# create AlphaMatrix, which is filled with zeros and is T high and N wide
AlphaMatrix = []
for i in range(NumberOfEmissions):
    tempList = [0] * ANumberOfRows
    AlphaMatrix.append(tempList)



def initAlpha():
    for i in range(ANumberOfRows):
        AlphaMatrix[0][i] = B[i][O[0]] * pi[0][i]


# populate alphaMatrix with numbers
def firstAlpha(state, t):    
    totalSum = 0
    for j in range(ANumberOfRows): # N = ANumberOfRows = number of different states
        totalSum += AlphaMatrix[t-1][j]*A[j][state]

    AlphaMatrix[t][state] = totalSum * B[state][O[t]]
    return totalSum * B[state][O[t]]


def secondAlpha():
    totalSum = 0
    for i in range(1, NumberOfEmissions): # T = NumberOfEmissions = number of timesteps
        for j in range(ANumberOfRows): # N = number of states
            totalSum += firstAlpha(j, i)
    return totalSum
    
def lastSum():
    summ = 0
    for i in range(ANumberOfRows):
        summ += AlphaMatrix[NumberOfEmissions-1][i]
    return summ

initAlpha()
secondAlpha()

print(AlphaMatrix)
print(lastSum())
