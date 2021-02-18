'''
Module Name: drawLine
Author: CS3388
DOC: 01-22-2021

Purpose: This class implements the synthetic camera matrix which is used by the wireMesh module to create polygons.

Parameters: 
window, UP, E, G, nearPlane, farPlane, theta
'''

import operator
from math import *
import numpy as np
from matrix import matrix


class cameraMatrix:

    def __init__(self, window, UP, E, G, nearPlane=10.0, farPlane=50.0, theta=90.0):
        self.__UP = UP.normalize()
        self.__E = E
        self.__G = G
        self.__np = nearPlane
        self.__fp = farPlane
        self.__width = window.getWidth()
        self.__height = window.getHeight()
        self.__theta = theta
        self.__aspect = self.__width/self.__height
        self.__npHeight = self.__np*(pi/180.0*self.__theta/2.0)
        self.__npWidth = self.__npHeight*self.__aspect

        Mp = self.__setMp(self.__np, farPlane)
        T1 = self.__setT1(self.__np, self.__theta, self.__aspect)
        S1 = self.__setS1(self.__np, self.__theta, self.__aspect)
        T2 = self.__setT2()
        S2 = self.__setS2(self.__width, self.__height)
        W2 = self.__setW2(self.__height)

        self.__N = (self.__E - self.__G).removeRow(3).normalize()
        self.__U = self.__UP.removeRow(3).crossProduct(self.__N).normalize()
        self.__V = self.__N.crossProduct(self.__U)

        self.__Mv = self.__setMv(self.__U, self.__V, self.__N, self.__E)
        self.__C = W2*S2*T2*S1*T1*Mp
        self.__M = self.__C*self.__Mv

    '''
    Module Name: __setMv
    Author: Gautam Gupta
    DOC: 02-22-2021

    Purpose: The transformation matrix for the camera which operates through a set of transformation

    Parameters: (U, V, N, E)
    U, V, N: A numpy matrix of the custom matrix class. 
                    It consists of 3 rows and 1 column, each containing a value correspondent to the x,y,z plane.
                    U: Right
                    V: Up
                    N: Forward
    E: A numpy matrix of the custom matrix class.
                    It consists of 4 rows and 1 column which contains the intial position (x,y,z) of the camera.

    Output: This method returns the computer view matrix 4x4
    '''

    def __setMv(self, U, V, N, E):
        mv = matrix(np.identity(4))

        # Maintaining the intial rotation of the camera by assinging the identity matrix's 3x3 values
        values = [U, V, N]
        for i in range(0, 3):
            for j in range(0, 3):
                mv.set(i, j, values[i].get(j, 0))

        # Computing and assinging the last column values of the view matrix which is the translated position
        mv.set(0, 3, -(E.get(0, 0) * U.get(0, 0) + E.get(1, 0)
                       * U.get(1, 0) + E.get(2, 0) * U.get(2, 0)))
        mv.set(1, 3, -(E.get(0, 0) * V.get(0, 0) + E.get(1, 0)
                       * V.get(1, 0) + E.get(2, 0) * V.get(2, 0)))
        mv.set(2, 3, -(E.get(0, 0) * N.get(0, 0) + E.get(1, 0)
                       * N.get(1, 0) + E.get(2, 0) * N.get(2, 0)))
        return mv

    '''
    Module Name: __setMp
    Author: Gautam Gupta
    DOC: 02-22-2021

    Purpose: To perform a perspective projection while keeping the pseudo depth quality

    Parameters: (nearPlane, farPlane)
    nearPlane, farPlane: Float values to represent the distance between the planes and the respective plane

    Output: A perspective transformation 4x4 matrix
    '''

    def __setMp(self, nearPlane, farPlane):
        mp = matrix(np.identity(4))
        mp.set(0, 0, nearPlane)
        mp.set(1, 1, nearPlane)
        mp.set(2, 2, -(nearPlane + farPlane) / (farPlane - nearPlane))
        mp.set(2, 3, -2 * (farPlane * nearPlane) / (farPlane - nearPlane))
        mp.set(3, 2, -1)
        mp.set(3, 3, 0)
        return mp

    '''
    Module Name: __setT1
    Author: Gautam Gupta
    DOC: 02-22-2021

    Purpose: To transalate the positional values within the viewing volume between the near plane coordinates and the far plane

    Parameters: (nearPlane, theta, aspect)
    theta: viewing angle
    nearPlane: Float value - distance between camera and the near plane
    aspect: Float value - graphic window/graphic aspect ratio (y/x)


    Output: A 4x4 matrix to apply the translation.
    '''

    def __setT1(self, nearPlane, theta, aspect):
        top = nearPlane * tan(pi/180.0 * theta / 2.0)
        right = aspect * top
        bottom = -top
        left = -right

        t1 = matrix(np.identity(4))
        t1.set(0, 3, -(right + left) / 2.0)
        t1.set(1, 3, -(top + bottom)/2.0)
        return t1

    '''
    Module Name: __setS1
    Author: Gautam Gupta
    DOC: 02-22-2021

    Purpose: To scale the values within the viewing volume between the near plane coordinates and the far plane

    Parameters: (nearPlane, theta, aspect)
    theta: viewing angle
    nearPlane: Float value - distance between camera and the near plane
    aspect: Float value - graphic window/graphic aspect ratio (y/x)


    Output: A 4x4 matrix to apply the scaling
    '''

    def __setS1(self, nearPlane, theta, aspect):
        top = nearPlane * tan(pi/180.0 * theta / 2.0)
        right = aspect * top
        bottom = -top
        left = -right

        s1 = matrix(np.identity(4))
        s1.set(0, 0, 2.0/(right - left))
        s1.set(1, 1, 2.0/(top - bottom))
        return s1

    '''
    Module Name: __setT2
    Author: Gautam Gupta
    DOC: 02-22-2021

    Purpose: Translates the x, y position coordinates to the positive quadrant

    Parameters: N/A

    Output: A 4x4 matrix to apply the translation
    '''

    def __setT2(self):
        t2 = matrix(np.identity(4))
        t2.set(0, 3, 1.0)
        t2.set(1, 3, 1.0)
        return t2

    '''
    Module Name: __setS2
    Author: Gautam Gupta
    DOC: 02-22-2021

    Purpose: Scales the translated coordinates such that they fit in the defined space of the graphic window

    Parameters: (width, height)
    width, height: The respective values of the graphic window/canvas.
    
    Output: A 4x4 matrix to apply the transformation
    '''

    def __setS2(self, width, height):
        s2 = matrix(np.identity(4))
        s2.set(0, 0, width/2.0)
        s2.set(1, 1, height/2.0)
        return s2

    '''
    Module Name: __setW2
    Author: Gautam Gupta
    DOC: 02-22-2021

    Purpose: A supporting method to the S2 and the T2 transformations which converts the operations to screen coordinates

    Parameters: (height)
    height: The value of the graphic window/canvas height.

    Output: A 4x4 matrix to apply the transformation
    '''

    def __setW2(self, height):
        w2 = matrix(np.identity(4))
        w2.set(1, 1, -1.0)
        w2.set(1, 3, height)
        return w2

    def worldToViewingCoordinates(self, P):
        return self.__Mv*P

    def worldToImageCoordinates(self, P):
        return self.__M*P

    def worldToPixelCoordinates(self, P):
        return self.__M*P.scalarMultiply(1.0/(self.__M*P).get(3, 0))

    def viewingToImageCoordinates(self, P):
        return self.__C*P

    def viewingToPixelCoordinates(self, P):
        return self.__C*P.scalarMultiply(1.0/(self.__C*P).get(3, 0))

    def imageToPixelCoordinates(self, P):
        return P.scalarMultiply(1.0/P.get(3, 0))

    def getUP(self):
        return self.__UP

    def getU(self):
        return self.__U

    def getV(self):
        return self.__V

    def getN(self):
        return self.__N

    def getE(self):
        return self.__E

    def getG(self):
        return self.__G

    def getMv(self):
        return self.__Mv

    def getC(self):
        return self.__C

    def getM(self):
        return self.__M

    def getNp(self):
        return self.__np

    def getFp(self):
        return self.__fp

    def getTheta(self):
        return self.__theta

    def getAspect(self):
        return self.__aspect

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getNpHeight(self):
        return self.__npHeight

    def getNpWidth(self):
        return self.__npWidth
