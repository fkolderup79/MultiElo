class Elo:

    def __init__(self, base, k, e, t_distr, m):
        self.base = base
        self.k = k
        self.e = e
        self.m = m
        self.t_distr = t_distr

    def calculate(self, rate_w, rate_l):
        points = self.k * (1 / (1 + (pow(10, (rate_w - rate_l) / self.e))))
        return points