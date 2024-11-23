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
        # stores the indices corresponding to the minimum energy
        vertical_seam = []
        min_path = {}

        for j in range (self.height()):
            for i in range(self.width()):
                if j == 0:
                    min_path[i,j] = self.energy(i,j)
                else:
                    # get energy of: top-left, directly above, and top-right values, provided they are within range
                    if i > 0:
                        top_left = min_path[i-1,j-1]
                    else:
                        top_left = 1e20
                    
                    directly_above = min_path[i,j-1]

                    if i < self.width() - 1:
                        top_right = min_path[i+1,j-1]
                    else:
                        top_right = 1e20
                    
                    min_val = min(top_left,directly_above,top_right)
                    min_path[i,j] = min_val + self.energy(i,j)
            
        # get minimum energy at height - 1
        min_energy_at_bottom = []
        for i in range(self.width()):
            min_energy_at_bottom.append(min_path[i,self.height() - 1])
        vertical_seam.append(min_energy_at_bottom.index(min(min_energy_at_bottom)))

        # backtrack to get the indexes
        for i in range(2,self.height()+1,1):
            x = vertical_seam[len(vertical_seam)-1] ## get the x-index of the last value

            if x > 0:
                top_left = min_path[x-1,(self.height()-i)]
            else:
                top_left = 1e20
                    
            directly_above = min_path[x,(self.height()-i)]

            if x < self.width() - 1:
                top_right = min_path[x+1,(self.height()-i)]
            else:
                top_right = 1e20

            temp_arr = [top_left,directly_above,top_right]

            temp_val = 0
            for j in range(len(temp_arr)):
                if j == 0:
                    temp_val = temp_arr[j]
                else:
                    if temp_arr[j] < temp_val:
                        temp_val = temp_arr[j]
            
            if temp_val == top_left:
                vertical_seam.append(x-1)
            elif temp_val == directly_above:
                vertical_seam.append(x)
            else: # equal to top_right
                vertical_seam.append(x+1)

        vertical_seam.reverse()
        return vertical_seam

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''

        

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        if self.width() == 1:
            raise SeamError("SeamError: Width is equal to 1.")

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        if self.height() == 1:
            raise SeamError("SeamError: Height is equal to 1.")

class SeamError(Exception):
    pass
