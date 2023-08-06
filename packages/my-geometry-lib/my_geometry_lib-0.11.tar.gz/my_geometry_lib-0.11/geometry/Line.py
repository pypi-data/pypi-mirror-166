import math
from .point import Point


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.__first_point = point1
        self.__second_point = point2

    def length(self):
        return round(math.sqrt(pow(abs(self.__second_point.x - self.__first_point.x), 2) + pow(
            abs(self.__second_point.y - self.__first_point.y), 2)), 4)
