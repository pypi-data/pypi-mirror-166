import math

from .point import Point
from .line import Line


class Triangle:
    def __init__(self, point1: Point, point2: Point, point3: Point):
        self.__first_point = point1
        self.__second_point = point2
        self.__third_point = point3

        self.__first_line = Line(point1, point2)
        self.__second_line = Line(point1, point3)
        self.__third_line = Line(point2, point3)

    def perimeter(self):
        return round(self.__first_line.length() + self.__second_line.length() + self.__third_line.length(), 4)

    def square(self):
        l1 = self.__first_line.length()
        l2 = self.__second_line.length()
        l3 = self.__third_line.length()
        p = (l1 + l2 + l3) / 2
        return round(math.sqrt(p * (p - l1) * (p - l2) * (p - l3)), 4)
