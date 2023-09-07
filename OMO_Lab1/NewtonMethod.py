from sympy import *
import inspect


class NewtonMethod(object):
    def __init__(self, f, a, b, eps):
        self.f = lambdify(symbols('x'), f)
        self.df = lambdify(symbols('x'), diff(f, symbols('x')))
        self.ddf = lambdify(symbols('x'), diff(f, symbols('x'), symbols('x')))
        self.a = a
        self.b = b
        self.eps = eps
        self.x0 = 0
        self.x1 = 0
        self.k = 0
        self.log_input_data()

    def converge(self):
        """
        Перевірка умови збіжності
        """
        if self.f(self.a) * self.ddf(self.a) > 0:
            print("Умова збіжності задовільняється для а.")
            self.x0 = self.a
            return True
        elif self.f(self.b) * self.ddf(self.b) > 0:
            print("Умова збіжності задовільняється для b.")
            self.x0 = self.b
            return True
        else:
            print("Умова збіжності не задовільняється.")
            return False

    def accuracy_check(self):
        """
        Перевірка точності
        """
        return abs(self.x1 - self.x0) < self.eps

    def log_input_data(self):
        print("Метод Ньютона")
        print("=============================================")
        print("Вхідні дані:")
        print("{}".format(inspect.getsource(self.f)).replace("_lambdifygenerated", "f"))
        print("a = {}".format(self.a))
        print("b = {}".format(self.b))
        print("eps = {}".format(self.eps))

        print("=============================================")
        print("Отримані похідні функції:")
        print("{}".format(inspect.getsource(self.df)).replace("_lambdifygenerated", "df"))
        print("{}".format(inspect.getsource(self.ddf)).replace("_lambdifygenerated", "ddf"))

    def log_result(self):
        print("=============================================")
        print(f"Розв'язок знайдено на ітерації {self.k}: ")
        print(f"x = {format(self.x1, '.10f')}")
        print(f"Перевірка точності: ")
        print(f"{format(abs(self.x1-self.x0), '.10f')} < {format(self.eps, '.10f')}")

    def solve(self):
        if self.converge():
            self.x1 = self.x0 - self.f(self.x0) / self.df(self.x0)
            self.k += 1
            while not self.accuracy_check():
                self.k +=1
                self.x0 = self.x1
                self.x1 = self.x0 - self.f(self.x0) / self.df(self.x0)
            self.log_result()
            return self.x1


x = symbols('x')
f = cos(2 / x) - 2 * sin(1 / x) + 1 / x
NewtonMethod(f, 1.8, 2, 0.0001).solve()
