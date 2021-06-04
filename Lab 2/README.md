# ai_labb2

### Question 1 This problem can be formulated in matrix form. Please specify the initial probability vector π, the transition probability matrix A and the observation probability matrix B.


π 
| c1  | c2  |
|-----|-----|
| 0.5 | 0.5 |

A
|    | c1  | c2  |
|----|-----|-----|
| c1 | 0.5 | 0.5 |
| c2 | 0.5 | 0.5 |

B
|    | head | tail |
|----|------|------|
| c1 | 0.9  | 0.1  |
| c2 | 0.5  | 0.5  |

Initially there is equal chance for both coins to be chosen. Then each time there is equal chance that each coin is chosen. For c_1 there is a 90% chance that we get head, and for c_2 there is equal chance.

### Question 2 What is the result of this operation?

T = A * [[1],[0]] = [[0.5], [0.5]]

### Question 3 What is the result of this operation?
T * B = [0.7, 0.3]


### Question 4 Why is it valid to substitute O_1:t = o_1:t with O_t = o_t when we condition on the state X_t = x_i?

O_1:t stands for an observation sequence, whereas O_t only stands for one observation. So when we condition on the state X_t, we only want to look at one observation.


### Question 5 How many values are stored in the matrices δ and δ^idx respectively?
δ has T*N values, and δ^idx has (T-1)*N values, as we do not want for the initial time.

### Question 6 Why we do we need to divide by the sum over the final α values for the di-gamma function?

To scale the answer as we are looking at the whole observation sequence.




