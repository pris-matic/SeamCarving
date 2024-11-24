#!/usr/bin/env python3

from picture import Picture
from math import sqrt,pow
from PIL import Image

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        
        if ((i < 0 or i >= self.width()) or (j < 0 or j >= self.height())):
            raise IndexError("Index out of bounds.")

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
        
        if (j+1 == self.height()):
            bottomVal = self[i,0]
        else:
            bottomVal = self[i,j+1]
        
        top_r,top_g,top_b = topVal
        bottom_r,bottom_g,bottom_b = bottomVal
        yEnergy = pow(abs(bottom_r-top_r),2) + pow(abs(bottom_g-top_g),2) + pow(abs(bottom_b-top_b),2)

        return sqrt(xEnergy+yEnergy)

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        
        min_energy = {} # stores the minimum cumulative energy
        min_path = {} # stores the path leading to the minimum cumulative energy

        for j in range (self.height()):
            for i in range(self.width()):
                if j == 0:
                    min_energy[i,j] = self.energy(i,j)
                    min_path[i,j] = 0
                else:
                    # get energy of: top-left, directly above, and top-right values, provided they are within range
                    if i > 0:
                        top_left = min_energy[i-1,j-1]
                    else:
                        top_left = 1e20
                    
                    directly_above = min_energy[i,j-1]

                    if i < self.width() - 1:
                        top_right = min_energy[i+1,j-1]
                    else:
                        top_right = 1e20
                    
                    movement = [top_left,directly_above,top_right]
                    min_val = min(movement)
                    min_energy[i,j] = min_val + self.energy(i,j)
                    min_path[i,j] = movement.index(min_val) - 1
            
        # get minimum energy at height - 1
        min_val = 1e20
        x_pos = 0
        for i in range(self.width()):
            if min_energy[i, self.height()-1] < min_val:
                min_val = min_energy[i, self.height()-1]
                x_pos = i

        vertical_seam = [] # stores the indices corresponding to the minimum energy

        # backtrack to get the indexes

        for j in range (self.height()-1,-1,-1):
            vertical_seam.append(x_pos)
            if j > 0:
                x_pos += min_path[x_pos,j]

        vertical_seam.reverse()
        print(len(vertical_seam))
        return vertical_seam

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        img = SeamCarver(self.picture().transpose(Image.Transpose.ROTATE_90))
        horizontal_seam = img.find_vertical_seam()
        
        return horizontal_seam
    
    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        for i in range(len(seam)-1):
            if abs(seam[i]-seam[i+1])>1:
                raise SeamError("SeamError: Invalid seam.")
        if (len(seam) != self.height()):
            raise SeamError("SeamError: Seam is not equal to the height.")
        if self.width() == 1:
            raise SeamError("SeamError: Width is equal to 1.")
        
        for j in range(self.height()): 
            to_remove = seam[j] 
            
            for i in range(to_remove, self.width() - 1):
                self[i, j] = self[i + 1, j]
            
            del self[self.width() - 1, j]

        self._width -= 1

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        for i in range(len(seam)-1):
            if abs(seam[i]-seam[i+1])>1:
                raise SeamError("SeamError: Invalid seam.")
        if (len(seam) != self.width()):
            raise SeamError("SeamError: Seam is not equal to the width.")
        if self.height() == 1:
            raise SeamError("SeamError: Height is equal to 1.")

        img = SeamCarver(self.picture().transpose(Image.Transpose.ROTATE_90))
        seam.reverse()
        img.remove_vertical_seam(seam)
            
        new_img = img.picture().transpose(Image.Transpose.ROTATE_270)
        self.__init__(new_img)

class SeamError(Exception):
    pass
