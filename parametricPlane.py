'''
Module Name: parametricPlane
Author: Gautam Gupta
Student #: 250897104
DOC: 01-22-2021

Purpose: To compute and return the set of points to create a plane

Parameters: parametricObject, width, height
parametricObject: A base class which defines the properties for all 3d objects such as the position matrix, color, reflectance, u&v range, and uvDelta
width, height: Respective float values for the plane's target width and height
'''

from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject


class parametricPlane(parametricObject):
    def __init__(self, T=matrix(np.identity(4)), width=10.0, height=10.0, color=(255, 255, 0), reflectance=(0.2, 0.4, 0.4, 1.0), uRange=(0.0, 1.0), vRange=(0.0, 1.0), uvDelta=(1.0/10.0, 1.0/10.0)):
        super().__init__(T, color, reflectance, uRange, vRange, uvDelta)
        self.__width = width
        self.__height = height

    '''
    Purpose: To compute a position matrix for the points in the 2-d space

    Parameters: u, v: Respective points in the 2-D space

    Output: A 4x1 position vector (matrix) for the points on the plane's surface
    '''
    def getPoint(self, u, v):
        P = matrix(np.ones((4, 1)))
        P.set(0, 0, self.__width * u)
        P.set(1, 0, self.__height * v)
        P.set(2, 0, 0)
        return P

    '''
    Purpose: These methods are the setters and getters for the class parameters width and height

    Parameters: width, height: Respective float values for the plane's target width and height
    '''
    def setWidth(self, width):
        self.__width = width

    def setHeight(self, height):
        self.__height = height

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height
