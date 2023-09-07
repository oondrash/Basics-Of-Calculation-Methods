import numpy as np


def random_matrix(a0):
    from random import random

    return np.array([[int(100 * random()) for _ in range(a0)] for _ in range(a0)]), np.array(
        [[int(100 * random())] for _ in range(a0)])


def gillbert_matrix(a0):
    return np.array([[1 / (i + j - 1) for i in range(1, a0 + 1)] for j in range(1, a0 + 1)]), np.array(
        [[1 / (i + 1)] for i in range(a0)])


def test(a0):
    m = np.array([[1 / (i + j - 1) for i in range(1, a0 + 1)] for j in range(1, a0 + 1)])
    return m, np.dot(m, np.ones((a0, 1)))


class GaussMethod(object):
    def __init__(self, matrix, vector, size=3):
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
        self.log_input_data()

    def log_input_data(self):
        print("Метод Гаусса")
        print("=============================================")
        print("Вхідні дані:")
        print("Матриця A:")
        print(self.matrix.view())
        print("Вектор b:")
        print(self.vector.view())

    def calculate_m_k(self, k, a_k):
        """Calculate matrix M_k"""
        m_k = np.array((np.eye(self.size)))
        for i in range(self.size):
            for j in range(self.size):
                if i == k and j == k:
                    m_k[i][j] = 1 / a_k[i][j]
                elif i > k and j == k:
                    m_k[i][j] = -(a_k[i][j] / a_k[k][k])
                elif i < k and j == k:
                    m_k[i][j] = 0
        return m_k

    def calculate_p_k(self, a_k):
        """Calculate matrix P_k"""
        p_k = np.array((np.eye(self.size)))
        a_k_max = a_k.max()
        a_k_min = a_k.min()
        a_k_max_by_abs = max(abs(a_k_max), abs(a_k_min))
        sign = 1 if a_k_max == a_k_max_by_abs or a_k_min == a_k_max_by_abs else -1
        index_max = [np.where(a_k == sign*a_k_max_by_abs)[0][0], np.where(a_k == sign*a_k_max_by_abs)[1][0]]
        p_k[[index_max[0], index_max[1]]] = p_k[[index_max[1], index_max[0]]]
        return p_k

    @staticmethod
    def calculate_a_k(a_k, b_k, p_k, m_k):
        """Calculate matrix A_k"""
        return np.dot(np.dot(m_k, p_k), a_k), np.dot(np.dot(m_k, p_k), b_k)

    def log_step(self, k, a_k, b_k, p_k, m_k):
        print("=============================================")
        print("Ітерація №{}".format(k))
        print("Матриця P_{}:".format(k))
        print(p_k.view())
        print("Матриця M_{}:".format(k))
        print(m_k.view())
        print("Матриця A_{}:".format(k))
        print(a_k.view())

    def log_output_matrix(self, a_k, b_k, result):
        print("=============================================")
        print("Вихідні дані:")
        print("Матриця A:")
        print(a_k.view())
        print("Вектор b:")
        print(b_k.view())
        print("Розв'язок системи:")
        print(result)

    def solve_system(self, a_k, b_k):
        from sympy import Matrix, solve_linear_system, symbols
        a_k, b_k = a_k, b_k
        a = np.append(a_k, b_k, axis=1)
        result = np.linalg.solve(a_k, b_k)
        return result

    def solve(self):

        a_k = self.matrix
        b_k = self.vector
        result = None
        for i in range(self.size):
            p_k = self.calculate_p_k(a_k)
            m_k = self.calculate_m_k(i, np.dot(p_k, a_k))
            a_k, b_k = self.calculate_a_k(a_k, b_k, p_k, m_k)
            result = self.solve_system(a_k, b_k)
            self.log_step(i, a_k, b_k, p_k, m_k)
        self.log_output_matrix(a_k, b_k, result)
        return a_k, b_k


# a = np.array([[10, 0, 3], [3, -1, 0], [-2, 4, 1]])
# b = np.array([[7], [2], [1]])
# method = GaussMethod('gillbert', 'gillbert', 3)
# method.solve()

m, v = test(100)
print(m)
print(v)
method = GaussMethod(m, v)
method.solve()
