#!/usr/bin/env python3

from picture import Picture
from math import sqrt,pow

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        # calculation for x
        if (i-1 < 0):
            leftVal = self[self.width()-1,j]
        else:
            leftVal = self[i-1,j]

        if (i+1 == self.width()):
            rightVal = self[0,j]
        else:
            rightVal = self[i+1,j]

        left_r,left_g,left_b = leftVal
        right_r,right_g,right_b = rightVal
        xEnergy = pow(abs(right_r-left_r),2) + pow(abs(right_g-left_g),2) + pow(abs(right_b-left_b),2)
        
        # calculation for y
        if (j-1 < 0):
            topVal = self[i,self.height()-1]
        else:
            topVal = self[i,j-1]
        
        if (i+1 == self.height()):
            bottomVal = self[0,j]
        else:
            bottomVal = self[i,j+1]
        
        top_r,top_g,top_b = topVal
        bottom_r,bottom_g,bottom_b = bottomVal
        yEnergy = pow(abs(top_r-bottom_r),2) + pow(abs(top_g-bottom_g),2) + pow(abs(top_b-bottom_b),2)

        return sqrt(xEnergy+yEnergy)

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        raise NotImplementedError

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        if Picture.width() == 1:
            raise SeamError("SeamError: Width is equal to 1.")
        raise NotImplementedError

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        if Picture.height() == 1:
            raise SeamError("SeamError: Height is equal to 1.")
        raise NotImplementedError

class SeamError(Exception):
    pass
