import operator
from math import *
import numpy as np
from matrix import matrix

class cameraMatrix:

    def __init__(self,window,UP,E,G,nearPlane=10.0,farPlane=50.0,theta=90.0):
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

        Mp = self.__setMp(self.__np,farPlane)
        T1 = self.__setT1(self.__np,self.__theta,self.__aspect)
        S1 = self.__setS1(self.__np,self.__theta,self.__aspect)
        T2 = self.__setT2()
        S2 = self.__setS2(self.__width,self.__height)
        W2 = self.__setW2(self.__height)

        self.__N = (self.__E - self.__G).removeRow(3).normalize()
        self.__U = self.__UP.removeRow(3).crossProduct(self.__N).normalize()
        self.__V = self.__N.crossProduct(self.__U)

        self.__Mv = self.__setMv(self.__U,self.__V,self.__N,self.__E)
        self.__C = W2*S2*T2*S1*T1*Mp
        self.__M = self.__C*self.__Mv

    def __setMv(self,U,V,N,E):
        mv = matrix(np.identity(4))
        values = [U, V, N]
        for i in range(0, 3):
            for j in range(0, 3):
                mv.set(i, j, values[j].get(j, 0))

        mv.set(0,3,-( E.get(0,0) * U.get(0,0) + E.get(1,0) * U.get(1,0) + E.get(2,0) * U.get(2,0)))
        mv.set(1,3,-( E.get(0,0) * V.get(0,0) + E.get(1,0) * V.get(1,0) + E.get(2,0) * V.get(2,0)))
        mv.set(2,3,-( E.get(0,0) * N.get(0,0) + E.get(1,0) * N.get(1,0) + E.get(2,0) * N.get(2,0)))
        return mv
        
    def __setMp(self,nearPlane,farPlane):
        mp = matrix(np.identity(4))
        mp.set(0,0, nearPlane)
        mp.set(1,1, nearPlane)
        mp.set(2,2,-( nearPlane + farPlane ) / ( farPlane - nearPlane ))
        mp.set(2,3,-2 * (farPlane * nearPlane) / (farPlane - nearPlane))
        mp.set(3,2,-1)
        mp.set(3,3,0)
        return mp

    def __setT1(self,nearPlane,theta,aspect):
        top = nearPlane * tan(pi/180.0 * theta / 2.0)
        right = aspect * top
        bottom = -top
        left = -right
        t1 = matrix(np.identity(4))
        t1.set(0,3, -(right + left) / 2.0)
        t1.set(1,3,-(top + bottom)/2.0)
        return t1
        
    def __setS1(self,nearPlane,theta,aspect):
        # calculate top, right, bottom, left (t,r,b,l)
        top = nearPlane * tan(pi/180.0 * theta / 2.0)
        right = aspect * top
        bottom = -top
        left = -right
        #create a 4*4 identity matrix
        __S1 = matrix(np.identity(4))
        #set values
        __S1.set(0,0,2.0/(right - left))
        __S1.set(1,1,2.0/(top - bottom))
        #return S1
        return __S1

    def __setT2(self):
        #create a 4*4 identity matrix
        __T2 = matrix(np.identity(4))
        #set values
        __T2.set(0,3,1.0)
        __T2.set(1,3,1.0)
        #return T2
        return __T2
        
    def __setS2(self,width,height):
        #create a 4*4 identity matrix
        __S2 = matrix(np.identity(4))
        #set values
        __S2.set(0,0,width/2.0)
        __S2.set(1,1,height/2.0)
        #return s2
        return __S2
        
    def __setW2(self,height):
        #Complete this method
        #create a 4*4 identity matrix
        __W2 = matrix(np.identity(4))
        #set values
        __W2.set(1,1,-1.0)
        __W2.set(1,3, height)
        #return w2
        return __W2
        
    def worldToViewingCoordinates(self,P):
        return self.__Mv*P

    def worldToImageCoordinates(self,P):
        return self.__M*P

    def worldToPixelCoordinates(self,P):
        return self.__M*P.scalarMultiply(1.0/(self.__M*P).get(3,0))

    def viewingToImageCoordinates(self,P):
        return self.__C*P

    def viewingToPixelCoordinates(self,P):
        return self.__C*P.scalarMultiply(1.0/(self.__C*P).get(3,0))

    def imageToPixelCoordinates(self,P):
        return P.scalarMultiply(1.0/P.get(3,0))

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