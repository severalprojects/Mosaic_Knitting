#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 10:10:22 2019

@author: jsw
"""

#take a string (of the right length) and convert it into a 2D list 
def strTo2D(string, rows, cols): 
    if len(string) != (rows*cols):
        print("error: string doesn't have {} characters".format(rows*cols))
        return
    theArray = []
    for i in range(rows):
        row = []
        for j in range (cols):
            row.append(string[(i*cols)+j])
        theArray.append(row)    
    
    return theArray


#take a 2D list and return a single string of all its elements concatinated.
def TwoD2Str(theArray): 
    rows = len(theArray)
    cols = len(theArray[0])
    
    theString = ""
    for i in range(rows):
        tempstring = ""
        for j in range(cols):
            tempstring += theArray[i][j]
        theString += tempstring
        
    
    return theString