import random

class Sensores:
    def __init__(self, name, bounds, integer=False, gauss=False, mean=None, sigma=None):
        self.__name = name
        self.__bounds = bounds
        self.__integer = integer
        self.__gaus = gauss
        self.__mean = mean
        self.__sigma = sigma

    def getNome(self):
        return self.__name

    def getValor(self):
        valor = None
        if self.__integer:
            valor = random.randint(self.__bounds[0], self.__bounds[1])
        elif self.__gaus:
            valor = random.gauss(self.__mean, self.__sigma)
        else:
            valor = random.uniform(self.__bounds[0], self.__bounds[1])
        return valor