#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 10:41:31 2019

@author: jsw
"""

import JStrings as JS
import tkinter as TK
from tkinter import messagebox
from tkinter import filedialog
import random
from functools import partial
import math

################THIS CLASS CONTAINS THE DATA STRUCTURE#####################################
################OPERATIONS/METHODS ARE INDEPENDENT OF VISUALIZATION########################

class block:
    
    mirror = None
    r = 0 
    c = 0 
    s = ""
    
    def __init__(self, string, rows, cols):
        self.s = string
        self.r = rows
        self.c = cols
        #print("you created a block with {} rows and {} cols and the string is {}".format(\
        #      self.r, self.c, self.s))
    
    #method to print a block in the terminal 
    def bPrint(self): 
        
        for i in range(self.r):
            rowstring = ""
            for j in range(self.c):
                rowstring+=self.s[(i*self.c)+j]+" "
            #rowstring +="\n"    
            print(rowstring)
            
        print("this is a test of printing method for a block")

    def bPrintUD(self): 
        
        for i in range(self.r-1, -1, -1):
            rowstring = ""
            for j in range(self.c):
                rowstring+=self.s[(i*self.c)+j]+" "
            #rowstring +="\n"    
            print(rowstring)
            
        print("this is a test of printing method for a block")    
    
    #this method will tile a block, returning a new block made from copies of the old one
    def bTile(self, hRepeat, vRepeat):
        print("this is a function call to tile the block")
        
        
        blockstring=""
        for i in range (self.r*vRepeat):
            for j in range(self.c*hRepeat):
                BSindex = ((i%self.r)*self.c)+(j%self.c)
                blockstring += self.s[BSindex] 
                #if (j+1)==(bCols*hRepeat): 
                    #blockstring += "\n"
        return block(blockstring, self.r*vRepeat, self.c*hRepeat)
    
    #method to add the necessary edges to a block
    def addEdges(self, width=2):
        blockarray = JS.strTo2D(self.s, self.r, self.c)
        #add border to left of row
        for i in range(self.r):
            for j in range(width):
                if i%2 == 1:
                    blockarray[i].insert(0, "B")
                    blockarray[i].append("B")
                else:
                    blockarray[i].insert(0, "W")
                    blockarray[i].append("W")
        self.c+= width*2    
        self.s = JS.TwoD2Str(blockarray)
        
    def addBase(self, thickness):
        return
        
    def addCap(self, thickness): 
        return 
    
    def validate(self, maxRun):
        print("This method will make sure it's a valid mosaic pattern")
        runs = self.findLongRuns(maxRun)
        problems = [0] #this will store a list of indices where there's a problem
        print("found long runs here: {}".format(runs))
        return runs

    def findLongRuns(self, maxRun):
        theBlock = JS.strTo2D(self.s, self.r, self.c) 
        
        wRuns = []
        bRuns = []
        Runs = []
        
        
        numRows = len(theBlock)
        stitchPRow = len(theBlock[0])
        for row in range(numRows-1, -1, -1): 
        #start looking at a row:    
            runLen = 0
            longRun = []
            for stitch in range(stitchPRow):
                lastStitch = stitchPRow - 1


                #this indent checks black rows for too many white/green stitches
                if row%2== 1: #checking a '0' row for too many '-'s 
                    
                    if theBlock[row][stitch] == "-":
                        
                        runLen += 1
                        longRun.append(self.r*row+stitch)
                        
                        if (runLen > maxRun): #once run is long enough, it's an error
                            
                            if (stitch != lastStitch): 
                                #look at the next stitch, see if it's not part of the run
                                #if so, run is over
                                if theBlock[row][stitch+1] == "0":
                                    wRuns.append(longRun)
                                    runLen = 0
                                
                            else:
                               
                                longRun.append(self.r*row+stitch)
                                wRuns.append(longRun)
                                runLen = 0
                       
                        #check for wrapping (too) long runs
                        if stitch == lastStitch:
                             i = 1
                             while theBlock[row][(stitch + i)%stitchPRow] == "-" :
                                 runLen += 1
                                 if runLen > stitchPRow:
                                     break
                                 longRun.append(self.r*row+((stitch + i)%stitchPRow))
                                 i += 1
                             if runLen > maxRun:
                                 wRuns.append(longRun)
                                           
                    if theBlock[row][stitch] == "0":
                        runLen = 0
                        longRun = []
                
                if not wRuns:
                    Runs.append(wRuns)
               
                if row%2 == 0: #checking a '-' row for too many '0's 
                    
                    if theBlock[row][stitch] == "0":
                        
                        runLen += 1
                        longRun.append(self.r*row+stitch)
                        
                        if (runLen > maxRun): #once run is long enough, it's an error
                            if (stitch != lastStitch): 
                                if theBlock[row][stitch+1] == "-":
                                    bRuns.append(longRun)
                                    runLen = 0
                                
                            else:
                                longRun.append(self.r*row+stitch)
                                bRuns.append(longRun)
                                runLen = 0
                    
                                                #check for wrapping (too) long runs
                        if stitch == lastStitch:
                             i = 1
                             while theBlock[row][(stitch + i)%stitchPRow] == "0" :
                                 runLen += 1
                                 if runLen > stitchPRow:
                                     break
                                 longRun.append(self.r*row+((stitch + i)%stitchPRow))
                                 i += 1
                             if runLen > maxRun:
                                 bRuns.append(longRun)
                    
                    if theBlock[row][stitch] == "-":
                        runLen = 0
                        longRun = []
                
                
                if not bRuns:
                    Runs.append(bRuns)    
                        
        
        
        if not Runs:
            print("No Long Runs!")
        # else:
        #     if Runs[0]:
        #         print("the long green runs are here: {}".format(Runs[0])) 
        #         for run in Runs[0]:
        #             for stitch in range(len(run)):
        #                 self.itemconfig(self.squares[run[stitch]][0], outline="red", width="5")

        #     if Runs[1]:
        #         print("the long black runs are here: {}".format(Runs[1])) 
        #         for run in Runs[1]:
        #             for stitch in range(len(run)):
        #                 self.itemconfig(self.squares[run[stitch]][0], outline="blue", width="5")
        return [wRuns, bRuns]                  
        

    def findBadLifts(self):
        theBlock = JS.strTo2D(self.s, self.r, self.c) 
        
        bBLifts = []
        bWLifts = []
        bLifts = []
        
        
        numRows = len(theBlock)
        
        stitchPRow = len(theBlock[0])
        for row in range(numRows-1, -1, -1): 
            print("checking row {} for bad lifts".format(row)) 
            rowBelow = (row+1)%self.r
        #start looking at each stitch a row:    
            for stitch in range(stitchPRow):
                if row%2== 1: #checking a '0' row for bad '-' lifts
                    print("row {} is a black row".format(row))
                    if theBlock[row][stitch] == "-": #if it's a lift         
                        if theBlock[rowBelow][stitch] != "-":
                            bBLifts.append(row*self.c+stitch)
                            #print("bad black lift found at stitch {}".format(stitch))

            for stitch in range(stitchPRow):
                if row%2== 0: #checking a '-' row for bad '0' lifts
                    print("row {} is a black row".format(row))
                    if theBlock[row][stitch] == "0": #if it's a lift         
                        if theBlock[rowBelow][stitch] != "0":
                            bWLifts.append(row*self.c+stitch)
                            #print("bad black lift found at stitch {}".format(stitch))
        #self.itemconfig(width = 300)
        #self.itemconfig(height = 300)

        if not bBLifts and not bWLifts:
            print("no bad lifts! congrats!")   

        if bBLifts:
            print("bad black lifts here: {}".format(bBLifts)) 
            # for stitch in bBLifts:
            #     self.itemconfig(self.squares[stitch][0], outline="yellow", width="5")   
        
        
        if bWLifts:
            print("bad green lifts here: {}".format(bWLifts)) 
            # for stitch in bWLifts:
            #     self.itemconfig(self.squares[stitch][0], outline="white", width="5")  

        bLifts = [bBLifts, bWLifts]
        return bLifts     



