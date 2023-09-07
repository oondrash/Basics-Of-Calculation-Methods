import numpy as np


def random_matrix(a0):
    from random import random

    return np.array([[int(100 * random()) for _ in range(a0)] for _ in range(a0)]), np.array(
        [[int(100 * random())] for _ in range(a0)])


def gillbert_matrix(a0):
    return np.array([[1 / (i + j - 1) for i in range(1, a0 + 1)] for j in range(1, a0 + 1)]), np.array(
        [[1 / (i + 1)] for i in range(a0)])


class Jacobi(object):
    def __init__(self, matrix, vector, size=3, eps=0.0001):
        if str(matrix) == "random":
            self.matrix = random_matrix(size)[0]
        elif str(matrix) == "gillbert":
            self.matrix = gillbert_matrix(size)[0]
        else:
            self.matrix = matrix
        if str(vector) == "random":
            self.vector = random_matrix(size)[1]
            self.size = size
        elif str(vector) == "gillbert":
            self.vector = gillbert_matrix(size)[1]
            self.size = size
        else:
            self.vector = vector
            self.size = len(vector)
        self.eps = eps
        self.log_input_data()

    def log_input_data(self):
        print("Метод Якобі")
        print("=============================================")
        print("Вхідні дані:")
        print("Матриця A:")
        print(self.matrix.view())
        print("Вектор b:")
        print(self.vector.view())
        print("Точність eps:")
        print(self.eps)

    def log_step(self, i, x, x_next, q):
        print("Ітерація №", i)
        print()
        print("x:")
        print(x.view())
        print("x_next:")
        print(x_next.view())
        print("||x_next - x|| / (1 - q) * q:")
        print(np.linalg.norm(x_next - x) / ((1 - q) * q))
        print("||x_next - x|| > eps * ((1 - q) / q):")
        print(np.linalg.norm(x_next - x) > self.eps * ((1 - q) / q))
        print("=============================================")

    def log_result(self, result):
        print("Результат:")
        print(result.view())
        print("=============================================")

    @staticmethod
    def enter_condition(self, q):
        if q < 1:
            print("Умова збіжності виконується")
            return True
        print("Умова збіжності не виконується")
        return False

    def finish_condition(self, x1, x2, q):

        if np.linalg.norm(x2 - x1) > self.eps * ((1 - q) / q):
            return False
        return True

    def solve(self):
        D = np.diag(np.diag(self.matrix))
        U = np.tril(self.matrix - D)
        L = np.triu(self.matrix - D)
        B = np.dot(-np.linalg.inv(D), L + U)
        q = np.linalg.norm(B, ord=np.inf)
        if not self.enter_condition(self, q):
            return None
        n = int((np.log((1 - q) * self.eps)) / np.log(q)) + 1
        print("Визначена кількість ітерацій:", n)
        x = np.zeros((self.size, 1))
        x_next = np.array([[self.vector[i][0] / self.matrix[i][i]] for i in range(self.size)])
        i = 0
        while not self.finish_condition(x, x_next, q):
            i += 1
            self.log_step(i, x, x_next, q)
            x = x_next
            x_next = np.dot(B, x) + np.array([[self.vector[i][0] / self.matrix[i][i]] for i in range(self.size)])
        self.log_result(x_next)
        return x_next


a = np.array([[3, -1, 1], [-1, 2, 0.5], [1, 0.5, 3]])
b = np.array([[1], [1.75], [2.5]])
eps = 0.001
method = Jacobi(a, b, eps=eps)
method.solve()
