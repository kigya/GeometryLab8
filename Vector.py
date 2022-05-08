from math import *

from Point import Point


class Vector:
    def __init__(self, point1, point2):
        if type(point1) == Point:
            self.x = point2.x - point1.x
            self.y = point2.y - point1.y
        else:
            self.x = point1
            self.y = point2

    def __str__(self):
        return '[' + str(self.x) + ', ' + str(self.y) + ']'

    @staticmethod
    def get_length(p1, p2):
        return sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

    @staticmethod
    def scalar_product(v1, v2):
        return v1.x * v2.x + v1.y * v2.y

    @staticmethod
    def get_vector(alpha, speed = 1):
        return Vector(speed * cos(alpha), speed * sin(alpha)), speed

    @staticmethod
    def s_mult(v, scalar):
        new_vector = Vector(v.x * scalar, v.y * scalar)
        return new_vector

    @staticmethod
    def s_minus(v1, v2):
        new_vector = Vector(v1.x - v2.x, v1.y - v2.y)
        return new_vector

    def print(self):
        print('[' + str(self.x) + ', ' + str(self.y) + ']')