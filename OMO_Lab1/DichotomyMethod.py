from sympy import *
import inspect


class DichotomyMethod(object):
    def __init__(self, function, a, b, eps):
        self.f = lambdify(symbols('x'), function)
        self.a = a
        self.b = b
        self.eps = eps
        self.c = 0
        self.k = 0
        self.converge_speed = 0
        self.log_input_data()

    def converge(self):
        """
        Перевірка умови збіжності
        """
        if self.f(self.a) * self.f(self.b) < 0:
            print("Умова збіжності задовільняється.")
            return True
        else:
            print("Умова збіжності не задовільняється.")
            return False

    def accuracy_check(self):
        """
        Перевірка точності
        """
        return abs(self.b - self.a) < self.eps

    def log_input_data(self):
        print("Метод Дихтомії")
        print("=============================================")
        print("Вхідні дані:")
        print("{}".format(inspect.getsource(self.f)).replace("_lambdifygenerated", "f"))
        print("a = {}".format(self.a))
        print("b = {}".format(self.b))
        print("eps = {}".format(self.eps))

    def get_converge_speed(self):
        self.converge_speed = (self.b - self.a) / 2 ** self.k
        return self.converge_speed

    def log_result(self):
        print("=============================================")
        print(f"Розв'язок знайдено на ітерації {self.k}: ")
        print(f"x = {format(self.c, '.10f')}")
        print(f"f(x) = {format(self.f(self.c),'.10f')}")
        print(f"Перевірка точності: ")
        print(f"{format(self.f(self.b) - self.f(self.a), '.10f')} < {format(self.eps, '.10f')}")

    def solve(self):
        if self.converge():
            self.k = 0
            while not self.accuracy_check():
                self.k += 1
                self.c = (self.a + self.b) / 2
                if self.f(self.c) * self.f(self.a) < 0:
                    self.b = self.c
                if self.f(self.c) * self.f(self.b) < 0:
                    self.a = self.c
                if self.f(self.c) == 0:
                    self.log_result()
                    return self.c
            self.log_result()
            return self.c


x = symbols('x')
f = cos(2 / x) - 2 * sin(1 / x) + 1 / x
DichotomyMethod(f, 1.8, 2, 0.0001).solve()
