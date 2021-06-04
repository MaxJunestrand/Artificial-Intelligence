import math

A = input() #transition
B = input() #emission matrix
pi = input() #initial i prob
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

# Declare constants
maxIters = 50
oldLogProb = -99999999999999999.9 #smallish float
iters = 0


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

NumberOfEmissions = int(O.pop(0))



# create AlphaMatrix, which is filled with zeros and is T high and N wide
# Also called Forward algorithm

AlphaMatrix = []
for i in range(NumberOfEmissions):
    tempList = [0] * ANumberOfRows
    AlphaMatrix.append(tempList)


    
while iters < maxIters:

    # Scaling vector to keep things from underflowing
    c = [0]*NumberOfEmissions


    # This procedure iteratively estimates the probability to be in a certain state i at time t and 
    # having observed the observation sequence up to time t for t ∈ [1,..T ].
    AlphaMatrix = [[0.0]*len(A) for q in range(len(O))]
    for i in range(len(A)):
        AlphaMatrix[0][i] = B[i][O[0]]*pi[0][i]
        c[0] += AlphaMatrix[0][i]

    c[0] = 1/c[0]
    for i in range(len(A)):
        AlphaMatrix[0][i] = c[0]*AlphaMatrix[0][i]

    for timeStep in range(1,len(AlphaMatrix)):
        for i in range(len(A)):
            for j in range(len(A)):
                AlphaMatrix[timeStep][i] +=  A[j][i]*AlphaMatrix[timeStep-1][j]
            AlphaMatrix[timeStep][i] = AlphaMatrix[timeStep][i]*B[i][O[timeStep]]
            c[timeStep] += AlphaMatrix[timeStep][i]
        c[timeStep] = 1/c[timeStep]
        for i in range(len(A)):
            AlphaMatrix[timeStep][i] = c[timeStep]*AlphaMatrix[timeStep][i]


    #Beta or Backward algorithm
    betaMatrix = [[0.0]*len(A) for q in range(len(O))]
    # beta [t][i]

    # init beta, let init beta be scaled by c
    for i in range(len(betaMatrix[0])):
        betaMatrix[NumberOfEmissions-1][i] = c[-1]


    for t in range(len(O)-2, -1, -1):  #You go backwards (that's why its called backward algorithm)
        for i in range(len(A)):
            for j in range(len(A)): #Inner beta

                betaMatrix[t][i] += betaMatrix[t+1][j] * B[j][O[t+1]] * A[i][j]
            betaMatrix[t][i] = c[t]*betaMatrix[t][i] #scale beta with same factor as alpha



    # print("AlphaMatrix: ", AlphaMatrix, "len alpha: ", len(AlphaMatrix))

    # di gamma
    # Interpretation: Given the entire observation sequence and current estimate of the
    # HMM, what is the probability that at time (t) the hidden i is (Xt=i) && at time
    # (t+1) the hidden i is (Xt+1=j)?
    diGammaMatrix = [[[0.0]*ANumberOfRows for i in range(ANumberOfRows)] for ii in range(len(O))]
    # diGammaMatrix[t][i i][i j]
    gammaMatrix = [[0.0]*ANumberOfRows for q in range(len(O))]
    # gammaMatrix[t][i]

    # No need to normalize gamma matrices as alpha & beta have been normalized
    for t in range(len(O)-1):
        for i in range(len(A)):
            for j in range(len(A)):
                diGammaMatrix[t][i][j] = AlphaMatrix[t][i] * A[i][j] * B[j][O[t+1]] * betaMatrix[t+1][j]
                gammaMatrix[t][i] += diGammaMatrix[t][i][j]


    # special case for gamma_T-1
    for i in range(len(A)):
        gammaMatrix[NumberOfEmissions-2][i] = AlphaMatrix[NumberOfEmissions-2][i]

    # print("gammaMatrix: ", gammaMatrix)
    # estimations!

    # pi matrix
    for i in range(ANumberOfRows):
        pi[0][i] = gammaMatrix[0][i]


    # A matrix
    for i in range(ANumberOfRows):
        # print(diGammaMatrix)

        lower = 0
        for t in range(len(O)-1):
            lower += gammaMatrix[t][i]

        for j in range(ANumberOfRows):
            upper = 0
            for t in range(NumberOfEmissions-1):
                upper += diGammaMatrix[t][i][j]
            
            A[i][j] = upper/lower


    # B matrix
    for i in range(ANumberOfRows):
        lower = 0
        for t in range(NumberOfEmissions):
            lower += gammaMatrix[t][i]
        
        for j in range(len(B[0])):
            upper = 0
            for t in range(len(O)):
                if int(O[t]) == j:
                    upper += gammaMatrix[t][i]
            
            B[i][j] = upper/lower
        
    
    # print(MatrixToString(A))
    # print(MatrixToString(B))

    # Compute log(P(O|lambda))

    logProb = 0
    for i in range(NumberOfEmissions - 1):
        logProb += math.log(c[i])

    logProb = -logProb


    iters += 1
    if iters < maxIters and logProb > oldLogProb:
        oldLogProb = logProb
    else:
        break


print(MatrixToString(A))
print(MatrixToString(B))

