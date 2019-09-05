#######functions that generate diffenet types of blocks (meaning, the list necessary to construct
# a block of the particular type)
import JStrings as JS
import tkinter as TK
from tkinter import messagebox
from tkinter import filedialog
import random
from functools import partial
import math

def swapSinString(string, stitchList): ##take a string and list of coords and swap those stitches
    asList = list(string)
    for stitch in stitchList:
        if asList[stitch] == "0":
            asList[stitch] = "-"
        else:
            asList[stitch] = "O"  
    swappedString = "".join(asList)   
    return swappedString     

def findBadLifts(string, rows, cols):
    theBlock = JS.strTo2D(string, rows, cols) 
    
    bBLifts = []
    bWLifts = []
    bLifts = []
    
    
    numRows = len(theBlock)
    
    stitchPRow = len(theBlock[0])
    for row in range(numRows-1, -1, -1): 
        # print("checking row {} for bad lifts".format(row)) 
        rowBelow = (row+1)%rows
    #start looking at each stitch a row:    
        for stitch in range(stitchPRow):
            if row%2== 1: #checking a '0' row for bad '-' lifts
                # print("row {} is a black row".format(row))
                if theBlock[row][stitch] == "-": #if it's a lift         
                    if theBlock[rowBelow][stitch] != "-":
                        bBLifts.append(row*cols+stitch)
                        #print("bad black lift found at stitch {}".format(stitch))

        for stitch in range(stitchPRow):
            if row%2== 0: #checking a '-' row for bad '0' lifts
                # print("row {} is a black row".format(row))
                if theBlock[row][stitch] == "0": #if it's a lift         
                    if theBlock[rowBelow][stitch] != "0":
                        bWLifts.append(row*cols+stitch)
                        #print("bad black lift found at stitch {}".format(stitch))
    #self.itemconfig(width = 300)
    #self.itemconfig(height = 300)

    if not bBLifts and not bWLifts:
        print("no bad lifts! congrats!")   

    # if bBLifts:
    #     print("bad black lifts here: {}".format(bBLifts)) 
    #     # for stitch in bBLifts:
    #     #     self.itemconfig(self.squares[stitch][0], outline="yellow", width="5")   
    
    
    # if bWLifts:
    #     print("bad green lifts here: {}".format(bWLifts)) 
    #     # for stitch in bWLifts:
    #     #     self.itemconfig(self.squares[stitch][0], outline="white", width="5")  

    for lift in bBLifts:
        bLifts.append(lift)

    for lift in bWLifts:
        bLifts.append(lift)    
    return bLifts  


def defaultBlock(rows, cols):  
    blockS = ""
    for i in range(rows):
        for stitch in range(cols):
            if i%2 == 0:
                blockS += "-"
            else:
                blockS += "0"    

    return [blockS, rows, cols]    


def randomBlock(rows, cols):
    stitches =["0", "-"]
    slength = rows*cols
    blockS = ""
    for i in range(slength):  
        blockS += random.choice(stitches)
    return [blockS, rows, cols]  

##remember: top row is always --- bottom row is 0000
##this method generates rows from the bottom of the block upward. 

def randomVBlock(rows, cols, longestRun): #first make a random block that has no bad long runs
    stitches = ["0", "-"]
    theblock = []
    for row in range(rows):
        #print("ATTENTION: Generating row {}".format(row))
        theRow=[]
        run = 0
        for stitch in range(cols):
            newStitch = random.choice(stitches)
            if (row % 2) == 1: ## we're in a "-" row so avoid "0" runs
                #newStitch = "-"
                if newStitch == "-":   # this is always fine on this row.                 
                    run = 0
                if newStitch == "0": 
                    run+=1
                    if stitch == (cols - 1): #special case for last stitch to avoid wrapped longruns
                        checkWrap = 0
                        while theRow[checkWrap] == "0": 
                            run +=1 #adds to runs if there are sequential "0"s at beginning of row
                            checkWrap +=1
                    if run > longestRun: #in this case swap the stitch and reset run
                        newStitch = "-"
                        run = 0   
                    # if ((row > 0) & (theblock[row-1][stitch] != "0")):  
                    #     newStitch = "-"        

            if (row % 2) == 0: ## we're in a "0" row so avoid "-" runs
                #newStitch = "0"
                if newStitch == "0":                   
                    run = 0
                if newStitch == "-": 
                    run+=1
                    if stitch == (cols - 1): #special case for last stitch to avoid wrapped longruns
                        checkWrap = 0
                        while theRow[checkWrap] == "-": 
                            run +=1 #adds to runs if there are sequential "0"s at beginning of row
                            checkWrap +=1
                    if run > longestRun: #in this case swap the stitch and reset run
                        newStitch = "0"
                        run = 0
            theRow.append(newStitch)  
        theblock.insert(0, theRow)
        # print("row {} is this:{}".format(row, theRow))
    
    blockString = (JS.TwoD2Str(theblock))
    badLifts = findBadLifts(blockString, rows, cols)
    noBadLifts = swapSinString(blockString, badLifts)

        
    return [noBadLifts, rows, cols]    #returns a block!  

    #helper function to genreate box coordinates
def boxCoords(w, h, numAcross, numUp):
    bW = w/numAcross
    bH = h/numUp
    coordList = []
    for i in range (numAcross*numUp):
       ULx = (i%numAcross)*bW
       ULy = (i//numAcross)*bH      
       coordList.append([ULx, ULy, ULx+bW, ULy, ULx+bW, ULy+bH, ULx, ULy+bH]) #list is [UL(x, y), UR(x, y), LR(x, y), LL(x,y)]
    return coordList