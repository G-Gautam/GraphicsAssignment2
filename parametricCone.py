'''
Module Name: parametricCone
Author: Gautam Gupta
Student #: 250897104
DOC: 01-22-2021

Purpose: To compute and return the set of points to create a cone

Parameters: parametricObject, height, radius
parametricObject: A base class which defines the properties for all 3d objects such as the position matrix, color, reflectance, u&v range, and uvDelta
height, radius: Respective float values for the cone's target radius and height
'''

from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject


class parametricCone(parametricObject):
    def __init__(self, T=matrix(np.identity(4)), height=10.0,  radius=10.0, color=(0, 0, 255), reflectance=(0.2, 0.4, 0.4, 1.0), uRange=(0.0, 1.0), vRange=(0.0, 2*pi), uvDelta=(pi/18.0, pi/18.0)):
        super().__init__(T, color, reflectance, uRange, vRange, uvDelta)
        self.__radius = radius
        self.__height = height

    '''
    Purpose: To compute a position matrix for the points in the 2-d space

    Parameters: u, v: Respective points in the 2-D space

    Output: A 4x1 position vector (matrix) for the points on the cone's surface
    '''
    def getPoint(self, u, v):
        P = matrix(np.ones((4, 1)))
        P.set(0, 0, self.__radius * (1 - u) * sin(v))
        P.set(1, 0, self.__radius * (1 - u) * cos(v))
        P.set(2, 0, self.__height * u)
        return P

    '''
    Purpose: These methods are the setters and getters for the class parameters radius and height

    Parameters: radius, height: Respective float values for the cone's target radius and height
    '''
    def setRadius(self, radius):
        self.__radius = radius

    def setHeight(self, height):
        self.__height = height

    def getRadius(self):
        return self.__radius

    def getHeight(self):
        return self.__height
