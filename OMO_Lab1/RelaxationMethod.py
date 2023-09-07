from sympy import *
import inspect


class RelaxationMethod(object):
    def __init__(self, f, a, b, eps):
        self.f = lambdify(symbols('x'), f)
        self.df = lambdify(symbols('x'), diff(f, symbols('x')))
        self.df_sympy = diff(f, symbols('x'))
        self.a = a
        self.b = b
        self.eps = eps
        self.tau_opt = 0
        self.x1 = 0
        self.x0 = 0
        self.k = 0
        self.increasing = None
        self.log_input_data()

    def count_tau_opt(self):
        self.critical_points = list(filter(lambda x: self.a <= x <= self.b, solve(self.df_sympy)))
        if len(self.critical_points) > 0:
            print("Умова знакосталості не задовільняється")
            return 0
        c = (self.b - self.a) / 2
        if self.df(c) > 0:
            self.increasing = True
            self.tau_opt = - 2 / (self.df(self.a) + self.df(self.b))
            return self.tau_opt
        else:
            self.increasing = False
            self.tau_opt = 2 / (self.df(self.a) + self.df(self.b))
            return self.tau_opt

    def set_x0(self):
        self.x0 = (self.b - self.a) / 2
        return self.x0

    def log_input_data(self):
        print("Метод Релаксації")
        print("=============================================")
        print("Вхідні дані:")
        print("{}".format(inspect.getsource(self.f)).replace("_lambdifygenerated", "f"))
        print("a = {}".format(self.a))
        print("b = {}".format(self.b))
        print("eps = {}".format(self.eps))
        print("=============================================")
        print("Отриманa похіднa функції:")
        print("{}".format(inspect.getsource(self.df)).replace("_lambdifygenerated", "df"))
        print("=============================================")
        print("Визначення оптимального кроку:")
        print("tau_opt = {}".format(self.count_tau_opt()))
        print("=============================================")
        print("Визначення початкового значення:")
        print("x0 = (a+b)/2 = {}".format(self.set_x0()))

    def converge(self):
        """
        Перевірка умови збіжності
        """
        if self.increasing:
            c = self.b
        else:
            c = self.a
        if self.tau_opt * self.df(c) < 1:
            print("=============================================")
            print("Проста умова збіжності задовільняється")
            return True
        else:
            print("=============================================")
            print("Проста умова збіжності не задовільняється")
            return False

    def accuracy_check(self):
        """
        Перевірка точності
        """
        return abs(self.x1 - self.x0) < self.eps

    def log_result(self):
        print("=============================================")
        print(f"Розв'язок знайдено на ітерації {self.k}: ")
        print(f"x = {format(self.x1, '.10f')}")
        print(f"Перевірка точності: ")
        print(f"{format(abs(self.x1 - self.x0), '.10f')} < {format(self.eps, '.10f')}")

    def solve(self):
        if self.converge() and self.tau_opt != 0:
            self.x1 = self.x0 + self.tau_opt * (self.f(self.x0))
            self.k += 1
            while not self.accuracy_check():
                self.k += 1
                self.x0 = self.x1
                self.x1 = self.x0 + self.tau_opt * (self.f(self.x0))
            self.log_result()
            return self.x1



x = symbols('x')
f = x ** 2 - 4

RelaxationMethod(f, 1, 3, 0.0001).solve()
