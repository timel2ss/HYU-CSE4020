import numpy as np

# A. Create a 1d array M with values ranging from 2 to 26 and print M
M = np.arange(2, 27)
print(M)

# B. Reshape M as a 5x5 matrix and print M.
M = M.reshape(5, 5)
print(M)

# C. Set the value of inner elements of the matrix M to 0 and print
M[1:4, 1:4] = 0
print(M)

# D. Assign M^2 to the M and print M.
M = M @ M
print(M)

# E. Lets call the first row of the matrix M a vector v.
# Calculate the magnitude of the vector v and print it.
v = M[0, :]
magnitude = np.sqrt(v @ v)
print(magnitude)