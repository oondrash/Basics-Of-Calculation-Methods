import numpy as np
from numpy import linalg as la


def jacobi(A, b, ep, x0, Imax):
    M = np.diag(np.diag(A))
    E = (-1) * np.tril(A - M)
    F = (-1) * np.triu(A - M)
    N = E + F
    iter = 0
    x = x0
    print(np.dot(np.linalg.inv(M),N))
    while iter < 29:
        iter = iter + 1

        x = np.dot(np.linalg.inv(M), np.dot(N, x) + b)  # approached solution
        x_e = np.linalg.solve(A, b)  # exact solution
        err = la.norm(x_e - x)  # error
    return [x, x_e, err, iter]


ep, Imax, x0 = 0.001, 1000, np.zeros(3)
A = np.array([[3, -1, 1], [-1, 2, 0.5], [1, 0.5, 3]])
b = np.array([[1], [1.75], [2.5]])

l  = jacobi(A, b, ep, x0, Imax)
print(l)
