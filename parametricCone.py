from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject


class parametricCone(parametricObject):
    def __init__(self, T=matrix(np.identity(4)), height=10.0,  radius=10.0, color=(0, 0, 255), reflectance=(0.2, 0.4, 0.4, 1.0), uRange=(0.0, 1.0), vRange=(0.0, 2*pi), uvDelta=(pi/18.0, pi/18.0)):
        super().__init__(T, color, reflectance, uRange, vRange, uvDelta)
        self.__radius = radius
        self.__height = height

    def getPoint(self, u, v):
        P = matrix(np.ones((4, 1)))
        P.set(0, 0, self.__radius * (1 - u) * sin(v))
        P.set(1, 0, self.__radius * (1 - u) * cos(v))
        P.set(2, 0, self.__height * u)
        return P

    def setRadius(self, radius):
        self.__radius = radius

    def setHeight(self, height):
        self.__height = height

    def getRadius(self):
        return self.__radius

    def getHeight(self):
        return self.__height
