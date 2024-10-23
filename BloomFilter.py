import math
import mmh3
from bitarray import bitarray


class BloomFilter:
    def __init__(self, n=1e6, p=0.01):
        self.__m = math.ceil((-n * math.log(p)) / math.pow(math.log(2), 2))
        self.__l = -math.ceil(math.log(p) / math.log(2))
        self.__array = bitarray(self.__m)
        self.__array.setall(0)

    def add(self, string: str):
        for i in range(self.__l):
            index = mmh3.hash(string, i) % self.__m
            self.__array[index] = 1

    def check(self, string: str):
        for i in range(self.__l):
            index = mmh3.hash(string, i) % self.__m
            if not self.__array[index]:
                return False
        return True
